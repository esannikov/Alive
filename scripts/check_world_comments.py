#!/usr/bin/env python3
"""Read-only setup preflight. Never install an app, post a comment, or alter repository visibility."""
import json, subprocess, sys, urllib.request, urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/'Production/Dashboard/comments.json').read_text())
repo=json.loads(subprocess.check_output(['gh','api','repos/'+cfg['repo']],text=True))
if repo['private'] or not repo['has_discussions']:
    sys.exit('Repository must be public with Discussions enabled; visibility is never changed by this script.')
url='https://giscus.app/api/discussions/categories?repo='+cfg['repo'].replace('/','%2F')
try:
    with urllib.request.urlopen(url,timeout=20) as response: data=json.load(response)
except urllib.error.HTTPError as e:
    sys.exit(e.read().decode())
category=next((x for x in data['categories'] if x['name']==cfg['category']),None)
if not category:sys.exit('Create the Comments category in Announcement format in GitHub Discussions.')
if data['repositoryId']!=repo['node_id']:sys.exit('Repository ID mismatch')
print(json.dumps({'repo':cfg['repo'],'repoId':data['repositoryId'],'category':category['name'],'categoryId':category['id'],'giscusInstalled':True,'note':'Confirm Announcement format in GitHub UI before enabling comments.json.'},ensure_ascii=False,indent=2))
