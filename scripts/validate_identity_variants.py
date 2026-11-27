#!/usr/bin/env python3
"""Validate casting identities independently from immutable image codes."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def validate():
 source=json.loads((ROOT/'Production/Dashboard/identity_variants.json').read_text())
 registry=json.loads((ROOT/'Production/Dashboard/asset_codes.json').read_text())
 config=json.loads((ROOT/'Production/Dashboard/objects.json').read_text())
 published=json.loads((ROOT/'docs/World/identity-variants.json').read_text())
 runtime=json.loads((ROOT/'docs/World/data.js').read_text().removeprefix('window.ALIVE_WORLD=').strip().removesuffix(';'))
 by={a['code']:a for a in registry['assets']};hum={o['id']for o in config['objects']if o['group']=='people'and o['id']not in ['base-girls','tais-clothing']}
 variants={v['id']:v for v in source['variants']};assert len(variants)==len(source['variants'])
 for vid,v in variants.items():
  char=v['character'];assert char in hum and re.fullmatch(re.escape(char)+r'-type-\d{3,}',vid)
  assert v['anchor_asset']in by and v['cover_asset']in v['member_codes']
  assert len(v['member_codes'])==len(set(v['member_codes']))
  for code in v['member_codes']:assert source['assets'][code]['variants'][char]==vid
 for code,m in source['assets'].items():
  assert code in by and not(set(m['variants'])&set(m['review_required']))
  for char,vid in m['variants'].items():assert vid in variants and variants[vid]['character']==char and code in variants[vid]['member_codes']
 for a in by.values():
  if a.get('visibility')=='archived':continue
  for char in [a['object']]+a.get('additional_objects',[]):
   if char in hum:
    m=source['assets'].get(a['code'],{});assert char in m.get('variants',{}) or char in m.get('review_required',{}),(a['code'],char)
 assert runtime['identityVariants']==published['variants']
 for a in runtime['assets']:
  m=source['assets'].get(a['code'],{})
  assert a['identityVariantIds']==m.get('variants',{})
  assert a['identityReviewRequired']==m.get('review_required',{})
 for v in published['variants']:
  src=variants[v['id']]
  for k,val in src.items():assert v[k]==val
  expected=[c for c in src['member_codes']if by[c].get('visibility')!='archived' and(v['character']==by[c]['object']or v['character']in by[c].get('additional_objects',[]))]
  assert v['active_asset_codes']==expected
  cover=by[v['cover_asset']]
  if expected:
   assert v['cover_asset'] in expected, 'Identity cover must be a current frame of its character'
  else:
   assert cover.get('visibility')=='archived' or v['character'] in cover.get('previous_objects',[]), 'Inactive identity needs explicit archive/reserve provenance'
 # Regression cases: preserve independent casts, producer split, shared-scene identities.
 ids=lambda c:source['assets'][c]['variants']
 assert len({ids(c)['emma']for c in ['emma027','emma028','emma033','emma037','emma038']})==1
 assert len({ids(c)['emma']for c in ['emma023','emma024','emma025','emma026']})==4
 assert ids('tais053')['tais']!=ids('tais059')['tais']
 assert ids('romik007')['romik']!=ids('romik007')['vovik']
 assert ids('romik007')['romik']==ids('romik002')['romik']
 assert len({ids(c)['kolka']for c in ['kolka033','kolka034','kolka035','kolka036']})==1
 assert ids('nitka007')['nitka']==ids('nitka008')['nitka']
 assert source['assets']['emma036']['review_required'].get('emma')
 print(json.dumps({'status':'PASS','variants':len(variants),'mapped_assets':len(source['assets']),'unresolved_character_appearances':sum(len(m['review_required'])for m in source['assets'].values())}))
if __name__=='__main__':validate()
