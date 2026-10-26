"""No network or writes: verify aggregation across discussions and nested replies."""
import hashlib
import unittest
from unittest.mock import patch
import sync_world_comments as feed

PAGES = [{'term':'Alive/World/characters/emma/', 'page':'characters/emma/', 'title':'Эмма'},
         {'term':'Alive/World/robots/lon/', 'page':'robots/lon/', 'title':'Лон'}]

def thread(id, page):
    return {'id':id, 'title':'renamed', 'body':'<!-- sha1: '+hashlib.sha1(page['term'].encode()).hexdigest()+' -->'}

def comment(id, day, **overrides):
    return dict(id=id, createdAt=f'2026-10-{day:02}T12:00:00Z', url='https://github.com/esannikov/Alive/discussions/1',
                bodyText='A comment', author={'login':'reader'}, isMinimized=False, replies={'nodes':[]}, **overrides)

class FeedTests(unittest.TestCase):
    def test_collect(self):
        discussions=[thread('d1',PAGES[0]), thread('d2',PAGES[1]), {'id':'ignored','body':'another discussion','title':'Unknown'}]
        hidden=comment('hidden',29);hidden['isMinimized']=True;hidden['replies']['nodes']=[comment('hidden-reply',30)]
        old=comment('old',1);old['replies']['nodes']=[comment('new-reply',26)]
        comments={'d1':[old,hidden,comment('c20',20),comment('c21',21),comment('c22',22)], 'd2':[comment('c23',23),comment('c24',24),comment('c25',25)]}
        def fake(query, select, **kwargs):
            return iter(discussions if query==feed.DISCUSSIONS else comments[kwargs['id']])
        with patch.object(feed,'paginated',side_effect=fake):
            items=feed.collect(PAGES,'category')
        self.assertEqual([i['id'] for i in items],['new-reply','c25','c24','c23','c22'])
        self.assertEqual(items[0]['page'],'characters/emma/')
        self.assertEqual(items[1]['title'],'Лон')
    def test_directory_includes_empty_threads(self):
        discussion=thread('d1',PAGES[0]);discussion['number']=52
        def fake(query, select, **kwargs):return iter([discussion] if query==feed.DISCUSSIONS else [])
        directory={}
        with patch.object(feed,'paginated',side_effect=fake):
            self.assertEqual(feed.collect(PAGES,'category',directory),[])
        self.assertEqual(directory,{'characters/emma/':52})
    def test_directory_change_publishes_without_new_comments(self):
        import base64,json
        current={'sha':'abc','content':base64.b64encode(json.dumps({'schemaVersion':1,'items':[],'discussionNumbers':{}}).encode()).decode()}
        with patch.object(feed,'gh_api',side_effect=[current,{}]) as api:
            feed.publish({'schemaVersion':1,'items':[],'discussionNumbers':{'characters/emma/':52}})
            self.assertEqual(api.call_args.kwargs['method'],'PUT')
    def test_pagination(self):
        results=[{'nodes':[1], 'pageInfo':{'hasNextPage':True,'endCursor':'next'}}, {'nodes':[2], 'pageInfo':{'hasNextPage':False,'endCursor':None}}]
        with patch.object(feed,'graphql',side_effect=results) as call:
            self.assertEqual(list(feed.paginated('query',lambda x:x)),[1,2])
            self.assertEqual(call.call_args.kwargs['cursor'],'next')
    def test_excerpt_deleted_author(self):
        item=comment('a',20);item.update(author=None,bodyText='  hello\n '+('x'*300))
        result=feed.make_item(item,PAGES[0])
        self.assertEqual(result['author'],'Удалённый аккаунт')
        self.assertLessEqual(len(result['excerpt']),260)
        self.assertNotIn('\n',result['excerpt'])
    def test_empty_and_deleted(self):
        with patch.object(feed,'paginated',return_value=iter([])):
            self.assertEqual(feed.collect(PAGES,'category'),[])
    def test_hidden_replies_do_not_hide_older_visible_reply(self):
        parent=comment('parent',1)
        hidden=comment('hidden',26);hidden['isMinimized']=True
        parent['replies']={'nodes':[hidden], 'pageInfo':{'hasPreviousPage':True,'startCursor':'earlier'}}
        response={'node':{'replies':{'nodes':[comment('visible',25)],'pageInfo':{'hasPreviousPage':False}}}}
        with patch.object(feed,'graphql',return_value=response):
            self.assertEqual([r['id'] for r in feed.visible_replies(parent)],['visible'])
    def test_publish_uses_put(self):
        import base64,json
        current={'sha':'abc','content':base64.b64encode(json.dumps({'schemaVersion':1,'items':[{'old':True}]}).encode()).decode()}
        with patch.object(feed,'gh_api',side_effect=[current,{}]) as api:
            feed.publish({'schemaVersion':1,'items':[]})
            self.assertEqual(api.call_args.kwargs['method'],'PUT')
            self.assertEqual(api.call_args.args[1]['sha'],'abc')
    def test_no_commit_if_unchanged(self):
        import base64,json
        current={'sha':'abc','content':base64.b64encode(json.dumps({'schemaVersion':1,'items':[]}).encode()).decode()}
        with patch.object(feed,'gh_api',return_value=current) as api:
            feed.publish({'schemaVersion':1,'items':[]})
            self.assertEqual(api.call_count,1)

if __name__=='__main__':unittest.main()
