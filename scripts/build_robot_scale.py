#!/usr/bin/env python3
"""Build an explicitly provisional, metrically consistent robot comparison sheet."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'Production/Dashboard'; OUT=ROOT/'docs/World/robots/scale';OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((D/'robot_scale_study.json').read_text());rows=data['rows'];esc=html.escape
byid={a['id']:a for a in rows}
assert len(byid)==len(rows)
assert byid['don15']['height_cm'] < byid['don12']['height_cm']
assert byid['martin']['height_cm'] == byid['don12']['height_cm']
assert all(a['range_cm'][0] <= a['height_cm'] <= a['range_cm'][1] for a in rows)
S=1.8;W=2400;H=1320
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">ALIVE: рабочая шкала людей и роботов</title><desc id="desc">Все размеры предложены для дизайна. Силуэты условны. Обе строки используют одинаковую шкалу 1,8 единицы на сантиметр.</desc><rect width="2400" height="1320" fill="#101314"/><style>text{{font-family:Arial,sans-serif;fill:#edf0ea}}.grid{{stroke:#35403d;stroke-width:1}}.outline{{stroke:#d7fa65;stroke-width:2;fill:#28352d}}.human{{stroke:#a9bec6;stroke-width:2;fill:#28343b}}.ghost{{stroke:#c9a46c;stroke-width:2;stroke-dasharray:8 6;fill:#302b22}}</style><text x="60" y="48" font-size="32">ALIVE · РОБОТЫ И ЛЮДИ</text><text x="60" y="85" font-size="23" fill="#d7fa65">ВСЕ ЧИСЛА — ПРЕДЛОЖЕНИЕ ДЛЯ ДИЗАЙНА · НЕ РАЗМЕРЫ ИЗ РОМАНА</text>']
def silhouette(a):
 h=a['height_cm']*S;shape=a['shape'];cl='human' if a['kind']=='human' else 'ghost' if a['kind']=='envelope' else 'outline';w=(a.get('width_cm') or 48)*S
 # Keep wide equipment within its column: the diagram compares height; width is in the table.
 w=min(w,155)
 if shape=='human':
  return f'<g class="{cl}"><circle cx="0" cy="{-h*.91}" r="{h*.09}"/><path d="M{-h*.07},{-h*.8} L{-h*.14},{-h*.74} L{-h*.2},{-h*.40} L{-h*.15},{-h*.38} L{-h*.10},{-h*.64} L{-h*.10},{-h*.44} L{-h*.09},0 L{-h*.025},0 L0,{-h*.39} L{h*.025},0 L{h*.09},0 L{h*.10},{-h*.44} L{h*.10},{-h*.64} L{h*.15},{-h*.38} L{h*.2},{-h*.40} L{h*.14},{-h*.74} L{h*.07},{-h*.8} Z"/></g>'
 if shape.startswith('don'):
  return f'<g class="{cl}"><rect x="-25" y="{-h}" width="50" height="{h*.14}" rx="12"/><path d="M-30,{-h*.83} H30 L38,{-h*.47} H-38Z"/><path d="M-36,{-h*.77} L-52,{-h*.40} M36,{-h*.77} L52,{-h*.40}" stroke-width="15"/><path d="M-20,{-h*.47} L-24,-7 M20,{-h*.47} L24,-7" stroke-width="19"/><path d="M-37,-4H-10 M10,-4H37" stroke-width="8"/><circle cx="-11" cy="{-h*.94}" r="5"/><circle cx="11" cy="{-h*.94}" r="5"/></g>'
 if shape=='envelope':return f'<g class="ghost"><rect x="{-w/2}" y="{-h}" width="{w}" height="{h}"/><path d="M{-w/2},{-h} L{w/2},0 M{w/2},{-h} L{-w/2},0"/></g>'
 if shape=='dog':return f'<g class="outline"><rect x="-48" y="{-h*.65}" width="85" height="{h*.45}" rx="8"/><rect x="20" y="{-h}" width="28" height="{h*.43}" rx="7"/><circle cx="-30" cy="-9" r="9"/><circle cx="26" cy="-9" r="9"/><path d="M-48,{-h*.47}L-65,{-h*.7}"/></g>'
 if shape in ['sphere','cleaner']:
  return f'<g class="outline"><path d="M{-w/2},-8 Q{-w/2},{-h} 0,{-h} Q{w/2},{-h} {w/2},-8Z"/>'+ (f'<path d="M-20,{-h*.55} L-70,-13 M20,{-h*.55} L70,-13" stroke-width="6"/>' if shape=='sphere' else '')+'</g>'
 if shape=='loader':return f'<g class="outline"><rect x="-68" y="{-h*.48}" width="120" height="{h*.40}"/><rect x="40" y="{-h}" width="17" height="{h*.91}"/><path d="M57,-28H85" stroke-width="9"/><circle cx="-40" cy="-12" r="12"/><circle cx="32" cy="-12" r="12"/></g>'
 if shape=='delivery':return f'<g class="outline"><rect x="{-w/2}" y="{-h}" width="{w}" height="{h-18}" rx="8"/><path d="M{-w/2},{-h*.62}H{w/2} M{-w/2},{-h*.28}H{w/2}"/><circle cx="-45" cy="-10" r="10"/><circle cx="45" cy="-10" r="10"/></g>'
 body=f'<g class="outline"><rect x="{-w/2}" y="{-h*.75}" width="{w}" height="{h*.64}" rx="12"/><rect x="{-w*.28}" y="{-h}" width="{w*.56}" height="{h*.22}" rx="12"/><circle cx="{-w*.3}" cy="-10" r="10"/><circle cx="{w*.3}" cy="-10" r="10"/><path d="M{-w/2},{-h*.6}L{-w/2-20},{-h*.3} M{w/2},{-h*.6}L{w/2+20},{-h*.3}" stroke-width="10"/>'
 if shape=='gardener':body+=f'<path d="M{-w/2},{-h*.45}L{-w/2-32},{-h*.68} M{w/2},{-h*.45}L{w/2+32},{-h*.55}" stroke-width="8"/>'
 return body+'</g>'
lineups=[rows[:9],[dict(id='reference',title='Человек · ориентир',height_cm=180,width_cm=None,kind='human',shape='human')]+rows[9:]]
for idx,(baseline,line) in enumerate(zip([550,1160],lineups)):
 if idx:svg.append('<text x="60" y="666" font-size="26">СЛУЖЕБНЫЕ МАШИНЫ · ТА ЖЕ ШКАЛА ВЫСОТЫ</text>')
 for cm in range(0,251,50):
  y=baseline-cm*S;svg.append(f'<line class="grid" x1="95" x2="2350" y1="{y}" y2="{y}"/><text x="65" y="{y+7}" text-anchor="end" font-size="19">{cm}</text>')
 step=220 if idx else 245
 for i,a in enumerate(line):
  x=220+i*step;h=a['height_cm']*S
  svg.append(f'<g transform="translate({x},{baseline})">{silhouette(a)}</g><text x="{x}" y="{baseline-h-16}" text-anchor="middle" font-size="25">{a["height_cm"]} см</text>')
  words=a['title'].split(' · ')
  for k,w in enumerate(words):svg.append(f'<text x="{x}" y="{baseline+35+k*27}" text-anchor="middle" font-size="20">{esc(w)}</text>')
svg.append('<text x="60" y="1280" font-size="22">Пунктир: только пробный габарит оборудования. Ширина силуэтов условна; габариты основания — в таблице.</text></svg>')
(OUT/'scale-sheet.svg').write_text(''.join(svg))
source='https://raw.githubusercontent.com/esannikov/Alive/28693513d0bda68bd5351590f4569dd86b9b3ff8/Sources/ALIVE.pdf'
table=[]
for a in rows:
 size='—' if a['width_cm'] is None else f'{a["width_cm"]} × {a["length_cm"]}'
 links=' · '.join(f'<a href="{source}#page={p}" target="_blank" rel="noopener">{p}</a>' for p in a['pages'])
 table.append(f'<tr><th scope="row">{esc(a["title"])}</th><td>{a["height_cm"]}</td><td>{a["range_cm"][0]}–{a["range_cm"][1]}</td><td>{size}</td><td>{esc(a["basis"])}<br><small>PDF: {links}</small></td><td>{esc(a["rationale"])}</td></tr>')
alias=''.join(f'<li><strong>{esc(a["title"])}.</strong> {esc(a["note"])}</li>' for a in data['aliases'])
body=f'''<style>.scale-sheet{{width:100%;height:auto;border:1px solid #303735}}.scale-table-wrap{{overflow-x:auto}}.scale-table{{border-collapse:collapse;min-width:1050px;width:100%;font-size:14px}}.scale-table th,.scale-table td{{padding:14px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #303735}}.scale-table th{{font-weight:500}}.scale-table a{{text-decoration:underline}}.scale-notes{{max-width:900px;line-height:1.7}}.scale-notes li{{margin:12px 0}}.scale-note{{color:#d7fa65;margin:24px 0}}.scale-actions{{display:flex;gap:24px;flex-wrap:wrap;margin:24px 0}}details.scale-details{{margin-top:32px}}details.scale-details summary{{cursor:pointer;font-size:20px}}</style>
<div class="page-heading"><h1>Роботы и люди: масштаб</h1><p>Рабочий размерный лист · 24 октября 2026</p></div>
<p class="scale-note">Все численные размеры ниже — предложения для дизайна. В романе подтверждены относительные соотношения; измеренных моделей пока нет.</p>
<div class="scale-actions"><a href="scale-sheet.svg" target="_blank">Открыть лист крупно ↗</a><a href="scale-sheet.svg" download>Скачать SVG</a><a href="@ROOT@../ProductionFlow/#task=scale">Размеры в Flow ↗</a></div>
<img class="scale-sheet" src="scale-sheet.svg" width="2400" height="1320" alt="Сравнительная шкала предложенных высот людей и роботов. Все значения перечислены в таблице ниже.">
<section class="scale-notes"><h2>Первым — Лон</h2><p>Лон соединяет бытовую механику и характер: чинит комод, готовит, заботится о детях, свистит и шутит. Для первого концепта предлагается высота 145 см и основание 55 × 55 см. Белый корпус, маленькие чёрные колёса, неподвижная полоска рта, боковая щётка и экран под передней панелью взяты из романа.</p><p>Перед художественными вариантами нужно проверить четыре действия на одном простом макете: работа у поверхности 90 см, ремонт ящика, удержание ребёнка и разворот с руками в проходе. Высота 145 см сама по себе не доказывает устойчивость: нужны масса, центр тяжести и положение груза. Столешница 90 см и пробный проход 80 см здесь также приняты для проверки, а не взяты из текста.</p><p><strong>Обязательные связи:</strong> Дон-15 ниже Дона-12 (с. 108); садовник примерно по пояс Таис (с. 422). Мартин относится к Донам-12. Перепрограммирование не увеличивает Дона-15. Рост людей нельзя восстановить по поясным портретам без масштаба.</p><p>Доставщик выглядит крупным за счёт основания 120 × 180 см, а не обязательной гигантской высоты. Погрузчику отдельно нужны транспортная высота и зона подъёма; 360 см подъёма — пробная проверка пространства, не факт романа.</p></section>
<details class="scale-details" open><summary>Размеры и основания выбора</summary><p>Высота и диапазон в сантиметрах. Диапазон — варианты для проверки, не погрешность измерения. Основание: ширина × длина, без раскрытых манипуляторов.</p><div class="scale-table-wrap"><table class="scale-table"><thead><tr><th>Фигура / машина</th><th>Высота</th><th>Диапазон</th><th>Основание</th><th>Опора в романе</th><th>Почему предложен размер</th></tr></thead><tbody>{''.join(table)}</tbody></table></div></details>
<details class="scale-details"><summary>Названия, которые не означают отдельную модель</summary><ul class="scale-notes">{alias}</ul></details>
<div class="scale-actions"><a href="@ROOT@../ProductionFlow/#task=lon">Корпус Лона в Flow ↗</a><a href="@ROOT@../ProductionFlow/#task=robotfamilies">Семейства роботов ↗</a><a href="@ROOT@../ProductionFlow/#task=service">Служебные роботы ↗</a></div>'''
(D/'robot_scale_body.html').write_text(body)
print('Built provisional robot scale SVG and page body')
