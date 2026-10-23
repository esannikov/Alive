#!/usr/bin/env python3
"""Build the static ALIVE visual catalogue. Codes are assigned in the source registry only."""
from pathlib import Path
import collections
import hashlib
import html
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/World'
REGISTRY = ROOT / 'Production/Dashboard/asset_codes.json'
esc = lambda x: html.escape(str(x), quote=True)
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-5-5 5 5-5 5"/></svg>'
EXTERNAL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>'


def build():
    registry = json.loads(REGISTRY.read_text())
    config = json.loads((ROOT/'Production/Dashboard/objects.json').read_text())
    plan = json.loads((ROOT/'Production/research_plan.json').read_text())
    objects = {o['id']: o for o in config['objects']}
    tasks = {t['id']: t for t in plan['tasks']}
    assets = []
    assert len({a['code'] for a in registry['assets']}) == len(registry['assets'])
    (OUT/'previews').mkdir(parents=True, exist_ok=True)
    for record in registry['assets']:
        source = ROOT / record['source_file']
        assert source.is_file(), f'Missing source: {source}'
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256'], record['code']
        code = record['code']
        for suffix, width, quality in [('view', 1440, 85), ('thumb', 400, 78)]:
            target = OUT/'previews'/f'{code}-{suffix}.webp'
            if not target.exists():
                subprocess.run(['cwebp','-quiet','-q',str(quality),'-resize',str(width),'0',str(source),'-o',str(target)],check=True)
        series = record['series']
        assert series in {s['id'] for s in config['series']}, f'Unknown series: {series}'
        caption = re.sub(r'^(Усиленная версия|Мягкое смешение|Исходная Таис|Исходный образ|Таис с чертами Беллы):\s*', '', record['caption'])
        assets.append({'code':code,'object':record['object'],'title':caption,'series':series,
                       'preview':f'previews/{code}-view.webp','thumb':f'previews/{code}-thumb.webp',
                       'original':f'https://raw.githubusercontent.com/esannikov/Alive/{record["source_commit"]}/{record["source_file"]}',
                       'sourceFile':record['source_file'],
                       'status':'Поисковый вариант','kind':'appearance', 'taskIds':record['task_ids']})
    bycode = {a['code']: a for a in assets}
    data = {'objects':config['objects'],'assets':assets,'series':config['series'],
            'groups':plan['groups'],'tasks':[{'id':t['id'],'title':t['title'],'group':t['group'],'output':t['output']} for t in plan['tasks']]}
    (OUT/'data.js').write_text('window.ALIVE_WORLD='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')

    def asset_url(a):
        return f'characters/{a["object"]}/#{a["code"]}'

    def sidebar(prefix, active, category=''):
        primary = [('index.html','Обзор','overview'),('work.html','В разработке','work'),('catalog.html','Каталог','catalog')]
        nav = ''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if active==ident else '')+f'>{label}</a>' for url,label,ident in primary)
        groups = ''.join(f'<a class="category {"current" if g["id"]==category else ""}" href="{prefix}catalog.html#{g["id"]}">{esc(g["title"])}</a>' for g in plan['groups'])
        return f'''<aside class="sidebar" id="navigation"><a class="brand" href="{prefix}index.html">ALIVE<span class="brand-sub mono">Разработка мира</span></a><nav class="primary" aria-label="Основная навигация">{nav}</nav><nav class="categories" aria-label="Разделы мира">{groups}</nav><a class="flow-link mono" href="{prefix}../ProductionFlow/">ProductionFlow {EXTERNAL}</a></aside>'''

    def page(path, title, body, active='catalog', category='', obj=None):
        target = OUT/path
        target.parent.mkdir(parents=True,exist_ok=True)
        prefix = os.path.relpath(OUT,target.parent).replace('\\','/')
        prefix = '' if prefix=='.' else prefix+'/'
        # All authored body paths are relative to the World root.
        body = body.replace('@ROOT@',prefix)
        scripts = f'<script defer src="{prefix}data.js"></script><script defer src="{prefix}site.js" id="world-script"></script>'
        metadata = f'data-root="{prefix}" data-page="{esc(active)}"'+(f' data-object="{obj}"' if obj else '')
        target.write_text(f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{esc(title)} · ALIVE</title><meta name="description" content="Визуальная разработка ALIVE: персонажи, материалы и постоянные коды изображений."><link rel="stylesheet" href="{prefix}site.css"><link rel="preload" href="{prefix}fonts/Onest-Variable.ttf" as="font" type="font/ttf" crossorigin>{scripts}</head><body {metadata}><a class="skip-link" href="#main">К содержимому</a><header class="mobile-bar"><a href="{prefix}index.html">ALIVE</a><button id="menu-toggle" aria-controls="navigation" aria-expanded="false">Разделы</button></header><noscript><nav class="fallback-navigation"><a href="{prefix}index.html">Обзор</a><a href="{prefix}catalog.html">Каталог</a><a href="{prefix}../ProductionFlow/">План</a></nav></noscript>{sidebar(prefix,active,category)}<div class="page"><header class="utility"><div class="breadcrumbs"><a href="{prefix}index.html">ALIVE</a><span>/</span><span>{esc(title)}</span></div><form class="search-form" role="search" action="{prefix}search.html">{SEARCH}<input name="q" id="global-search" type="search" placeholder="Имя, код, предмет…" aria-label="Поиск по миру" autocomplete="off"><button type="submit" aria-label="Найти">{ARROW}</button></form></header><main id="main" tabindex="-1">{body}</main><footer class="page-footer mono"><span>ALIVE / визуальная разработка</span><a href="{prefix}../ProductionFlow/">Карта работ {EXTERNAL}</a></footer></div><div id="notice" class="notice mono" role="status" aria-live="polite"></div></body></html>''')

    def object_cards():
        cards = []
        for o in config['objects']:
            a=bycode[o['cover']]
            cards.append(f'''<article class="object-card"><a class="card-image" href="@ROOT@characters/{o['id']}/"><img src="@ROOT@{a['preview']}" width="1440" height="810" alt="{esc(o['title'])}: {esc(a['title'])}"></a><div class="card-body"><span class="code mono">{a['code']}</span><h3><a href="@ROOT@characters/{o['id']}/">{o['title']}</a></h3><p class="card-meta">{o['summary']}</p><a class="button primary-button" href="@ROOT@characters/{o['id']}/">Открыть галерею {ARROW}</a></div></article>''')
        cards.append('''<article class="object-card pending"><div class="ship-placeholder"><span class="mono">Галерея появится здесь</span></div><div class="card-body"><span class="code mono">В работе</span><h3>Корабль</h3><p class="card-meta">Материалы готовятся к подключению</p><span class="button unavailable" aria-disabled="true">Галерея пока недоступна</span></div></article>''')
        return '<div class="object-grid">'+''.join(cards)+'</div>'

    descriptions={
        'people':'Внешность, модельные листы, костюмы и состояния', 'style':'Стиль, пропорции, материалы и свет',
        'robots':'Лон, Доны, служебные модели', 'station':'Корпус, уровни, макет и маршруты',
        'world':'Быт, сообщества и системы станции', 'locations':'Подробные комплекты помещений',
        'props':'Транспорт, оборудование и личные вещи', 'screens':'Устройства, интерфейсы и доступ',
        'signs':'Эмблемы, надписи и навигация', 'life':'Проявления, состояния и существа',
        'sound':'Звуковые и речевые признаки', 'delivery':'Комплекты эпизодов и общий атлас'}
    rows=''.join(f'''<a class="catalog-row {"available" if g['id']=='people' else "planned"}" href="@ROOT@catalog.html#{g['id']}"><span class="row-title">{g['title']}</span><span class="row-description">{descriptions[g['id']]}</span><span class="row-state mono">{"Есть материалы" if g['id']=='people' else "Запланировано"}</span>{ARROW}</a>''' for g in plan['groups'])
    page('index.html','Обзор',f'''<div class="page-heading"><h1>Разработка ALIVE</h1><p>Персонажи, пространства и предметы мира.</p></div><section aria-labelledby="current-heading"><h2 id="current-heading">Сейчас в разработке</h2>{object_cards()}</section><section class="catalog-section" aria-labelledby="catalog-heading"><div class="section-heading"><h2 id="catalog-heading">Полный состав разработки</h2><a class="quiet-link mono" href="@ROOT@catalog.html">Открыть каталог {ARROW}</a></div><div class="catalog-list">{rows}</div></section>''',active='overview')
    page('work.html','В разработке',f'''<div class="page-heading"><h1>В разработке</h1><p>Текущие подборки и материалы, которые готовятся.</p></div><section aria-label="Текущие работы"><h2 class="sr-only">Материалы</h2>{object_cards()}</section>''',active='work')
    catalog=[]
    for g in plan['groups']:
        members=[t for t in plan['tasks'] if t['group']==g['id']]
        entries=[]
        for t in members:
            connected=[o for o in config['objects'] if t['id'] in o['task_ids']]
            links=''.join(f'<a class="inline-object" href="@ROOT@characters/{o["id"]}/">{o["title"]} {ARROW}</a>' for o in connected)
            entries.append(f'''<li class="task-line"><div><span>{esc(t['title'])}</span><span class="task-note mono">{"Есть связанные материалы" if connected else "Неактивно" if t['scope']=='inactive' else "Запланировано"}</span></div><div class="task-links">{links}<a class="plan-link mono" href="@ROOT@../ProductionFlow/#task={t['id']}">План {EXTERNAL}</a></div></li>''')
        catalog.append(f'''<details class="catalog-group" id="{g['id']}" {'open' if g['id']=='people' else ''}><summary><span>{g['title']}</span><span class="mono">{len(members)} материалов</span>{ARROW}</summary><ul>{''.join(entries)}</ul></details>''')
    page('catalog.html','Каталог',f'''<div class="page-heading"><h1>Каталог мира</h1><p>Все направления разработки — от первых образов до готовых комплектов.</p></div><div class="catalog-groups">{''.join(catalog)}</div>''')
    for o in config['objects']:
        aa=[a for a in assets if a['object']==o['id']];current=[a for a in aa if a['series']=='current'];first=bycode[o['cover']]
        tabs=''.join(f'<button class="derivative {"active" if d["id"]=="appearance" else ""}"'+(' aria-current="page"' if d['id']=='appearance' else ' disabled title="Материалы ещё не подготовлены"')+f'>{d["title"]}{f" <span class=mono>{len(current)}</span>" if d["id"]=="appearance" else ""}</button>' for d in config['derivatives'])
        series=[s for s in config['series'] if any(a['series']==s['id'] for a in aa)]
        options=''.join(f'<option value="{s["id"]}">{s["title"]} · {sum(a["series"]==s["id"] for a in aa)}</option>' for s in series)+'<option value="all">Все серии</option>'
        grid=''.join(f'''<figure class="asset-tile" id="{a['code']}" data-series="{a['series']}" data-code="{a['code']}"><a href="#{a['code']}" class="thumb-link" aria-label="{a['code']}: {esc(a['title'])}"><img src="@ROOT@{a['thumb']}" alt="{esc(a['title'])}" width="400" height="225" loading="lazy"></a><figcaption><a href="@ROOT@{a['original']}" class="asset-code mono">{a['code']}</a><span>{esc(a['title'])}</span></figcaption></figure>''' for a in aa)
        page(f'characters/{o["id"]}/index.html',o['title'],f'''<div class="page-heading object-heading"><div><h1>{o['title']}</h1><p>Визуальная разработка</p></div><a class="quiet-link" href="reference.html">Справка {EXTERNAL}</a></div><nav class="derivatives" aria-label="Производные персонажа">{tabs}</nav><div class="gallery-toolbar"><label class="select-label"><span class="sr-only">Серия изображений</span><select id="series-select">{options}</select></label><span class="mono gallery-count" id="gallery-count">{len(current)} вариантов</span><button id="compare-toggle" class="quiet-button js-only" aria-pressed="false">Сравнить</button></div><section class="viewer" id="viewer" aria-label="Просмотр изображения"><a class="hero-link" id="hero-link" href="@ROOT@{first['original']}"><img id="hero-image" src="@ROOT@{first['preview']}" alt="{esc(first['title'])}" width="1440" height="810" fetchpriority="high"></a><div class="viewer-caption"><div><strong id="hero-code" class="mono">{first['code']}</strong><span id="hero-title">{esc(first['title'])}</span></div><div class="viewer-step js-only"><button id="previous-image" aria-label="Предыдущее изображение">{ARROW}</button><button id="next-image" aria-label="Следующее изображение">{ARROW}</button></div></div><div class="viewer-actions"><a id="original-link" href="@ROOT@{first['original']}" target="_blank" rel="noopener">Оригинал {EXTERNAL}</a><button class="js-only" id="copy-code">Копировать код</button><button class="js-only" id="copy-link">Копировать ссылку</button><button class="js-only" id="enlarge">Развернуть {EXTERNAL}</button><a href="#gallery">Все варианты {ARROW}</a></div></section><section id="compare-panel" class="compare-panel" aria-label="Сравнение вариантов" hidden><div><label for="compare-left">Первый вариант</label><select id="compare-left"></select><img id="compare-image-left" alt=""><span id="compare-caption-left" class="mono"></span></div><div><label for="compare-right">Второй вариант</label><select id="compare-right"></select><img id="compare-image-right" alt=""><span id="compare-caption-right" class="mono"></span></div></section><div class="gallery-grid" id="gallery">{grid}</div><noscript><p class="noscript-note">Все серии показаны ниже. Для оригинала откройте код под изображением.</p></noscript><dialog id="image-dialog"><button id="close-image" aria-label="Закрыть изображение">Закрыть</button><img id="dialog-image" alt=""><div class="mono" id="dialog-caption"></div></dialog>''',category='people',obj=o['id'])
        source_commit=registry['assets'][0]['source_commit']
        pdf=f'https://raw.githubusercontent.com/esannikov/Alive/{source_commit}/Sources/ALIVE.pdf'
        pages=' · '.join(f'<a href="{pdf}#page={n}" target="_blank" rel="noopener">{n}</a>' for n in o['source_pages'])
        flow=''.join(f'<a class="reference-link" href="@ROOT@../ProductionFlow/#task={id}"><span>{tasks[id]["title"]}</span>{ARROW}</a>' for id in o['task_ids'])
        page(f'characters/{o["id"]}/reference.html',f'{o["title"]} · справка',f'''<div class="page-heading"><a class="back-link mono" href="./">К галерее {ARROW}</a><h1>{o['title']}: справка</h1></div><div class="reference-content"><section><h2>Опоры в романе</h2><p>{esc(o['source_summary'])}</p><p class="source-pages">Страницы PDF: {pages}</p><p class="subtle">{esc(o['source_note'])}</p><a class="quiet-link" href="https://github.com/esannikov/Alive/blob/{source_commit}/Bible/Characters.md" target="_blank" rel="noopener">Описание персонажей · {o['evidence']} {EXTERNAL}</a></section><section><h2>В ProductionFlow</h2>{flow}</section><section><h2>Как читать материалы</h2><p>Это поисковые варианты. Выбранная внешность, подробный модельный лист и принятый комплект — отдельные результаты. Коды изображений сохраняются при перемещении между подборками.</p></section></div>''',category='people')
    page('search.html','Поиск', '''<div class="page-heading"><h1>Поиск по миру</h1><p>Имя, постоянный код, предмет или нужный материал.</p></div><p class="mono" id="search-summary">Введите запрос в строке поиска.</p><div id="search-results" class="search-results"></div><noscript><p>Для поиска нужен JavaScript. <a href="catalog.html">Открыть полный каталог</a>.</p></noscript>''',active='search')
    mapping={}
    for t in plan['tasks']:
        related=[{'title':o['title'],'url':f'../World/characters/{o["id"]}/'} for o in config['objects'] if t['id'] in o['task_ids']]
        if related:mapping[t['id']]=related
    flowfile=ROOT/'docs/ProductionFlow/index.html';flowtext=flowfile.read_text()
    payload=json.dumps(mapping,ensure_ascii=False,separators=(',',':'))
    if 'const WORLD_LINKS=' in flowtext:
        flowtext=re.sub(r'const WORLD_LINKS=.*?;\n',lambda _:f'const WORLD_LINKS={payload};\n',flowtext,count=1)
    else:raise RuntimeError('ProductionFlow integration marker missing; apply the integration patch once.')
    flowfile.write_text(flowtext)
    print(json.dumps({'status':'BUILT','images':len(assets),'objects':len(objects),'tasks':len(tasks),'pages':8},ensure_ascii=False))

if __name__=='__main__':build()
