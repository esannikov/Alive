#!/usr/bin/env python3
"""Build the current character-scale atlas at the existing robots/scale URL."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'Production/Dashboard';OUT=ROOT/'docs/World/robots/scale'
data=json.loads((D/'character_scale_atlas.json').read_text())
assert len(data['items'])==data['physical_figures']==78
assert len({x['id'] for x in data['items']})==78
assert data['raster_size']==[9000,9000]
notes=(D/'character_scale_notes.html').read_text()
layouts=[('01-height-lineup-9k','По росту','Общая шкала роста персонажей и роботов'),('02-families-9k','По группам','Семьи, группы и поколения ALIVE'),('03-modules-9k','Сменные фигуры','Модульные карточки всех фигур')]
for name,_,_ in layouts:
 for ext in ['.png','.svg','-preview.png']:assert (OUT/(name+ext)).is_file(),name+ext
nav=''.join(f'<a href="{name}.png" data-atlas-layout="{name}" data-alt="{alt}"'+(' aria-current="true"' if i==0 else '')+f'>{i+1:02} · {label}</a>' for i,(name,label,alt) in enumerate(layouts))
v=lambda name:hashlib.sha256((OUT/name).read_bytes()).hexdigest()[:12]
body=f'''<link rel="stylesheet" href="atlas.css?v={v('atlas.css')}">
<div class="page-heading"><h1>Персонажи и роботы: масштаб</h1><p>Три схемы · 78 фигур и 2 нематериальных образа · 9000 × 9000 px</p></div>
<p class="atlas-size-note">Числа в сантиметрах — рабочие оценки для сопоставления. Значок книги отмечает описание из романа; цитаты и страницы приведены под схемой. Контуры обозначают ещё не разработанные образы, их U-коды сохранены для замены.</p>
<nav class="atlas-controls atlas-layouts" aria-label="Выбор схемы">{nav}</nav>
<div class="atlas-controls"><button id="atlas-fit" type="button" data-atlas-js hidden>Весь лист</button><button id="atlas-actual" type="button" data-atlas-js hidden>100%</button><label data-atlas-js hidden>Масштаб <input id="atlas-zoom" type="range" min="5" max="150" step="1" value="15" aria-label="Масштаб схемы"></label><output id="atlas-percent" for="atlas-zoom" data-atlas-js hidden></output><a id="atlas-png" href="01-height-lineup-9k.png" download>PNG 9K ↓</a><a id="atlas-svg" href="01-height-lineup-9k.svg" download>SVG ↓</a><a href="#sources">Опоры в романе ↓</a></div>
<div class="atlas-viewer" id="atlas-viewer" tabindex="0" role="region" aria-label="Схема со свободной прокруткой"><img id="atlas-poster" src="01-height-lineup-9k-preview.png" width="1800" height="1800" alt="Общая шкала роста персонажей и роботов"></div>
<p class="atlas-hint"><span id="atlas-status" role="status">Превью · при увеличении загружается оригинал 9K</span>. Перетаскивайте лист мышью или прокручивайте. На телефоне используйте прокрутку и регулятор масштаба.</p>
<div class="atlas-sources">{notes}</div>
<script defer src="atlas.js?v={v('atlas.js')}"></script>'''
(D/'robot_scale_body.html').write_text(body)
print('Built current 3-layout 9K character atlas; 78 figures and source notes')
