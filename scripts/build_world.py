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
variant_count = lambda n: str(n)+' '+('вариант' if n%10==1 and n%100!=11 else 'варианта' if n%10 in [2,3,4] and n%100 not in [12,13,14] else 'вариантов')
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-5-5 5 5-5 5"/></svg>'
EXTERNAL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>'


def build():
    registry = json.loads(REGISTRY.read_text())
    config = json.loads((ROOT/'Production/Dashboard/objects.json').read_text())
    plan = json.loads((ROOT/'Production/research_plan.json').read_text())
    studies = config.get('studies', [])
    objects = {o['id']: o for o in config['objects']}
    tasks = {t['id']: t for t in plan['tasks']}
    object_path = lambda o: o.get('path', f'characters/{o["id"]}')
    assets = []
    assert len({a['code'] for a in registry['assets']}) == len(registry['assets'])
    (OUT/'previews').mkdir(parents=True, exist_ok=True)
    for record in registry['assets']:
        source = ROOT / record['source_file']
        assert source.is_file(), f'Missing source: {source}'
        assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256'], record['code']
        code = record['code']
        for suffix, width, quality in [('view', 1440, 85), ('thumb-hq', 640, 92)]:
            target = OUT/'previews'/f'{code}-{suffix}.webp'
            if not target.exists():
                subprocess.run(['cwebp','-quiet','-q',str(quality),'-resize',str(width),'0',str(source),'-o',str(target)],check=True)
        series = record['series']
        assert series in {s['id'] for s in config['series']}, f'Unknown series: {series}'
        caption = re.sub(r'^(Усиленная версия|Мягкое смешение|Исходная Таис|Исходный образ|Таис с чертами Беллы):\s*', '', record['caption'])
        assets.append({'code':code,'object':record['object'],'title':caption,'series':series,
                       'preview':f'previews/{code}-view.webp','thumb':f'previews/{code}-thumb-hq.webp',
                       'original':f'https://raw.githubusercontent.com/esannikov/Alive/{record["source_commit"]}/{record["source_file"]}',
                       'sourceFile':record['source_file'], 'display':os.path.relpath(source,OUT).replace('\\','/'), 'page':object_path(objects[record['object']])+'/',
                       'status':'Поисковый вариант','kind':record.get('kind','appearance'), 'taskIds':record['task_ids'], 'archived':record.get('visibility')=='archived', 'previousObjects':record.get('previous_objects',[]), 'additionalObjects':record.get('additional_objects',[])})
    bycode = {a['code']: a for a in assets}
    data = {'objects':config['objects'],'assets':assets,'series':config['series'],
            'deletedCodes':registry.get('deleted_codes',[]),'groups':plan['groups'],'tasks':[{'id':t['id'],'title':t['title'],'group':t['group'],'output':t['output']} for t in plan['tasks']]}
    comments_file = ROOT/'Production/Dashboard/comments.json'
    if comments_file.exists():
        comments = json.loads(comments_file.read_text())
        if comments.get('enabled'):
            assert comments.get('repoId') and comments.get('categoryId'), 'Giscus IDs are required before activation'
            assert comments['mapping'] == 'pathname' and comments['strict'] == '1'
        theme_hash = hashlib.sha256((OUT/'giscus-compact.css').read_bytes()).hexdigest()[:12]
        data['comments'] = {**comments, 'voteTheme': 'https://esannikov.github.io/Alive/World/giscus-votes.css?v='+hashlib.sha256((OUT/'giscus-votes.css').read_bytes()).hexdigest()[:12], 'theme': f'https://esannikov.github.io/Alive/World/giscus-compact.css?v={theme_hash}'}
    (OUT/'data.js').write_text('window.ALIVE_WORLD='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')

    def asset_url(a):
        return f'{object_path(objects[a["object"]])}/#{a["code"]}'

    def sidebar(prefix, active, category=''):
        primary = [('index.html','Обзор','overview'),('work.html','В разработке','work'),('catalog.html','Каталог','catalog')]
        nav = ''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if active==ident else '')+f'>{label}</a>' for url,label,ident in primary)
        groups = ''.join(f'<a class="category {"current" if g["id"]==category else ""}" href="{prefix}catalog.html#{g["id"]}">{esc(g["title"])}</a>' for g in plan['groups'])
        return f'''<aside class="sidebar" id="navigation"><a class="brand" href="{prefix}index.html">ALIVE<span class="brand-sub mono">Разработка мира</span></a><nav class="primary" aria-label="Основная навигация">{nav}</nav><nav class="categories" aria-label="Разделы мира">{groups}</nav><a class="flow-link mono" href="{prefix}../ProductionFlow/">ProductionFlow {EXTERNAL}</a></aside>'''

    def asset_version(name):
        digest=hashlib.sha256((OUT/name).read_bytes()).hexdigest()[:12]
        return f'{name}?v={digest}'

    comment_pages = []

    def page(path, title, body, active='catalog', category='', obj=None):
        canonical = path.removesuffix('index.html') if path.endswith('index.html') else path
        comment_pages.append({'term': 'Alive/World/' + re.sub(r'\.\w+$', '', canonical), 'page': canonical, 'title': title, 'variantCodes': [a['code'] for a in assets if obj and (a['object']==obj or obj in a.get('additionalObjects',[]))]})
        target = OUT/path
        target.parent.mkdir(parents=True,exist_ok=True)
        prefix = os.path.relpath(OUT,target.parent).replace('\\','/')
        prefix = '' if prefix=='.' else prefix+'/'
        # All authored body paths are relative to the World root.
        body = body.replace('@ROOT@',prefix)
        scripts = f'<script defer src="{prefix}{asset_version("data.js")}"></script><script defer src="{prefix}{asset_version("site.js")}" id="world-script"></script><script defer src="{prefix}{asset_version('votes.js')}"></script>'
        metadata = f'data-root="{prefix}" data-page="{esc(active)}"'+(f' data-object="{obj}"' if obj else '')
        target.write_text(f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{esc(title)} · ALIVE</title><meta name="description" content="Визуальная разработка ALIVE: персонажи, корабль, материалы и постоянные коды изображений."><link rel="stylesheet" href="{prefix}{asset_version("site.css")}"><link rel="preload" href="{prefix}fonts/Onest-Variable.ttf" as="font" type="font/ttf" crossorigin>{scripts}</head><body {metadata}><a class="skip-link" href="#main">К содержимому</a><header class="mobile-bar"><a href="{prefix}index.html">ALIVE</a><button id="menu-toggle" aria-controls="navigation" aria-expanded="false">Разделы</button></header><noscript><nav class="fallback-navigation"><a href="{prefix}index.html">Обзор</a><a href="{prefix}catalog.html">Каталог</a><a href="{prefix}../ProductionFlow/">План</a></nav></noscript>{sidebar(prefix,active,category)}<div class="page"><header class="utility"><div class="breadcrumbs"><a href="{prefix}index.html">ALIVE</a><span>/</span><span>{esc(title)}</span></div><form class="search-form" role="search" action="{prefix}search.html">{SEARCH}<input name="q" id="global-search" type="search" placeholder="Имя, код, предмет…" aria-label="Поиск по миру" autocomplete="off"><button type="submit" aria-label="Найти">{ARROW}</button></form></header><main id="main" tabindex="-1">{body}</main><footer class="page-footer mono"><span>ALIVE / визуальная разработка</span><a href="{prefix}../ProductionFlow/">Карта работ {EXTERNAL}</a></footer></div><div id="notice" class="notice mono" role="status" aria-live="polite"></div></body></html>''')

    def discussion_summary(path):
        return f'<a class="card-discussion" data-discussion-summary="{esc(path)}/" href="@ROOT@{esc(path)}/#comments" aria-label="Открыть комментарии"><span class="card-discussion-placeholder">Комментарии…</span></a>'

    def object_cards():
        cards = []
        for o in config['objects']:
            a=bycode[o['cover']]
            cards.append(f'''<article class="object-card" data-kind="{o.get('kind','character')}" data-filter-kind="{'locations' if o.get('kind') == 'location' else 'ship' if o.get('kind') == 'ship' else 'robots' if o.get('group') == 'robots' else 'people'}"><a class="card-image" href="@ROOT@{object_path(o)}/"><img src="@ROOT@{a['preview']}" width="1440" height="810" alt="{esc(o['title'])}: {esc(a['title'])}"></a><div class="card-body"><span class="code mono">{a['code']}</span><h3><a href="@ROOT@{object_path(o)}/">{o['title']}</a></h3><p class="card-meta">{o['summary']}</p>{discussion_summary(object_path(o))}<a class="button primary-button" href="@ROOT@{object_path(o)}/">Открыть галерею {ARROW}</a></div></article>''')
        if 'moag' not in objects: cards.append('''<article class="object-card pending" data-filter-kind="ship"><div class="ship-placeholder"><span class="mono">Галерея появится здесь</span></div><div class="card-body"><span class="code mono">В работе</span><h3>Корабль</h3><p class="card-meta">Материалы готовятся к подключению</p><span class="button unavailable" aria-disabled="true">Галерея пока недоступна</span></div></article>''')
        for study in studies:
            cards.append(f'''<article class="object-card" data-filter-kind="{esc(study['group'])}"><a class="card-image" href="@ROOT@{study['path']}/"><img src="@ROOT@{study['image']}" width="1440" height="810" alt="{esc(study['title'])}"></a><div class="card-body"><span class="code mono">{esc(study.get('label','Размерная гипотеза'))}</span><h3>{esc(study['title'])}</h3><p class="card-meta">{esc(study['summary'])}</p>{discussion_summary(study['path'])}<a class="button primary-button" href="@ROOT@{study['path']}/">{esc(study.get('button_label','Открыть лист'))} {ARROW}</a></div></article>''')
        return '<div class="object-grid">'+''.join(cards)+'</div>'

    page('index.html','Обзор',f'''<div class="page-heading"><h1>Разработка ALIVE</h1><p>Персонажи, пространства и предметы мира.</p></div><section aria-labelledby="current-heading"><h2 id="current-heading">Сейчас в разработке</h2><div class="home-controls js-only" id="home-controls"><div class="home-filters" role="group" aria-label="Фильтр галерей"><button type="button" data-filter="all" aria-pressed="true">Все</button><button type="button" data-filter="people" aria-pressed="false">Люди</button><button type="button" data-filter="robots" aria-pressed="false">Роботы</button><button type="button" data-filter="ship" aria-pressed="false">Корабль</button><button type="button" data-filter="locations" aria-pressed="false">Пространства</button></div><label>Порядок <select id="home-sort"><option value="default">По порядку</option><option value="activity">Недавно обсуждали</option></select></label><button id="home-resort" type="button" class="quiet-button" hidden>Обновить порядок</button></div>{object_cards()}</section><section id="recent-comments" class="recent-comments" aria-labelledby="recent-comments-heading"><div class="section-heading"><h2 id="recent-comments-heading">Последние комментарии</h2><button id="recent-comments-retry" class="quiet-button" hidden>Повторить</button></div><p id="recent-comments-status" class="recent-comments-status" role="status">Загрузка комментариев…</p><ol id="recent-comments-list" class="recent-comments-list" hidden></ol><a class="quiet-link recent-comments-all" href="https://github.com/esannikov/Alive/discussions?discussions_q=">Все обсуждения {EXTERNAL}</a><noscript><p>Комментарии доступны по ссылке «Все обсуждения».</p></noscript></section>''',active='overview')
    page('work.html','В разработке',f'''<div class="page-heading"><h1>В разработке</h1><p>Текущие подборки и материалы, которые готовятся.</p></div><section aria-label="Текущие работы"><h2 class="sr-only">Материалы</h2>{object_cards()}</section>''',active='work')
    catalog=[]
    for g in plan['groups']:
        members=[t for t in plan['tasks'] if t['group']==g['id']]
        entries=[]
        for t in members:
            connected=[o for o in config['objects']+studies if t['id'] in o['task_ids']]
            links=''.join(f'<a class="inline-object" href="@ROOT@{object_path(o)}/">{o["title"]} {ARROW}</a>' for o in connected)
            entries.append(f'''<li class="task-line"><div><span>{esc(t['title'])}</span><span class="task-note mono">{"Есть связанные материалы" if connected else "Неактивно" if t['scope']=='inactive' else "Запланировано"}</span></div><div class="task-links">{links}<a class="plan-link mono" href="@ROOT@../ProductionFlow/#task={t['id']}">План {EXTERNAL}</a></div></li>''')
        catalog.append(f'''<details class="catalog-group" id="{g['id']}" {'open' if g['id']=='people' else ''}><summary><span>{g['title']}</span><span class="mono">{len(members)} материалов</span>{ARROW}</summary><ul>{''.join(entries)}</ul></details>''')
    page('catalog.html','Каталог',f'''<div class="page-heading"><h1>Каталог мира</h1><p>Все направления разработки — от первых образов до готовых комплектов.</p></div><div class="catalog-groups">{''.join(catalog)}</div>''')
    for o in config['objects']:
        aa=[a for a in assets if (a['object']==o['id'] or o['id'] in a.get('additionalObjects',[])) and not a['archived']]
        order=o.get('gallery_order',[])
        aa.sort(key=lambda a: order.index(a['code']) if a['code'] in order else len(order))
        current=[a for a in aa if a['series']==o['default_series']];first=bycode[o['cover']]
        tab_count=len({a['series'] for a in aa}) if o.get('kind')=='ship' else len(current)
        tabs=''.join(f'<button class="derivative {"active" if d["id"]=="appearance" else ""}"'+(' aria-current="page"' if d['id']=='appearance' else ' aria-disabled="true" data-pending title="Пока не подготовлено"')+f'>{d["title"]}{f" <span class=mono>{tab_count}</span>" if d["id"]=="appearance" else ""}</button>' for d in o.get('derivatives',config['derivatives']))
        series=[s for s in config['series'] if any(a['series']==s['id'] for a in aa)]
        options=''.join(f'<option value="{s["id"]}">{s["title"]} · {sum(a["series"]==s["id"] for a in aa)}</option>' for s in series)+('<option value="all">Все варианты</option>' if o.get('kind')=='ship' else '<option value="all">Все серии</option>')
        is_ship=o.get('kind')=='ship'
        variant_note='<p id="variant-note" class="variant-note"></p>' if o.get('variant_notes') else ''
        grid=''.join(f'''<figure class="asset-tile" id="{a['code']}" data-series="{a['series']}" data-code="{a['code']}"><a href="#{a['code']}" class="thumb-link" aria-label="{a['code']}: {esc(a['title'])}"><img src="@ROOT@{a['thumb']}" alt="{esc(a['title'])}" width="400" height="225" loading="lazy"></a><figcaption><a href="{a['original']}" class="asset-code mono">{a['code']}</a><span>{esc(a['title'])}</span></figcaption></figure>''' for a in aa)
        if is_ship:
            groups=[]
            for series_item in series:
                pair=[a for a in aa if a['series']==series_item['id']]
                cover=pair[0]
                view_links=''.join(f'<a class="ship-view-link" href="{a["original"]}" data-code="{a["code"]}"'+(f' id="{a["code"]}"' if i else '')+f'>{esc(a["title"].split("·")[-1].strip().capitalize())}</a>' for i,a in enumerate(pair))
                groups.append(f'<figure class="asset-tile ship-variant" id="{cover["code"]}" data-series="{cover["series"]}" data-code="{cover["code"]}"><a href="{cover["original"]}" data-code="{cover["code"]}" class="thumb-link" aria-label="{esc(series_item["title"])}"><img src="@ROOT@{cover["thumb"]}" alt="{esc(series_item["title"])}" width="640" height="290" loading="lazy"></a><figcaption><span class="variant-name">{esc(series_item["title"])}</span><div class="variant-views">{view_links}</div></figcaption></figure>')
            grid=''.join(groups)
            toolbar=f'<div class="view-choices js-only" role="group" aria-label="Ракурс выбранного корабля"><button data-angle="0" aria-pressed="true">Ракурс 1</button><button data-angle="1" aria-pressed="false">Ракурс 2</button></div><span id="gallery-count" class="sr-only">{variant_count(len(series))}</span>'
            gallery_html=f'<section class="ship-gallery" id="gallery" aria-labelledby="ship-gallery-title"><h2 id="ship-gallery-title">Все варианты корабля</h2><div class="gallery-grid">{grid}</div></section>'
        else:
            toolbar=f'<label class="select-label"><span class="sr-only">Серия изображений</span><select id="series-select">{options}</select></label><span class="mono gallery-count" id="gallery-count">{variant_count(len(current))}</span>'
            gallery_html=f'<div class="gallery-grid" id="gallery">{grid}</div>'
        dialog_navigation=f'<div class="dialog-navigation"><button id="dialog-previous" aria-label="Предыдущий ракурс">{ARROW}</button><button id="dialog-next" aria-label="Следующий ракурс">{ARROW}</button></div>' if is_ship else ''
        noscript_note='Выберите миниатюру или ракурс, чтобы открыть оригинал.' if is_ship else 'Все серии показаны ниже. Для оригинала откройте код под изображением.'
        page(f'{object_path(o)}/index.html',o['title'],f'''<div class="page-heading object-heading"><div><h1>{o['title']}</h1><p>{esc(o.get('subtitle','Визуальная разработка'))}</p></div><a class="quiet-link" href="reference.html">Справка {EXTERNAL}</a></div><nav class="derivatives" aria-label="Материалы объекта">{tabs}</nav><div class="gallery-toolbar">{toolbar}<button id="compare-toggle" class="quiet-button js-only" aria-pressed="false" {"hidden" if len(aa)<2 else ""}>Сравнить</button></div><section class="viewer" id="viewer" aria-label="Просмотр изображения"><a class="hero-link" id="hero-link" href="{first['original']}"><img id="hero-image" src="@ROOT@{first['display']}" alt="{esc(first['title'])}" width="1440" height="810" fetchpriority="high"></a><div class="viewer-caption"><div><strong id="hero-code" class="mono">{first['code']}</strong><span id="hero-title">{esc(first['title'])}</span></div><div class="viewer-step js-only" {"hidden" if len(aa)<2 else ""}><button id="previous-image" aria-label="Предыдущее изображение">{ARROW}</button><button id="next-image" aria-label="Следующее изображение">{ARROW}</button></div></div><div class="viewer-actions"><a id="original-link" href="{first['original']}" target="_blank" rel="noopener">Оригинал {EXTERNAL}</a><button class="js-only" id="copy-code">Копировать код</button><button class="js-only" id="copy-link">Копировать ссылку</button><button class="js-only" id="enlarge">Развернуть {EXTERNAL}</button><a class="gallery-fallback" href="#gallery">Все варианты {ARROW}</a></div><div id="viewer-rail" class="variant-rail js-only" aria-label="Выбор варианта"></div>{variant_note}</section><div id="compare-picker" class="compare-picker" hidden><div class="compare-slots" role="group" aria-label="Место для сравнения"><button type="button" data-compare-slot="left" aria-pressed="true">Первый вариант</button><button type="button" data-compare-slot="right" aria-pressed="false">Второй вариант</button><span id="compare-hint" role="status">Выберите первый вариант</span></div><div id="compare-rail" class="variant-rail" aria-label="Варианты для сравнения"></div></div><section id="compare-panel" class="compare-panel" aria-label="Сравнение вариантов" hidden><div><label for="compare-left">Первый вариант</label><select id="compare-left"></select><img id="compare-image-left" alt=""><span id="compare-caption-left" class="mono"></span></div><div><label for="compare-right">Второй вариант</label><select id="compare-right"></select><img id="compare-image-right" alt=""><span id="compare-caption-right" class="mono"></span></div></section>{gallery_html}<noscript><p class="noscript-note">{noscript_note}</p></noscript><dialog id="image-dialog"><div class="dialog-toolbar">{dialog_navigation}<button id="close-image" aria-label="Закрыть изображение">Закрыть</button></div><img id="dialog-image" alt=""><div class="mono" id="dialog-caption"></div></dialog>''',category=o['group'],obj=o['id'])
        source_commit=registry['assets'][0]['source_commit']
        pdf=f'https://raw.githubusercontent.com/esannikov/Alive/{source_commit}/Sources/ALIVE.pdf'
        pages=' · '.join(f'<a href="{pdf}#page={n}" target="_blank" rel="noopener">{n}</a>' for n in o['source_pages'])
        citations=f'<p class="source-pages">Страницы PDF: {pages}</p>' if pages else ''
        flow=''.join(f'<a class="reference-link" href="@ROOT@../ProductionFlow/#task={id}"><span>{tasks[id]["title"]}</span>{ARROW}</a>' for id in o['task_ids'])
        page(f'{object_path(o)}/reference.html',f'{o["title"]} · справка',f'''<div class="page-heading"><a class="back-link mono" href="./">К галерее {ARROW}</a><h1>{o['title']}: справка</h1></div><div class="reference-content"><section><h2>{esc(o.get('source_heading','Опоры в романе'))}</h2><p>{esc(o['source_summary'])}</p>{citations}<p class="subtle">{esc(o['source_note'])}</p><a class="quiet-link" href="https://github.com/esannikov/Alive/blob/{source_commit}/{o.get('source_doc','Bible/Characters.md')}" target="_blank" rel="noopener">{o.get('source_label', 'Описание персонажей · '+o['evidence'])} {EXTERNAL}</a></section><section><h2>В ProductionFlow</h2>{flow}</section><section><h2>Как читать материалы</h2><p>{o.get('reading_note','Это поисковые варианты. Выбранная внешность, подробный модельный лист и принятый комплект — отдельные результаты. Коды изображений сохраняются при перемещении между подборками.')}</p></section></div>''',category=o['group'])
    page('search.html','Поиск', '''<div class="page-heading"><h1>Поиск по миру</h1><p>Имя, постоянный код, предмет или нужный материал.</p></div><p class="mono" id="search-summary">Введите запрос в строке поиска.</p><div id="search-results" class="search-results"></div><noscript><p>Для поиска нужен JavaScript. <a href="catalog.html">Открыть полный каталог</a>.</p></noscript>''',active='search')
    for study in studies:
        page(study['path']+'/index.html', study['title'], (ROOT/study['body_file']).read_text(), category=study['group'])
    mapping={}
    for t in plan['tasks']:
        related=[{'title':o['title'],'url':f'../World/{object_path(o)}/'} for o in config['objects']+studies if t['id'] in o['task_ids']]
        if related:mapping[t['id']]=related
    flowfile=ROOT/'docs/ProductionFlow/index.html';flowtext=flowfile.read_text()
    payload=json.dumps(mapping,ensure_ascii=False,separators=(',',':'))
    if 'const WORLD_LINKS=' in flowtext:
        flowtext=re.sub(r'const WORLD_LINKS=.*?;\n',lambda _:f'const WORLD_LINKS={payload};\n',flowtext,count=1)
    else:raise RuntimeError('ProductionFlow integration marker missing; apply the integration patch once.')
    flowfile.write_text(flowtext)
    print(json.dumps({'status':'BUILT','images':len(assets),'objects':len(objects),'tasks':len(tasks),'pages':len(list(OUT.rglob('*.html')))},ensure_ascii=False))

    (OUT/'comment-pages.json').write_text(json.dumps(comment_pages, ensure_ascii=False, indent=2)+'\n')

if __name__=='__main__':build()
