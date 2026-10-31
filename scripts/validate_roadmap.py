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
assert data == json.loads((ROOT / 'Production/research_plan.json').read_text()), 'Published data diverged from editable plan'
tasks = {item['id']: item for item in data['tasks']}
assert len(tasks) == len(data['tasks']), 'Duplicate material ID'
assert len({g['id'] for g in data['groups']}) == len(data['groups'])
static = re.sub(r'<script\b[^>]*>.*?</script>', '', text, flags=re.S)
assert static.count('hidden data-task=') == len(tasks), 'Missing fallback rows'
assert static.count('data-open="false"') == len(data['groups']), 'Groups must start collapsed'
assert 'closed=new Set(groups.map(g=>g.id))' in text
assert '/Users/' not in text and 'file://' not in text, 'Local machine path in public page'
assert not re.search(r'https?://|fetch\s*\(|XMLHttpRequest|WebSocket', text), 'Unexpected external dependency'
assert not {'robotcycles', 'theme', 'physics'} & set(tasks), 'Production or showrunner work returned to research tasks'
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
for item in data['externalInputs']:
    refs.update(item['refs'])
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
inputs = {item['id']: item for item in data['externalInputs']}
assert inputs['showrunner-bible']['status'] == 'received'
evidence = {card['id'] for card in json.loads((ROOT / 'Sources/Design_Evidence.json').read_text())['cards']}
for task in tasks.values():
    assert task['status'] in ['planned', 'inactive']
    assert task['scope'] in ['research', 'inactive']
    assert all(i in inputs for i in task['inputDeps'])
    assert all(i in evidence for i in task['evidenceCards'])
    assert all((ROOT / f).is_file() for f in task['sourceFiles'])
    assert task['firstAction'] and task['readyWhen']
for noise in ['id="start"', 'function showStart()', '<h3>Первый шаг</h3>', '<h3>От команды</h3>', '<h3>Готово, когда</h3>', '<h3>Входные результаты</h3>']:
    assert noise not in text, 'Process metadata must stay out of the map interface'
assert "t.deps.length?'<h3>Зависит от</h3>'" in text
assert "next.length?'<h3>Нужно для</h3>'" in text
assert (ROOT / 'docs/.nojekyll').is_file()
assert not (ROOT / 'docs/index.html').exists(), 'Root redirect is not required'
assert 'SIL OPEN FONT LICENSE' in (ROOT / 'docs/LICENSE-Manrope.txt').read_text()
print(json.dumps({'status': 'PASS', 'materials': len(tasks), 'groups': len(data['groups']),
                  'static_rows': len(tasks), 'accounted_csv_items': len(refs),
                  'standalone': True, 'music': 'inactive'}, ensure_ascii=False))
