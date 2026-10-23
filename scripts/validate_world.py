#!/usr/bin/env python3
"""Validate identity, published references and safety of the static catalogue."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/World'
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ['src','href']:
            if key in a:self.links.append(a[key])

def main():
    registry=json.loads((ROOT/'Production/Dashboard/asset_codes.json').read_text())
    data=json.loads((OUT/'data.js').read_text().removeprefix('window.ALIVE_WORLD=').strip().removesuffix(';'))
    codes=[a['code'] for a in registry['assets']]
    assert len(codes)==len(set(codes)) and codes
    assert not set(codes).intersection(registry.get('deleted_codes',[])), 'Deleted code was reused'
    assert data.get('deletedCodes',[])==registry.get('deleted_codes',[])
    assert codes==[a['code'] for a in data['assets']], 'Code ordering changed'
    for a in registry['assets']:
        assert re.fullmatch(r'[a-z]+\d{3,}',a['code'])
        assert hashlib.sha256((ROOT/a['source_file']).read_bytes()).hexdigest()==a['sha256'], a['code']
    for a in data['assets']:
        assert (ROOT/a['sourceFile']).is_file()
        display=(OUT/a['display']).resolve()
        assert display==(ROOT/a['sourceFile']).resolve() and display.is_relative_to(ROOT/'docs')
        assert a['original'].startswith('https://raw.githubusercontent.com/esannikov/Alive/')
        assert (OUT/a['preview']).is_file() and (OUT/a['thumb']).is_file()
    tasks={t['id'] for t in data['tasks']}
    assert tasks=={t['id'] for t in json.loads((ROOT/'Production/research_plan.json').read_text())['tasks']}
    for o in data['objects']:
        assert o['cover'] in codes
        assert set(o['task_ids'])<=tasks
    pages=list(OUT.rglob('*.html')); parsed={}
    for p in pages:
        text=p.read_text();parser=Links();parser.feed(text);parsed[p.resolve()]=parser
        assert len(parser.ids)==len(set(parser.ids)), f'Duplicate HTML ID: {p}'
        assert '/Users/' not in text and 'file://' not in text
        assert not any(x in text for x in ['textarea','Утвердить образ','Вернуть на доработку','Решение по образу','Комплект персонажа']),p
        for link in parser.links:
            u=urlsplit(link)
            if u.scheme:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
            if target.is_dir():target=target/'index.html'
            assert target.is_relative_to(ROOT/'docs'),(p,link)
            assert target.is_file(),(p,link)
    for p,parser in parsed.items():
        for link in parser.links:
            u=urlsplit(link)
            if u.scheme or not u.fragment or u.fragment.startswith('task='):continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            if target.is_dir():target=target/'index.html'
            if target in parsed:assert unquote(u.fragment) in parsed[target].ids,(p,link)
    for a in data['assets']:
        target=OUT/a.get('page',f'characters/{a["object"]}/')/'index.html'
        assert (a['code'] in parsed[target.resolve()].ids) == (not a.get('archived',False))
    flow=(ROOT/'docs/ProductionFlow/index.html').read_text()
    mapping=json.loads(re.search(r'const WORLD_LINKS=(.*?);\n',flow)[1])
    assert set(mapping)<=tasks
    for links in mapping.values():
        for link in links:assert (ROOT/'docs/ProductionFlow'/link['url']/'index.html').resolve().is_file()
    for filename in ['site.js','data.js']:
        subprocess.run(['node','--check',str(OUT/filename)],check=True)
    for name in ['Onest','IBMPlexMono']:assert 'SIL OPEN FONT LICENSE' in (OUT/f'fonts/OFL-{name}.txt').read_text()
    print(json.dumps({'status':'PASS','pages':len(pages),'codes':len(codes),'active_images':sum(not a.get('archived',False) for a in data['assets']),'tasks':len(tasks),'bidirectional_task_links':len(mapping),'source_hashes':'match'},ensure_ascii=False))
if __name__=='__main__':main()
