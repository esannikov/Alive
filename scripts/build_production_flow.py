#!/usr/bin/env python3
"""Refresh the standalone map from the editable research plan (stdlib only)."""
from pathlib import Path
import datetime
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / 'docs/ProductionFlow/index.html'
data = json.loads((ROOT / 'Production/research_plan.json').read_text())
tasks, groups = data['tasks'], data['groups']
text = target.read_text()
payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
assert '</script' not in payload.lower()
text, n = re.subn(r'(<script id="plan-data" type="application/json">).*?(</script>)',
                  lambda m: m[1] + payload + m[2], text, flags=re.S)
assert n == 1
text, n = re.subn(r'const DATA=.*?,\{tasks,groups\}=DATA;',
                  lambda m: 'const DATA=' + payload + ',{tasks,groups}=DATA;', text, count=1, flags=re.S)
assert n == 1
esc = lambda value: html.escape(str(value), quote=True)
count = len(tasks)
nav = f'<button class="groupnav" type="button" data-filter="all" aria-pressed="true"><span class="dot" style="--c:#4169dc"></span><span class="label">Все материалы</span><span class="count">{count}</span></button>'
for group in groups:
    members = [t for t in tasks if t['group'] == group['id']]
    nav += f'<button class="groupnav" type="button" data-filter="{group["id"]}" aria-pressed="false"><span class="dot" style="--c:{group["color"]}"></span><span class="label">{esc(group["title"])}</span><span class="count">{len(members)}</span></button>'
a = text.index('<div id="nav">') + len('<div id="nav">')
b = text.index('</div><div class="navfoot">', a)
text = text[:a] + nav + text[b:]
a = text.index('<div id="sheet" class="sheet">') + len('<div id="sheet" class="sheet">')
b = text.index('</div></div></section>', a)
old = text[a:b]
board = old[:old.index('<div class="grouprow"')]
start = datetime.date(2026, 10, 19)
date = lambda offset: (start + datetime.timedelta(days=offset)).strftime('%d.%m')
for group in groups:
    members = [t for t in tasks if t['group'] == group['id']]
    active = [t for t in members if t['start'] is not None]
    begin, end = min(t['start'] for t in active), max(t['end'] for t in active)
    board += f'<div class="grouprow" data-group="{group["id"]}" data-open="false" style="--c:{group["color"]}"><button class="rowlabel" type="button" data-toggle="{group["id"]}" aria-expanded="false"><svg class="icon chevron" aria-hidden="true" viewBox="0 0 24 24"><path d="m9 5 7 7-7 7"/></svg><span class="dot"></span><span class="name">{esc(group["title"])}</span><span class="count">{len(members)}</span></button><div class="lane"><span class="summarybar" style="left:{begin/93*100}%;width:{(end-begin)/93*100}%"></span></div></div>'
    for task in members:
        inactive = task['start'] is None
        board += f'<div class="taskrow {"inactive" if inactive else ""}" hidden data-task="{task["id"]}" style="--c:{group["color"]}"><button class="rowlabel" type="button" data-select="{task["id"]}" aria-label="{esc(task["title"])}" aria-pressed="false"><span class="mini"></span><span class="name">{esc(task["title"])}</span></button><div class="lane">'
        if inactive:
            board += '<span class="off-label">Неактивно</span>'
        else:
            board += f'<button class="bar" type="button" data-select="{task["id"]}" aria-label="{esc(task["title"])}; {date(task["start"])} — {date(task["end"]-1)}" style="left:{task["start"]/93*100}%;width:{(task["end"]-task["start"])/93*100}%"><span class="bartext">{esc(task["title"])}</span></button>'
        board += '</div></div>'
board += f'<svg class="arrows" id="arrows" aria-hidden="true" height="{43*len(groups)}"></svg>'
text = text[:a] + board + text[b:]
text = re.sub(r'<span id="visiblecount">.*?</span>', f'<span id="visiblecount">{count} материалов</span>', text, count=1)
target.write_text(text)
print(f'Built {count} materials in {len(groups)} groups.')
