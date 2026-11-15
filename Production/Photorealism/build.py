from pathlib import Path
import json,hashlib,shutil,html,sys,zipfile,re,io
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing,Rect,Circle,Line,String,Polygon
from reportlab.graphics import renderSVG
from PIL import Image as PILImage
from content import pages,sources

ROOT=Path(__file__).resolve().parents[2] if Path(__file__).parent.name=='Photorealism' else Path.cwd()/'work/alive-clothing-site'
OUT=ROOT/'docs/World/photorealism';OUT.mkdir(parents=True,exist_ok=True)
(OUT/'assets').mkdir(exist_ok=True);(OUT/'prompts').mkdir(exist_ok=True);(OUT/'sources').mkdir(exist_ok=True)
shutil.copy2(ROOT/'Production/Photorealism/approved_principles.txt',OUT/'sources/approved_principles_2026-11-09.txt')
REG=json.loads((ROOT/'Production/Dashboard/asset_codes.json').read_text())
codes=['ira007','dimka010','andrey001','kolka025','emma018','taisc001','gardener005','senka007']
assets={}
for code in codes:
 a=next(a for a in REG['assets'] if a['code']==code);src=ROOT/a['source_file'];target=OUT/'assets'/(code+src.suffix);shutil.copy2(src,target)
 assert hashlib.sha256(target.read_bytes()).hexdigest()==a['sha256']
 assets[code]={**{k:a[k] for k in ['code','caption','source_file','source_commit','sha256']},'file':str(target.relative_to(OUT)),'url':f'https://raw.githubusercontent.com/esannikov/Alive/{a["source_commit"]}/{a["source_file"]}'}
dash=ROOT/'Production/Dashboard'
prompts={}
prompts['ira007']=json.loads((dash/'Semyon_Ira_Senka_2026-11-09.json').read_text())['scenes']['ira007']
prompts['dimka010']=next(j['prompt'] for j in json.loads((dash/'Dimka_2026-11-12.json').read_text())['jobs'] if j['published_code']=='dimka010')
prompts['andrey001']=next(j['prompt'] for j in json.loads((dash/'fedor_dimka_andrey_2026-11-09.json').read_text())['items'] if j['code']=='andrey001')
for code in ['kolka025','emma018']:
 prompts[code]=next(j['prompt'] for j in json.loads((dash/'Emma_Kolka_Casting_2026-11-15.json').read_text())['items'] if j['code']==code)
for code,prompt in prompts.items():(OUT/'prompts'/f'{code}.txt').write_text(prompt)
fonts=Path('/System/Library/Fonts/Supplemental')
pdfmetrics.registerFont(TTFont('ArialU',str(fonts/'Arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialUB',str(fonts/'Arial Bold.ttf')))
pdfmetrics.registerFontFamily('ArialU',normal='ArialU',bold='ArialUB',italic='ArialU',boldItalic='ArialUB')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyA',fontName='ArialU',fontSize=9.6,leading=13.3,spaceAfter=9,textColor=colors.HexColor('#263232')))
styles.add(ParagraphStyle(name='SmallA',fontName='ArialU',fontSize=8.1,leading=10.8,spaceAfter=6,textColor=colors.HexColor('#52615d')))
styles.add(ParagraphStyle(name='HeadA',fontName='ArialUB',fontSize=21,leading=25,spaceAfter=15,textColor=colors.HexColor('#143d37'),keepWithNext=True))
styles.add(ParagraphStyle(name='KickerA',fontName='ArialUB',fontSize=8,leading=11,spaceAfter=9,textColor=colors.HexColor('#6b8374'),keepWithNext=True))
styles.add(ParagraphStyle(name='CellA',fontName='ArialU',fontSize=8.4,leading=11,spaceAfter=0))
styles.add(ParagraphStyle(name='CellB',fontName='ArialUB',fontSize=8.3,leading=10.8,textColor=colors.white))
styles.add(ParagraphStyle(name='CodeA',fontName='ArialU',fontSize=8.1,leading=11.1,backColor=colors.HexColor('#eef2ee'),borderPadding=8,spaceAfter=12))
def para(t,style='BodyA'):return Paragraph(html.escape(t).replace('\n','<br/>'),styles[style])
W=507
def fit_image(code,maxw=W,maxh=245):
 path=OUT/assets[code]['file']
 with PILImage.open(path) as im:
  w,h=im.size; display=im.convert('RGB');display.thumbnail((2200,2200));buf=io.BytesIO();display.save(buf,format='JPEG',quality=94,subsampling=0);buf.seek(0)
 ratio=min(maxw/w,maxh/h)
 return Image(buf,width=w*ratio,height=h*ratio)
def arrow(d,x1,y1,x2,y2,col):
 import math
 d.add(Line(x1,y1,x2,y2,strokeColor=col,strokeWidth=1.5));a=math.atan2(y2-y1,x2-x1);s=7
 d.add(Polygon([x2,y2,x2-s*math.cos(a-.45),y2-s*math.sin(a-.45),x2-s*math.cos(a+.45),y2-s*math.sin(a+.45)],fillColor=col,strokeColor=col))
def light_diagram(kind):
 d=Drawing(507,205);green=colors.HexColor('#256d5b');warm=colors.HexColor('#c68a47');ink=colors.HexColor('#344641')
 d.add(Rect(1,1,505,203,fillColor=colors.HexColor('#f1f4ef'),strokeColor=colors.HexColor('#c6d3ca'),rx=8))
 d.add(String(18,183,'ВИД ЗВЕРХУ · УМОВНА СХЕМА, НЕ МАСШТАБНИЙ ПЛАН',fontName='ArialU',fontSize=8,fillColor=ink))
 subjects=[(244,102)] if kind!='l2' else [(211,102),(294,102)]
 for n,(x,y) in enumerate(subjects):
  d.add(Circle(x,y,15,fillColor=colors.HexColor('#d8b798'),strokeColor=ink));d.add(String(x-8,y-3,'A' if n==0 else 'B',fontName='ArialUB',fontSize=9));arrow(d,x+18 if n==0 else x-18,y,x+35 if n==0 else x-35,y,ink) if kind=='l2' else arrow(d,x,y-17,x,y-31,ink)
 d.add(Rect(228,28,42,19,fillColor=ink,strokeColor=None));d.add(String(225,14,'КАМЕРА',fontName='ArialU',fontSize=8,fillColor=ink))
 key={'l1':(175,40),'l2':(402,128),'l3':(120,70),'l4':(402,145),'l5':(140,62),'l6':(102,108)}[kind]
 d.add(Rect(key[0]-7,key[1]-24,14,48,fillColor=green,strokeColor=None));d.add(String(key[0]-30,key[1]+33,'KEY / КЛЮЧ',fontName='ArialUB',fontSize=8,fillColor=green))
 for x,y in subjects:arrow(d,key[0]+(12 if key[0]<200 else -12),key[1],x+(-18 if key[0]<200 else 18),y,green)
 if kind in ['l2','l3','l5']:
  d.add(Circle(340,158,7,fillColor=warm,strokeColor=None));d.add(String(355,155,'ЛАМПА',fontName='ArialU',fontSize=8,fillColor=ink));arrow(d,333,153,285,120,warm)
 fillx=320 if kind!='l2' else 250
 d.add(Rect(fillx-32,59,64,6,fillColor=colors.HexColor('#bbc8b5'),strokeColor=None));d.add(String(fillx-42,47,'СЛАБКЕ ВІДБИТТЯ',fontName='ArialU',fontSize=7,fillColor=ink))
 if kind in ['l1','l3','l6']:
  d.add(Rect(360,83,6,49,fillColor=ink,strokeColor=None));d.add(String(377,109,'ЧОРНИЙ',fontName='ArialU',fontSize=7,fillColor=ink));d.add(String(377,98,'ЕКРАН',fontName='ArialU',fontSize=7,fillColor=ink))
 if kind=='l4':d.add(String(330,76,'ВЕЛИКИЙ ВЕРХНЬОБОКОВИЙ ОТВІР',fontName='ArialU',fontSize=6.5,fillColor=green))
 return d

class Doc(SimpleDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='HeadA':
   key='p'+str(self.page);self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0,False)
def chrome(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#b6c8bc'));c.line(44,804,551,804);c.setFont('ArialU',7.5);c.setFillColor(colors.HexColor('#52615d'));c.drawString(44,815,'ALIVE / PHOTOREALISM / v1.0');c.drawRightString(551,815,'ПОДАНО НА ПОГОДЖЕННЯ · 15.11.2026');c.line(44,36,551,36);c.drawString(44,24,'Робочий стандарт · грудневі доповнення зазначено окремо');c.drawRightString(551,24,str(doc.page));c.restoreState()

story=[Spacer(1,35),para('ALIVE','KickerA'),Paragraph('Фотореалістичний<br/>стиль',ParagraphStyle(name='Cover',fontName='ArialUB',fontSize=38,leading=44,textColor=colors.HexColor('#143d37'),spaceAfter=18)),para('Виробничий пакет v1.0 · листопад 2026','HeadA'),fit_image('ira007',W,280),Spacer(1,18),para('Світло · оптика · плівкова подача · матеріали · промпти · перевірка'),para('Зібрано з готових матеріалів ALIVE для погодження базового напряму. Шість схем освітлення, вісім прикладів, п’ять точних промптів та окрема програма грудневого довідника.'),para('Статус: версія для продюсерського розгляду. Схеми й числові рецепти позначені як робочі пропозиції; приймання дизайну та результати невиконаних тестів не припускаються.','SmallA'),PageBreak()]
toc=[para('Навігація пакетом','HeadA')]
for n,x in enumerate(pages,3):toc.append(Paragraph(f'<link href="#p{n}" color="#256d5b">{html.escape(x["title"])}</link>  ·  {n}',styles['SmallA']))
toc.extend([para('Додаток A · точні архівні промпти (5)','SmallA'),para('Додаток B · джерела, оригінали, версії та контрольні суми','SmallA'),PageBreak()]);story+=toc
web=[];md=['# ALIVE · Фотореалістичний стиль v1.0\n\n15.11.2026. Пакет на погодження; грудневий довідник доповнюється окремо.\n']
def make_table(b):
 n=len(b['head']);widths=([110,205,192] if n==3 else [133,374]);rows=[[para(x,'CellB') for x in b['head']]]+[[para(x,'CellA') for x in row] for row in b['rows']]
 t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#234c42')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f4ef'),colors.white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#234c42'))]));return t
for section in pages:
 story.extend([para(section['kicker'],'KickerA'),para(section['title'],'HeadA')]);h=[f'<section id="{section["id"]}"><p class="eyebrow">{section["kicker"]}</p><h2>{section["title"]}</h2>'];md.append('\n## '+section['title']+'\n')
 for b in section['blocks']:
  typ=b['type']
  if typ=='p':story.append(para(b['text']));h.append('<p>'+html.escape(b['text'])+'</p>');md.append(b['text']+'\n')
  elif typ=='bullets':
   h.append('<ul>')
   for item in b['items']:story.append(Paragraph('• '+html.escape(item),styles['BodyA']));h.append('<li>'+html.escape(item)+'</li>');md.append('- '+item)
   h.append('</ul>');md.append('')
  elif typ=='table':
   story.extend([make_table(b),Spacer(1,12)]);h.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+html.escape(x)+'</th>' for x in b['head'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(x)+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table></div>');md.extend([' | '.join(b['head']),' | '.join(['---']*len(b['head']))]+[' | '.join(row) for row in b['rows']]+[''])
  elif typ=='code':story.append(para(b['text'],'CodeA'));h.append('<pre>'+html.escape(b['text'])+'</pre>');md.append('```text\n'+b['text']+'\n```\n')
  elif typ=='image':
   story.extend([fit_image(b['code']),Spacer(1,6),para(b['caption'],'SmallA')]);h.append(f'<figure><img src="@ROOT@photorealism/{assets[b["code"]]["file"]}" alt="{html.escape(b["caption"])}"><figcaption>{html.escape(b["caption"])}</figcaption></figure>')
  elif typ=='grid':
   rows=[]
   for i in range(0,len(b['codes']),2):
    row=[]
    for code,caption in zip(b['codes'][i:i+2],b['captions'][i:i+2]):row.append([fit_image(code,235,175 if len(b['codes'])>2 else 315),Spacer(1,4),para(caption,'SmallA')])
    rows.append(row)
   grid=Table(rows,colWidths=[W/2,W/2]);grid.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),9)]));story.append(grid)
   h.append('<div class="proof-grid">'+''.join(f'<figure><img src="@ROOT@photorealism/{assets[c]["file"]}" alt="{html.escape(cap)}"><figcaption>{html.escape(cap)}</figcaption></figure>' for c,cap in zip(b['codes'],b['captions']))+'</div>')
  elif typ=='diagram':
   d=light_diagram(b['kind']);story.extend([d,Spacer(1,10)]);svg=renderSVG.drawToString(d);(OUT/'assets'/(b['kind']+'.svg')).write_text(svg);h.append(f'<img class="light-plan" src="@ROOT@photorealism/assets/{b["kind"]}.svg" alt="План джерел {b["kind"]}">')
 h.append('</section>');web.append(''.join(h));story.append(PageBreak())

for code,prompt in prompts.items():
 story.extend([para('ДОДАТОК A / ТОЧНИЙ АРХІВНИЙ ТЕКСТ','KickerA'),para('Промпт · '+code,'HeadA'),para('Наведено дослівно з маніфесту відповідної серії. Це історія конкретного результату; нові універсальні шаблони містяться у розділах 16–17.','SmallA')])
 for text in prompt.split('\n\n'):story.append(para(text,'CodeA'))
 story.append(PageBreak())
 web.append(f'<section id="prompt-{code}"><p class="eyebrow">ДОДАТОК A / АРХІВНИЙ ПРОМПТ</p><h2>{code}</h2><a href="@ROOT@photorealism/prompts/{code}.txt" download>Завантажити TXT</a><details><summary>Повний текст без редактури</summary><pre>{html.escape(prompt)}</pre></details></section>')
 md.append('\n## Архівний промпт '+code+'\n\n```text\n'+prompt+'\n```\n')

story.extend([para('ДОДАТОК B / ДЖЕРЕЛА','KickerA'),para('Джерела та контрольні файли','HeadA')]);sourcehtml=['<section id="sources"><h2>Джерела та контрольні файли</h2><p>Технічні сторінки перевірені 15.11.2026. Авторські схеми ALIVE не є копіями схем виробників.</p><ul>']
for id,title,url,note in sources:
 story.append(Paragraph(f'<b>{id} · <link href="{html.escape(url,quote=True)}" color="#256d5b">{html.escape(title)}</link></b><br/>{html.escape(note)}',styles['BodyA']));sourcehtml.append(f'<li><a href="{url}">{id} · {title}</a> — {note}</li>');md.append(f'- [{id} · {title}]({url}) — {note}')
story.append(para('Внутрішні опори: Sources/Novel.md; Bible/Visual_Development.md; робочий принцип ALIVE_PHOTOREALISM від 09.11; маніфести Semyon_Ira_Senka, Dimka, fedor_dimka_andrey, Emma_Kolka_Casting, Tais_Clothing і Gardener_Selection. Точні шляхи, commits і SHA-256 включені у manifest.json.','SmallA'))
for code,a in assets.items():
 story.append(Paragraph(f'<b>{code}</b> · <link href="{a["url"]}" color="#256d5b">незмінний оригінал</link><br/>SHA-256: {a["sha256"][:32]}<br/>{a["sha256"][32:]}',styles['SmallA']));sourcehtml.append(f'<li><a href="{a["url"]}">{code} · оригінал</a></li>')
sourcehtml.append('</ul><p><a href="@ROOT@photorealism/manifest.json">Реєстр походження й SHA-256</a> · <a href="@ROOT@photorealism/guide.md">Редагований текст Markdown</a> · <a href="@ROOT@photorealism/december.md">Грудневі доробки окремо</a></p></section>');web.append(''.join(sourcehtml))
doc=Doc(str(OUT/'ALIVE_Photorealism_v1.0.pdf'),pagesize=(595.28,841.89),rightMargin=44,leftMargin=44,topMargin=55,bottomMargin=49,title='ALIVE · Фотореалістичний стиль v1.0',author='ALIVE · Візуальна розробка')
doc.build(story,onFirstPage=chrome,onLaterPages=chrome)
css='''<style>.photo-pkg{max-width:1020px}.photo-pkg .intro{font-size:1.15rem;line-height:1.65}.photo-pkg section{padding:36px 0;border-top:1px solid #394944;scroll-margin-top:25px}.photo-pkg h2{font-size:clamp(24px,3vw,34px);line-height:1.2}.photo-pkg p,.photo-pkg li{line-height:1.75;max-width:85ch}.photo-pkg .eyebrow{font-size:12px;letter-spacing:.08em;color:#b3c59c}.photo-pkg table{width:100%;border-collapse:collapse;font-size:14px}.photo-pkg th,.photo-pkg td{padding:13px;text-align:left;vertical-align:top;border:1px solid #3b4942}.photo-pkg th{background:#253c32}.photo-pkg .table-wrap{overflow-x:auto}.photo-pkg figure{margin:18px 0}.photo-pkg img{max-width:100%;max-height:620px;width:auto;height:auto;object-fit:contain}.photo-pkg figcaption{font-size:13px;color:#bac4bb;line-height:1.6;margin-top:10px}.photo-pkg .proof-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.photo-pkg .proof-grid img{width:100%;max-height:440px}.photo-pkg pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.7;padding:20px;background:#17251e;border:1px solid #395044}.photo-pkg .light-plan{width:100%;background:#f1f4ef;border-radius:8px}.photo-pkg .toc{columns:2;column-gap:30px;padding:18px 0}.photo-pkg .toc a{display:block;break-inside:avoid;padding:5px 0;font-size:14px}.photo-pkg .downloads{display:flex;gap:12px;flex-wrap:wrap;margin:25px 0}.photo-pkg details{margin-top:16px}.photo-pkg summary{cursor:pointer}@media(max-width:650px){.photo-pkg .toc{columns:1}.photo-pkg .proof-grid{grid-template-columns:1fr}.photo-pkg th,.photo-pkg td{padding:8px;font-size:12px}}</style>'''
body=css+'<article class="photo-pkg"><p class="eyebrow">ALIVE / ФОТОРЕАЛІЗМ / v1.0 / 15.11.2026</p><h1>Фотореалістичний стиль</h1><p class="intro">Робочий пакет на погодження: світло, оптика, плівкова подача, фактури, промпти та контроль якості. Зібрано з готових матеріалів. Грудневі доповнення позначені окремо.</p><div class="downloads"><a class="button" href="@ROOT@photorealism/ALIVE_Photorealism_v1.0.pdf">PDF · повний пакет</a><a class="button" href="@ROOT@photorealism/ALIVE_Photorealism_v1.0.zip">ZIP · джерела й промпти</a><a class="button" href="#december">Що доробити до грудня</a></div><nav class="toc" aria-label="Розділи пакета">'+''.join(f'<a href="#{s["id"]}">{s["title"]}</a>' for s in pages)+'</nav>'+''.join(web)+'</article>'
(dash/'photorealism_body.html').write_text(body)
(OUT/'guide.md').write_text('\n'.join(md))
dec=next(s for s in pages if s['id']=='december');(OUT/'december.md').write_text('# '+dec['title']+'\n\n'+ '\n\n'.join(b.get('text','') if b['type']=='p' else '\n'.join(' | '.join(row) for row in [b['head']]+b['rows']) for b in dec['blocks']))
manifest={'version':'1.0','date':'2026-11-15','status':'submitted_for_review_candidate','generated_new_images':False,'assets':list(assets.values()),'exact_prompts':[{ 'code':c,'file':f'prompts/{c}.txt','sha256':hashlib.sha256(t.encode()).hexdigest()} for c,t in prompts.items()],'sources':[dict(id=x[0],title=x[1],url=x[2],note=x[3]) for x in sources],'sections':[{'id':x['id'],'title':x['title']} for x in pages],'december_work':'KPP-R257','november_work':'KPP-R017','disclosure':'Lighting values, palette roles, film looks and test protocols are proposals; archival prompts and images are existing evidence, not measured camera metadata.'}
prompt_sources={'ira007':('Semyon_Ira_Senka_2026-11-09.json','scenes.ira007'),'dimka010':('Dimka_2026-11-12.json','jobs[published_code=dimka010].prompt'),'andrey001':('fedor_dimka_andrey_2026-11-09.json','items[code=andrey001].prompt'),'kolka025':('Emma_Kolka_Casting_2026-11-15.json','items[code=kolka025].prompt'),'emma018':('Emma_Kolka_Casting_2026-11-15.json','items[code=emma018].prompt')}
for row in manifest['exact_prompts']:
 f,selector=prompt_sources[row['code']];row.update(source_manifest='Production/Dashboard/'+f,selector=selector)
manifest['approved_principles']={'file':'sources/approved_principles_2026-11-09.txt','scope':'Working photographic method accepted by Eugene; not producer approval of all designs','sha256':hashlib.sha256((OUT/'sources/approved_principles_2026-11-09.txt').read_bytes()).hexdigest()}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(OUT/'ALIVE_Photorealism_v1.0.zip','w',zipfile.ZIP_DEFLATED) as z:
 for pth in sorted(OUT.rglob('*')):
  if pth.is_file() and pth.suffix not in ['.zip','.html']:z.write(pth,Path('ALIVE_Photorealism_v1.0')/pth.relative_to(OUT))
print(json.dumps({'sections':len(pages),'exact_prompts':len(prompts),'reference_images':len(assets),'pdf_bytes':(OUT/'ALIVE_Photorealism_v1.0.pdf').stat().st_size,'output':str(OUT)}))
