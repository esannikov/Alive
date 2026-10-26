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
  nodes { %s replies(last:5) { nodes { %s } pageInfo { hasPreviousPage startCursor } } }
  pageInfo { hasNextPage endCursor }
 } } }
}''' % (COMMENT_FIELDS, COMMENT_FIELDS)

REPLIES = """query($id:ID!,$before:String) {
 node(id:$id) { ... on DiscussionComment { replies(last:100,before:$before) {
  nodes { %s } pageInfo { hasPreviousPage startCursor }
 } } }
}""" % COMMENT_FIELDS


def visible_replies(comment):
    connection = comment['replies']
    found = []
    while True:
        found.extend(r for r in connection['nodes'] if not r.get('isMinimized') and r.get('bodyText', '').strip())
        info = connection.get('pageInfo', {})
        if len(found) >= 5 or not info.get('hasPreviousPage'):
            return sorted(found, key=lambda r: (r['createdAt'], r['id']), reverse=True)[:5]
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


def collect(pages, category, discussion_numbers=None):
    found = {}
    discussions = paginated(DISCUSSIONS, lambda d: d['repository']['discussions'], category=category)
    for discussion in discussions:
        page = identify_page(discussion, pages)
        if page is None:
            continue
        if discussion_numbers is not None:
            number = discussion['number']
            discussion_numbers[page['page']] = min(number, discussion_numbers.get(page['page'], number))
        comments = paginated(COMMENTS, lambda d: d['node']['comments'], id=discussion['id'])
        for comment in comments:
            # A minimized conversation is not promoted through its replies either.
            if comment.get('isMinimized'):
                continue
            for entry in [comment, *visible_replies(comment)]:
                item = make_item(entry, page)
                if item:
                    found[item['id']] = item
    return sorted(found.values(), key=lambda c: (c['createdAt'], c['id']), reverse=True)[:5]


def publish(feed):
    endpoint = f'repos/{REPO}/contents/{TARGET}'
    # Optimistic retry tolerates a simultaneous normal site publication.
    for attempt in range(3):
        current = gh_api(endpoint + '?ref=' + BRANCH)
        previous = json.loads(base64.b64decode(current['content']))
        if previous.get('items') == feed['items'] and previous.get('schemaVersion') == 1 and previous.get('discussionNumbers', {}) == feed.get('discussionNumbers', {}):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/TARGET)
    args = parser.parse_args()
    config = json.loads((ROOT/'Production/Dashboard/comments.json').read_text())
    pages = json.loads((ROOT/'docs/World/comment-pages.json').read_text())
    # Overview has a feed, not its own comment form.
    pages = [p for p in pages if p['page']]
    discussion_numbers = {}
    items = collect(pages, config['categoryId'], discussion_numbers)
    feed = {'schemaVersion': 1, 'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(), 'items': items, 'discussionNumbers': discussion_numbers}
    if args.publish:
        publish(feed)
    else:
        args.output.write_text(json.dumps(feed, ensure_ascii=False, indent=2)+'\n')
        print(f'Collected {len(items)} comments')


if __name__ == '__main__':
    main()
