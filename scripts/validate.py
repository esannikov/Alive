#!/usr/bin/env python3
"""Check ALIVE file portability and immutable source integrity (Python stdlib)."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
import hashlib,json,re,sys,unicodedata
ROOT=Path(__file__).resolve().parents[1]

def slug(text):
    text=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',text)
    return re.sub(r'[^\w\- ]','',text.lower()).replace(' ','-')

def anchors(text):
    out=set();counts=Counter()
    for line in text.splitlines():
        m=re.match(r'^#{1,6}\s+(.+)',line)
        if m:
            base=slug(m[1]);n=counts[base];counts[base]+=1
            out.add(base+(f'-{n}' if n else ''))
        m=re.search(r'\s\^([\w-]+)\s*$',line)
        if m:out.add('^'+m[1])
    return out

def main():
    errors=[];link_count=0;anchor_count=0
    files=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts]
    markdown={p.resolve():p.read_text() for p in files if p.suffix=='.md'}
    anchor_map={p:anchors(t) for p,t in markdown.items()}
    for p,t in markdown.items():
        rel=p.relative_to(ROOT)
        if '/Users/' in t or 'file://' in t:errors.append(f'{rel}: machine-specific path')
        if re.search(r'^(?:<{7}|={7}|>{7})(?: |$)',t,re.M):errors.append(f'{rel}: merge conflict marker')
        if re.search(r'\[\[03PROJECTS/',t):errors.append(f'{rel}: unresolved old vault link')
        for raw in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)',t):
            url=urlsplit(raw)
            if url.scheme or raw.startswith('//'):continue
            path=unquote(url.path)
            if path!=unicodedata.normalize('NFC',path):errors.append(f'{rel}: non-portable Unicode link: {raw}')
            target=(p.parent/path).resolve() if path else p
            link_count+=1
            if not target.is_relative_to(ROOT):errors.append(f'{rel}: link escapes repository: {raw}');continue
            if not target.exists():errors.append(f'{rel}: missing target: {raw}');continue
            if url.fragment and target.suffix=='.md':
                anchor_count+=1
                if unquote(url.fragment) not in anchor_map.get(target,set()):errors.append(f'{rel}: missing anchor: {raw}')
    manifest=json.loads((ROOT/'Sources/source_manifest.json').read_text())
    source_count=0
    for item in manifest['files']:
        source_count+=1;p=ROOT/item['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
            errors.append(f"{item['path']}: source checksum mismatch")
    evidence=json.loads((ROOT/'Sources/Design_Evidence.json').read_text())
    for path_key,hash_key in [('source','source_sha256'),('text_source','text_source_sha256')]:
        source=ROOT/evidence[path_key]
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=evidence[hash_key]:
            errors.append(f'Art direction evidence {path_key} checksum mismatch')
    if len(evidence['cards'])!=108:errors.append('Expected 108 design cards')
    for card in evidence['cards']:
        if not (ROOT/card['file']).is_file():errors.append(f"Missing card file: {card['id']}")
        if not card['pages'] or any(not 1<=n<=538 for n in card['pages']):errors.append(f"Invalid source page: {card['id']}")
    if any((ROOT/'Sources/Extracted').glob('S08*')) or (ROOT/'Sources/Citations/S08.md').exists():
        errors.append('Superseded novel copy is present')
    for p in files:
        if p.suffix=='.json':
            try:json.loads(p.read_text())
            except (ValueError,UnicodeError):errors.append(f'{p.relative_to(ROOT)}: invalid JSON')
        if p.is_symlink():errors.append(f'{p.relative_to(ROOT)}: symlink is not portable')
    report={'status':'PASS' if not errors else 'FAIL','markdown_files':len(markdown),'local_links':link_count,'anchors':anchor_count,'immutable_sources':source_count,'errors':errors}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if errors else 0

if __name__=='__main__':sys.exit(main())
