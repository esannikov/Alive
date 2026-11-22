"""Render Fedor's character sheets with the World package components."""
from html import escape


GROUPS = {
    'look': 'Типаж и модельные листы', 'face': 'Лицо крупным планом',
    'acting': 'Мимика и пластика', 'wardrobe': 'Костюмы и состояния',
    'headwear': 'Примерки с морской шапкой', 'scenes': 'Сюжетные пробы',
    'details': 'Детали и реквизит', 'clothes': 'Библиотека одежды',
}


def figure(asset):
    title = escape(asset['title'])
    code = escape(asset['code'])
    file = escape(asset['file'])
    pages = ', '.join(map(str, asset['pages']))
    note = f'<p>{escape(asset["caption"])}</p>' if asset['caption'] else ''
    if pages:
        note += f'<p class="tais-source">Страницы романа · {pages}</p>'
    if ref := asset.get('reference'):
        note += f'<p><a href="#{escape(ref)}">Посадка на Федоре · {escape(ref.upper())}</a></p>'
    return f'''<figure class="tais-sheet" id="{asset['id']}"><a class="tais-image-link" href="{file}" data-package-image="{file}" data-caption="{code} · {title}">
<img src="{escape(asset['preview'])}" width="{asset['width']}" height="{asset['height']}" alt="{title}" loading="lazy"></a>
<figcaption><div class="tais-caption-heading"><strong><span class="mono">{code}</span> {title}</strong><a href="{file}" download>PNG ↓</a></div>{note}</figcaption></figure>'''


def render(data):
    nav = ''.join(f'<a href="#{key}">{title}</a>' for key, title in GROUPS.items())
    sections = []
    for key, title in GROUPS.items():
        items = [a for a in data['assets'] if a['group'] == key]
        sections.append(f'<section id="{key}"><h2>{title}</h2><div class="tais-examples">'
                        + ''.join(map(figure, items)) + '</div></section>')
    return f'''<div class="package-proposal"><header class="package-heading"><a class="back-link" href="../">Федор · галерея</a><h1>Федор</h1><p>Модельный лист · типаж 009</p>
<div class="package-actions"><a class="button primary-button" href="{data['pdf']}">Скачать PDF</a>
<a href="{data['prompt_pack']}">Промпты</a><a href="{data['prompt_library']}">Лицо по зонам</a>
<a href="{data['wardrobe_library']}">Промпты для одежды</a></div></header>
<div class="package-layout"><aside class="package-index"><details open id="package-index"><summary>Содержание</summary><nav>{nav}</nav></details></aside>
<div class="package-content">{''.join(sections)}</div></div></div>
<dialog id="package-image-dialog" class="package-image-dialog"><div class="package-image-bar"><span id="package-image-title"></span>
<button id="package-image-actual" aria-pressed="false">100%</button><a id="package-image-download" href="images/fp01.png" download>PNG ↓</a>
<button id="package-image-close">Закрыть ×</button></div><div class="package-image-scroll"><img id="package-image-full" alt=""></div></dialog>'''
