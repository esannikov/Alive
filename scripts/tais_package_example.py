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
  out+=f'''<figure class="tais-sheet" id="{identity}"><a class="tais-image-link" href="{a['file']}" data-package-image="{a['file']}" data-caption="{esc(a['code']+' · '+a['title'])}" aria-label="Увеличить: {esc(a['title'])}"><img src="{a['preview']}" width="{a['width']}" height="{a['height']}" loading="lazy" decoding="async" alt="{esc(a['title'])} "></a><figcaption><div class="tais-caption-heading"><strong><span class="mono">{a['code']}</span> {esc(a['title'])}</strong><a href="{a['file']}" download>PNG ↓</a></div>'''
  if a['caption']:out+=f'<p>{esc(a["caption"])}</p>'
  if links:out+='<p class="tais-source">Роман, страницы PDF: '+links+'</p>'
  gallery=a.get('gallery')
  if gallery:
   out+=f'<p id="{identity}-variants"><a href="@ROOT@{esc(gallery["path"])}/">{esc(gallery["title"])}</a></p>'
  out+='</figcaption></figure>'
 if section=='continuity':
  rows=[('TC01 · ранняя вылазка','43–44','Для адаптации утверждены тёмный анорак, длинные брюки карго и красная бандана с сакурой','Рюкзак и магнитная доска'),('TC02 · куртка сохнет','52','Тёмно-синяя пайта; длинные штаны','Повторно используются доступные вещи'),('Ранение и перевязка','317–319','Пайта разрезана. Сторона плеча остаётся открытым решением','Скобы, марлевая салфетка и лейкопластырь'),('TC03 · вещи из каюты','377','Найденная джинсовая рубашка','Куртки с активными нашивками не берут'),('Заживление','417','Скобы рассасываются; ожидается шрам плеча','Лазерный меч — позднее снаряжение'),('TC04 · новые вещи','458','Спортивные штаны, полосатый верх; волосы распущены','Предыдущий комплект заменён')]
  out+='<div class="package-table-wrap"><table><caption>Таис: преемственность по событиям</caption><thead><tr><th>Состояние</th><th>Страницы</th><th>Одежда, волосы, повреждения</th><th>Вещи</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
 return out+'</div>'
def intro():
 if not DATA:return ''
 publication=DATA['publication']
 passport=next(a for a in DATA['assets'] if a['section']=='passport')
 return f'''<section class="tais-example-intro" id="tais-example"><div><h2>Фотореалистический пакет Таис</h2><p>Утверждённый <a href="@ROOT@characters/tais/#tais053">типаж А · tais053</a> в базовом костюме с тёмно-синим анораком, брюками карго и красной банданой с сакурой.</p><p class="tais-muted">Версия {esc(DATA['version'])} · {len(DATA['assets'])} листа · 6 ракурсов в костюме · 12 выражений · 8 поз · 4 сюжетных комплекта одежды.</p><div class="package-actions"><a class="button primary-button" href="{esc(publication['pdf'])}" download>Фотореалистический пакет · PDF ↓</a><a class="quiet-link" href="{esc(publication['prompt_pack'])}" download>Промпты для агентов · MD ↓</a><a class="quiet-link" href="#tais-tp24">Модельный лист фигуры ↓</a><a class="quiet-link" href="#p-passport">Смотреть все листы ↓</a></div></div><a class="tais-intro-image" href="{esc(passport['file'])}" data-package-image="{esc(passport['file'])}" data-caption="TAIS-TP01 · Паспорт образа"><img src="{esc(passport['preview'])}" width="{passport['width']}" height="{passport['height']}" alt="Таис в согласованном костюме, полный рост"></a></section>'''
def downloads():
 if not DATA:return ''
 publication=DATA['publication']
 return f'''<div class="tais-downloads"><strong>Комплект Таис · версия {esc(DATA['version'])}</strong><a href="{esc(publication['pdf'])}" download>Сводный PDF · {publication['page_count']} страниц ↓</a><a href="{esc(publication['prompt_pack'])}" download>MD-пакет промптов ↓</a><p>Оригинальный PNG каждого листа доступен под его изображением.</p></div>'''
def dialog():
 if not DATA:return ''
 passport=next(a for a in DATA['assets'] if a['section']=='passport')
 return f'''<dialog id="package-image-dialog" class="package-image-dialog"><div class="package-image-bar"><span id="package-image-title"></span><button type="button" id="package-image-actual" aria-pressed="false">100%</button><a id="package-image-download" href="{esc(passport['file'])}" download>PNG ↓</a><button type="button" id="package-image-close" aria-label="Закрыть изображение">Закрыть ×</button></div><div class="package-image-scroll"><img id="package-image-full" alt=""></div></dialog>'''
