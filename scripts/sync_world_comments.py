#!/usr/bin/env python3
"""Read Discussions and publish a small public feed. Never post comments.

Uses gh's ambient authentication (GITHUB_TOKEN in Actions); credentials never enter
JSON or browser code. Only one generated file on the publication branch is writable.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import re
import subprocess
from zoneinfo import ZoneInfo
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'esannikov/Alive'
BRANCH = 'codex/alive-roadmap-site'
TARGET = 'docs/World/recent-comments.json'


def gh_api(endpoint, payload=None, method=None):
    command = ['gh', 'api', endpoint]
    if method:
        command += ['--method', method]
    if payload is not None:
        command += ['--input', '-']
    result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                            text=True, capture_output=True, check=True)
    response = json.loads(result.stdout)
    if response.get('errors'):
        raise RuntimeError('GitHub GraphQL returned an error; feed was not changed')
    return response


def graphql(query, **variables):
    return gh_api('graphql', {'query': query, 'variables': variables})['data']


COMMENT_FIELDS = 'id url createdAt bodyText isMinimized author { login }'
DISCUSSIONS = '''query($category:ID!,$cursor:String) {
 repository(owner:"esannikov",name:"Alive") {
  discussions(first:100,categoryId:$category,after:$cursor) {
   nodes { id number title body }
   pageInfo { hasNextPage endCursor }
  }
 }
}'''
COMMENTS = '''query($id:ID!,$cursor:String) {
 node(id:$id) { ... on Discussion { comments(first:100,after:$cursor) {
  nodes { %s replies(last:100) { nodes { %s } pageInfo { hasPreviousPage startCursor } } }
  pageInfo { hasNextPage endCursor }
 } } }
}''' % (COMMENT_FIELDS, COMMENT_FIELDS)

REPLIES = """query($id:ID!,$before:String) {
 node(id:$id) { ... on DiscussionComment { replies(last:100,before:$before) {
  nodes { %s } pageInfo { hasPreviousPage startCursor }
 } } }
}""" % COMMENT_FIELDS


def visible_replies(comment, limit=5):
    connection = comment['replies']
    found = []
    while True:
        found.extend(r for r in connection['nodes'] if not r.get('isMinimized'))
        info = connection.get('pageInfo', {})
        if (limit is not None and len(found) >= limit) or not info.get('hasPreviousPage'):
            return sorted(found, key=lambda r: (r['createdAt'], r['id']), reverse=True)[:limit]
        cursor = info.get('startCursor')
        if not cursor:
            raise RuntimeError('Invalid reply pagination')
        connection = graphql(REPLIES, id=comment['id'], before=cursor)['node']['replies']
        if connection.get('pageInfo', {}).get('hasPreviousPage') and connection['pageInfo'].get('startCursor') == cursor:
            raise RuntimeError('Reply pagination did not advance')


def paginated(query, select, **variables):
    cursor = None
    while True:
        connection = select(graphql(query, cursor=cursor, **variables))
        yield from connection['nodes']
        info = connection['pageInfo']
        if not info['hasNextPage']:
            break
        next_cursor = info['endCursor']
        if not next_cursor or next_cursor == cursor:
            raise RuntimeError('Invalid pagination; feed was not changed')
        cursor = next_cursor


def identify_page(discussion, pages):
    # Strict Giscus mapping survives a renamed discussion title.
    for page in pages:
        digest = hashlib.sha1(page['term'].encode()).hexdigest()
        if f'<!-- sha1: {digest} -->' in discussion['body']:
            return page
    return None


def make_item(comment, page):
    if comment.get('isMinimized'):
        return None
    excerpt = re.sub(r'\s+', ' ', comment.get('bodyText', '')).strip()
    if not excerpt:
        return None
    if len(excerpt) > 260:
        excerpt = excerpt[:257].rstrip() + '…'
    return {'id': comment['id'], 'page': page['page'], 'title': page['title'],
            'author': (comment.get('author') or {}).get('login') or 'Удалённый аккаунт',
            'createdAt': comment['createdAt'], 'excerpt': excerpt, 'url': comment['url']}


def collect(pages, category, discussion_numbers=None, discussion_stats=None):
    found = {}
    if discussion_stats is not None:
        discussion_stats.update({p['page']: {'messageCount': 0, 'last': None} for p in pages})
    # Match the same oldest canonical thread used by the direct widget binding.
    selected = {}
    discussions = paginated(DISCUSSIONS, lambda d: d['repository']['discussions'], category=category)
    for discussion in discussions:
        page = identify_page(discussion, pages)
        if page is None:
            continue
        previous = selected.get(page['page'])
        if previous is None or discussion['number'] < previous[0]['number']:
            selected[page['page']] = (discussion, page)
    for discussion, page in selected.values():
        if discussion_numbers is not None:
            discussion_numbers[page['page']] = discussion['number']
        messages = {}
        comments = paginated(COMMENTS, lambda d: d['node']['comments'], id=discussion['id'])
        for comment in comments:
            if comment.get('isMinimized'):
                continue
            for entry in [comment, *visible_replies(comment, limit=None)]:
                # Include image-only messages in the count, even without an excerpt.
                messages[entry['id']] = entry
                item = make_item(entry, page)
                if item:
                    found[item['id']] = item
        if discussion_stats is not None:
            latest = max(messages.values(), key=lambda x: (x['createdAt'], x['id'])) if messages else None
            discussion_stats[page['page']] = {
                'messageCount': len(messages),
                'last': {'author': (latest.get('author') or {}).get('login') or 'Удалённый аккаунт',
                         'createdAt': latest['createdAt']} if latest else None,
            }
    return sorted(found.values(), key=lambda c: (c['createdAt'], c['id']), reverse=True)[:5]


def publish(feed):
    endpoint = f'repos/{REPO}/contents/{TARGET}'
    # Optimistic retry tolerates a simultaneous normal site publication.
    for attempt in range(3):
        current = gh_api(endpoint + '?ref=' + BRANCH)
        previous = json.loads(base64.b64decode(current['content']))
        if previous.get('items') == feed['items'] and previous.get('schemaVersion') == 1 and previous.get('discussionNumbers', {}) == feed.get('discussionNumbers', {}) and previous.get('discussionStats', {}) == feed.get('discussionStats', {}):
            print('Feed is current; no commit needed')
            return
        try:
            gh_api(endpoint, {'message': 'Update latest World comments', 'branch': BRANCH,
                              'sha': current['sha'], 'content': base64.b64encode(
                                  (json.dumps(feed, ensure_ascii=False, indent=2)+'\n').encode()).decode()}, method='PUT')
            print(f"Published {len(feed['items'])} comments")
            return
        except subprocess.CalledProcessError as error:
            if attempt == 2 or not any(code in error.stderr for code in ('409', '422')):
                raise


VOTE_REACTIONS = """query($id:ID!,$cursor:String) {
 node(id:$id) { ... on Discussion { reactions(first:100,after:$cursor) {
  nodes { id content createdAt user { login } }
  pageInfo { hasNextPage endCursor }
 } } }
}"""


def summarize_votes(reactions, members):
    weights = {k.lower(): v for k, v in members.items()}
    latest = {}
    for reaction in reactions:
        login = (reaction.get('user') or {}).get('login', '')
        key = login.lower()
        if key not in weights or reaction['content'] not in ('THUMBS_UP','THUMBS_DOWN'):
            continue
        if key not in latest or (reaction['createdAt'],reaction['id']) > (latest[key]['createdAt'],latest[key]['id']):
            latest[key] = reaction
    votes = [{'login': r['user']['login'], 'choice': 'for' if r['content']=='THUMBS_UP' else 'against',
              'weight': weights[k], 'createdAt':r['createdAt'], 'reactionId':r['id']}
             for k,r in sorted(latest.items())]
    scores = {s:sum(v['weight'] for v in votes if v['choice']==s) for s in ('for','against')}
    counts = {s:sum(v['choice']==s for v in votes) for s in ('for','against')}
    status = ('unanimous_against' if counts['against']>=2 and counts['for']==0 else
              'mixed' if counts['against'] and counts['for'] else 'for' if counts['for'] else
              'against_pending' if counts['against'] else 'unvoted')
    return {'votes':votes,'scores':scores,'people':counts,'status':status,'automaticRemoval':False}


def collect_votes(pages, config):
    members=config['voting']['members']
    codes={code for p in pages for code in p.get('variantCodes',[])}
    result={code:summarize_votes([],members) for code in sorted(codes)}
    selected={}
    for d in paginated(DISCUSSIONS,lambda x:x['repository']['discussions'],category=config['categoryId']):
        if not d['title'].startswith('ALIVE vote v1 '): continue
        code=d['title'].removeprefix('ALIVE vote v1 ')
        if code not in codes: continue
        digest=hashlib.sha1(d['title'].encode()).hexdigest()
        if f'<!-- sha1: {digest} -->' not in d['body']: continue
        if code not in selected or d['number']<selected[code]['number']: selected[code]=d
    for code,d in selected.items():
        reactions=list(paginated(VOTE_REACTIONS,lambda x:x['node']['reactions'],id=d['id']))
        result[code]=summarize_votes(reactions,members)
        result[code].update({'discussionNumber':d['number'],'url':f"https://github.com/{REPO}/discussions/{d['number']}"})
    return {'schemaVersion':1,'generatedAt':dt.datetime.now(dt.timezone.utc).isoformat(),
            'members':members,'minimumAgainstPeople':2,'automaticRemoval':False,'variants':result}


def vote_refresh_slot(now=None):
    local=(now or dt.datetime.now(dt.timezone.utc)).astimezone(ZoneInfo('Europe/Kyiv'))
    if local.hour>=21: return local.strftime('%Y-%m-%d')+'T21'
    if local.hour>=9: return local.strftime('%Y-%m-%d')+'T09'
    return (local-dt.timedelta(days=1)).strftime('%Y-%m-%d')+'T21'


def votes_due():
    response=gh_api(f'repos/{REPO}/contents/docs/World/votes.json?ref={BRANCH}')
    previous=json.loads(base64.b64decode(response['content']))
    return previous.get('refreshSlot') != vote_refresh_slot()


def publish_votes(data):
    endpoint=f'repos/{REPO}/contents/docs/World/votes.json'
    for attempt in range(3):
        current=gh_api(endpoint+'?ref='+BRANCH)
        old=json.loads(base64.b64decode(current['content']))
        if old.get('variants')==data['variants'] and old.get('refreshSlot')==data.get('refreshSlot'):
            return
        try:
            gh_api(endpoint,{'message':'Update World vote status','branch':BRANCH,'sha':current['sha'],
                'content':base64.b64encode((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()).decode()},method='PUT')
            return
        except subprocess.CalledProcessError as error:
            if attempt==2 or not any(code in error.stderr for code in ('409','422')): raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--refresh-votes', action='store_true', help='Refresh vote data now for a requested review')
    parser.add_argument('--output', type=Path, default=ROOT/TARGET)
    args = parser.parse_args()
    config = json.loads((ROOT/'Production/Dashboard/comments.json').read_text())
    pages = json.loads((ROOT/'docs/World/comment-pages.json').read_text())
    # Overview has a feed, not its own comment form.
    pages = [p for p in pages if p['page']]
    discussion_numbers = {}
    discussion_stats = {}
    items = collect(pages, config['categoryId'], discussion_numbers, discussion_stats)
    feed = {'schemaVersion': 1, 'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(), 'items': items, 'discussionNumbers': discussion_numbers, 'discussionStats': discussion_stats}
    votes = collect_votes(pages, config) if config.get('voting') and (not args.publish or args.refresh_votes or votes_due()) else None
    if votes is not None: votes['refreshSlot'] = vote_refresh_slot()
    if args.publish:
        publish(feed)
        if votes is not None: publish_votes(votes)
    else:
        args.output.write_text(json.dumps(feed, ensure_ascii=False, indent=2)+'\n')
        if votes is not None: (ROOT/'docs/World/votes.json').write_text(json.dumps(votes,ensure_ascii=False,indent=2)+'\n')
        print(f'Collected {len(items)} comments')


if __name__ == '__main__':
    main()
