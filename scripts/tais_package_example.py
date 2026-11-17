"""Illustrated Tais example for the proposal page; approval of identity is separate."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'Production/Dashboard/Tais_Package_Example_2026-11-17.json'
def load():return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else None
DATA=load();esc=html.escape
SOURCE='https://raw.githubusercontent.com/esannikov/Alive/1d1136ad314bff683317fca08f24d1dccf03c3bc/Sources/ALIVE.pdf'
def section_example(section):
 if not DATA:return ''
 if section=='animation':return '<p class="tais-example-note">В примере Таис показана только фотореалистическая часть. Две анимационные версии здесь пока не иллюстрируются — по решению пользователя.</p>'
 assets=[a for a in DATA['assets'] if a['section']==section]
 if not assets:return ''
 out='<div class="tais-examples"><p class="tais-example-label">Пример на Таис</p>'
 for a in assets:
  identity=a['code'].lower();links=' · '.join(f'<a href="{SOURCE}#page={p}" target="_blank" rel="noopener">{p}</a>' for p in a['pages'])
  out+=f'''<figure class="tais-sheet" id="{identity}"><a class="tais-image-link" href="{a['file']}" data-package-image="{a['file']}" data-caption="{esc(a['code']+' · '+a['title'])}" aria-label="Увеличить: {esc(a['title'])}"><img src="{a['preview']}" width="{a['width']}" height="{a['height']}" loading="lazy" decoding="async" alt="{esc(a['title'])} — Таис на светло-бежевом фоне"></a><figcaption><div class="tais-caption-heading"><strong><span class="mono">{a['code']}</span> {esc(a['title'])}</strong><a href="{a['file']}" download>PNG ↓</a></div><p>{esc(a['caption'])}</p>'''
  if links:out+='<p class="tais-source">Роман, страницы PDF: '+links+'</p>'
  out+='</figcaption></figure>'
 if section=='continuity':
  rows=[('TC01 · ранняя вылазка','43–44','Косы и бандана; серая куртка и бриджи','Рюкзак и магнитная доска'),('TC02 · куртка сохнет','52','Тёмно-синяя пайта; длинные штаны','Повторно используются доступные вещи'),('Ранение и перевязка','317–319','Пайта разрезана; плечо перевязано. Сторона не уточнена','Марля и пластырь — временное состояние'),('TC03 · вещи из каюты','377','Найденная джинсовая рубашка','Куртки с активными нашивками не берут'),('Заживление','417','Скобы рассасываются; ожидается шрам плеча','Лазерный меч — позднее снаряжение'),('TC04 · новые вещи','458','Спортивные штаны, полосатый верх; волосы распущены','Предыдущий комплект заменён')]
  out+='<div class="package-table-wrap"><table><caption>Таис: преемственность по событиям</caption><thead><tr><th>Состояние</th><th>Страницы</th><th>Одежда, волосы, повреждения</th><th>Вещи</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
 return out+'</div>'
def intro():
 if not DATA:return ''
 return f'''<section class="tais-example-intro" id="tais-example"><div><h2>Как выглядит пакет: Таис</h2><p>Фотореалистический пример на утверждённом типaже А — <a href="@ROOT@characters/tais/#tais053">tais053</a>. Лена и Игорь согласовали эту основу лица; новые листы раскрывают состав пакета и обсуждаются отдельно.</p><p class="tais-muted">{len(DATA['assets'])} аркуша/листа · 6 ракурсов фигуры · 12 выражений · 8 поз · 4 сюжетных комплекта одежды. Технические материалы — на спокойном светло-бежевом фоне.</p><div class="package-actions"><a class="button primary-button" href="tais/TAIS_Photoreal_Package_v1.pdf" download>PDF-пример ↓</a><a class="quiet-link" href="tais/TAIS_Prompt_Pack.md" download>Промпты для агентов · MD ↓</a><a class="quiet-link" href="#p-passport">Смотреть листы ↓</a></div></div><a class="tais-intro-image" href="tais/images/tp01.png" data-package-image="tais/images/tp01.png" data-caption="TAIS-TP01 · Паспорт образа"><img src="tais/images/tp01.webp" width="1024" height="1536" alt="Таис — полный рост на бежевом фоне"></a></section>'''.replace('типaже','типаже').replace('аркуша/листа','листа')
def downloads():
 if not DATA:return ''
 return '<div class="tais-downloads"><strong>Готовый пример Таис</strong><a href="tais/TAIS_Photoreal_Package_v1.pdf" download>Сводный PDF · 26 страниц ↓</a><a href="tais/TAIS_Prompt_Pack.md" download>MD-пакет промптов ↓</a><p>Оригинальный PNG каждого листа доступен под его изображением. Анимационная часть в этот пример не включена.</p></div>'
def dialog():
 if not DATA:return ''
 return '''<dialog id="package-image-dialog" class="package-image-dialog"><div class="package-image-bar"><span id="package-image-title"></span><button type="button" id="package-image-actual" aria-pressed="false">100%</button><a id="package-image-download" href="tais/images/tp01.png" download>PNG ↓</a><button type="button" id="package-image-close" aria-label="Закрыть изображение">Закрыть ×</button></div><div class="package-image-scroll"><img id="package-image-full" alt=""></div></dialog>'''
