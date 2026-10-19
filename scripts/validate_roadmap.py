#!/usr/bin/env python3
"""Validate the standalone roadmap before publishing (stdlib only)."""
from pathlib import Path
import collections
import json
import re

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'docs/ProductionFlow/index.html').read_text()
data = json.loads(re.search(r'<script id="plan-data"[^>]*>(.*?)</script>', text, re.S)[1])
runtime = json.loads(re.search(r'const DATA=(.*?),\{tasks,groups\}=DATA;', text, re.S)[1])
assert data == runtime, 'Static and interactive datasets diverged'
tasks = {item['id']: item for item in data['tasks']}
assert len(tasks) == len(data['tasks']), 'Duplicate material ID'
assert len({g['id'] for g in data['groups']}) == len(data['groups'])
static = re.sub(r'<script\b[^>]*>.*?</script>', '', text, flags=re.S)
assert static.count('hidden data-task=') == len(tasks), 'Missing fallback rows'
assert static.count('data-open="false"') == len(data['groups']), 'Groups must start collapsed'
assert 'closed=new Set(groups.map(g=>g.id))' in text
assert '/Users/' not in text and 'file://' not in text, 'Local machine path in public page'
assert not re.search(r'https?://|fetch\s*\(|XMLHttpRequest|WebSocket', text), 'Unexpected external dependency'
assert 'robotcycles' not in tasks, 'Movement library was removed from scope'
assert tasks['music']['start'] is None and tasks['music']['end'] is None
assert all(t['group'] in {g['id'] for g in data['groups']} for t in tasks.values())
for task in tasks.values():
    if task['start'] is None:
        assert task['id'] == 'music'
        continue
    assert 0 <= task['start'] < task['end'] <= 93
    for dep in task['deps']:
        assert dep in tasks and tasks[dep]['end'] is not None
        assert tasks[dep]['end'] <= task['start'], (task['id'], dep)
refs = collections.Counter(n for t in tasks.values() for n in t['refs'])
refs.update(data['supportingWork']['refs'])
for excluded in data.get('excludedWork', []):
    refs.update(excluded['refs'])
assert set(refs) == set(range(1, 157)) and all(v == 1 for v in refs.values())
seen = set()
def visit(item):
    if item in seen:
        return
    seen.add(item)
    for dep in tasks[item]['deps']:
        visit(dep)
visit('handoff')
assert seen == set(tasks) - {'music'}, 'Unconnected active material'
assert (ROOT / 'docs/.nojekyll').is_file()
redirect = (ROOT / 'docs/index.html').read_text()
assert 'content="0; url=ProductionFlow/"' in redirect
assert 'href="ProductionFlow/"' in redirect
assert 'SIL OPEN FONT LICENSE' in (ROOT / 'docs/LICENSE-Manrope.txt').read_text()
print(json.dumps({'status': 'PASS', 'materials': len(tasks), 'groups': len(data['groups']),
                  'static_rows': len(tasks), 'accounted_csv_items': len(refs),
                  'standalone': True, 'music': 'inactive'}, ensure_ascii=False))
