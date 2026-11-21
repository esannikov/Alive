#!/usr/bin/env python3
"""Build human-readable work cards from the research plan and source index."""
from pathlib import Path
import json
from urllib.parse import quote
from validate import slug

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'Production/research_plan.json').read_text())
evidence = json.loads((ROOT / 'Sources/Design_Evidence.json').read_text())
cards = {c['id']: c for c in evidence['cards']}
by_id = {t['id']: t for t in data['tasks']}
inputs = {i['id']: i for i in data['externalInputs']}
lines = ['![ALIVE · РАБОЧИЕ КАРТОЧКИ](../assets/sections/team.svg)', '',
         '# ALIVE — карточки исследовательских заданий', '',
         '[Начало работы](Research_Start.md) · [Карта](https://esannikov.github.io/Alive/ProductionFlow/) · [Редактируемый план](research_plan.json)', '',
         f'Обновлено {data["review"]["date"]}. Для каждого задания указаны опоры, первый шаг, входы и критерий предъявления. Наличие опор не означает, что дизайн уже создан или принят. Страницы выбранного задания перечитываются перед его выполнением.', '']
for group in data['groups']:
    lines += ['## ' + group['title'], '']
    for task in [t for t in data['tasks'] if t['group'] == group['id']]:
        lines += ['### ' + task['title'], '', '**Результат:** ' + task['output'], '']
        if task['scope'] == 'inactive':
            continue
        lines += ['**Первый шаг:** ' + task['firstAction'], '']
        lines += ['**Опоры проекта:** ' + ' · '.join(f'[{Path(f).stem}](../{f})' for f in task['sourceFiles']), '']
        if len(task['evidenceCards']) > 20:
            lines += ['**Карточки источников:** весь [реестр опор](../Sources/Design_Evidence.json), по разделам итогового комплекта.', '']
        else:
            for cid in task['evidenceCards']:
                card = cards[cid]
                pages = ', '.join(map(str, card['pages']))
                lines.append(f'- [{cid} · {card["title"]}](../{card["file"]}#{quote(slug(card['title']))}): страницы романа {pages}.')
            lines += ['']
        if task['inputDeps']:
            lines += ['**От команды:** ' + '; '.join(inputs[i]['title'] + ' — ' + inputs[i]['label'].lower() for i in task['inputDeps']) + '.', '']
        lines += ['**Входные результаты:** ' + (', '.join(by_id[i]['title'] for i in task['deps']) or 'сбор опор можно начать по Библии и роману') + '.', '',
                  '**Готово, когда:** ' + task['readyWhen'], '']
        if task['openDecisions']:
            lines += ['**Уточнить для этого задания:** ' + ' '.join(task['openDecisions']), '']
        if 'sceneSource' in task:
            scene = task['sceneSource']
            lines += ['**Эпизод-кандидат:** страницы ' + ', '.join(map(str, scene['pages'])) + '; участники: ' + ', '.join(scene['participants']) + '; предметы: ' + ', '.join(scene['objects']) + '.', '']
        next_tasks = [t['title'] for t in data['tasks'] if task['id'] in t['deps']]
        lines += ['**Передаём дальше:** ' + (', '.join(next_tasks) or 'итоговая передача') + '.', '']
(ROOT / 'Production/Research_Workcards.md').write_text('\n'.join(lines).rstrip() + '\n')
print(f'Built {len(data["tasks"])} work cards.')
