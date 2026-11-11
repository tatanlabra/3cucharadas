"""Scribus native frame composition, named paragraph styles and master page."""
import scribus as s
import json,sys,os,traceback
from pathlib import Path
P=Path(__file__).resolve().parent
COL={'bg':'161616','ink':'f2f5f8','muted':'b5beca','cyan':'64d8e9','purple':'a79cff','rule':'424953','panel':'202329'}
def fmt(n):return ('+' if n>0 else '−' if n<0 else '')+f'{abs(n):.2f}'.replace('.',',')
try:
 prefix=Path(sys.argv[1]);c=json.loads(prefix.with_suffix('.content.json').read_text());frames=[];styles={};page_no=0
 s.newDocument((810,1012.5),(60,60,44,44),s.PORTRAIT,1,s.UNIT_POINTS,s.NOFACINGPAGES,s.FIRSTPAGERIGHT,1)
 for name,hexv in COL.items():s.defineColorRGB(name,*[int(hexv[j:j+2],16) for j in (0,2,4)])
 for name,size,color,bold in [('Title',48,'ink',True),('Body',30,'ink',False),('Note',23,'muted',False),('Kicker',22,'cyan',True),('Conclusion',31,'cyan',True)]:
  styles[name]=(size,color,bold)
  s.createParagraphStyle(name=name,linespacingmode=0,linespacing=size*1.19)
 def rect(x,y,w,h,color):
  n=s.createRect(x,y,w,h);s.setFillColor(color,n);s.setLineColor('None',n);return n
 def line(x,y,x2,y2,color='rule',width=1):
  n=s.createLine(x,y,x2,y2);s.setLineColor(color,n);s.setLineWidth(width,n)
 def text(t,x,y,w,h,style='Body',size=None,color=None):
  n=s.createText(x,y,w,h)
  s.setText(t,n)
  if page_no:s.setParagraphStyle(style,n)
  s.setTextDistances(0,0,0,0,n)
  base,ink,bold=styles[style];s.setFont('Fira Sans '+('Medium' if bold else 'Regular'),n);s.setFontSize(size or base,n);s.setTextColor(color or ink,n);s.setLineSpacing((size or base)*1.19,n)
  if color:s.setTextColor(color,n)
  frames.append({'name':n,'page':page_no,'text':t});return n
 def image(x,y,w,h):
  n=s.createImage(x,y,w,h);s.loadImage(str(P/'out/assets/hero.png'),n);s.setScaleImageToFrame(True,True,n)
 s.createMasterPage('3C Editorial');s.editMasterPage('3C Editorial')
 rect(0,0,810,1012.5,'bg');rect(0,0,18,1012.5,'cyan')
 s.closeMasterPage();s.gotoPage(1);frames=[]
 for i,d in enumerate(c['slides'],1):
  page_no=i
  if i>1:s.newPage(-1)
  s.applyMasterPage('3C Editorial',i);s.gotoPage(i)
  line(60,93,750,93)
  text('3 Cucharadas',60,40,400,40,'Kicker',26,'ink');text('EDUCACIÓN III',540,44,220,30,'Note',20)
  special=d['kind'] in ['cover','cta']
  text(d['kicker'],60,111,690,32,'Kicker')
  if special:
   text(d['title'],60,170,690,205,'Title',64)
   image(260,380,490,276)
   text(d['body'],60,690,690,155)
  else:
   text(d['title'],60,165,690,180,'Title')
   if d['kind']=='chart':
    text(d['body'],60,370,235,330)
    line(315,370,315,735)
    lo,hi=d['domain'];x=lambda v:355+(v-lo)/(hi-lo)*370
    for j,r in enumerate(d['rows']):
     y=370+j*205;color='cyan' if j==0 else 'purple'
     text(r['label'],345,y,405,34,'Note',25)
     text(fmt(r['value']),345,y+36,400,70,'Title',54,color)
     text(f'[{fmt(r["lo"])}; {fmt(r["hi"])}]',345,y+109,405,36,'Note',24)
     for v in d['ticks']:
      line(x(v),y+151,x(v),y+173,'rule');text(str(v).replace('-','−'),x(v)-14,y+178,45,30,'Note',21)
     line(x(r['lo']),y+162,x(r['hi']),y+162,color,3)
     n=s.createEllipse(x(r['value'])-5,y+157,10,10);s.setFillColor(color,n);s.setLineColor('None',n)
    text(d['interval']+' · puntos porcentuales',345,795,405,36,'Note',23)
   else:
    text(d['body'],60,355,690,140)
    if d['kind']=='method':
     for j,r in enumerate(d['cards']):
      y=535+j*125;line(60,y,750,y);text(r['label'],60,y+20,370,70,'Title',48,'cyan' if j==0 else 'purple');text(r['text'],455,y+28,290,70,'Body',28)
    elif d['kind']=='diagram':
     for j,v in enumerate(d['steps']):
      x=60+j*240;rect(x,535,220,155,'panel');text(f'{j+1:02d}',x+15,547,180,45,'Title',32,'cyan');text(v,x+15,602,190,80,'Body',28)
     for j,v in enumerate(d['branches']):text(v,60+j*350,730,325,80,'Conclusion',30,'purple')
    else:
     for j,v in enumerate(d['items']):
      y=525+j*95;line(60,y-8,750,y-8);text(f'{j+1:02d}',60,y+7,60,40,'Kicker');text(v,145,y,605,85,'Body',30)
  if d['kind']=='cta':
   rect(60,857,690,65,'cyan');text(d['takeaway']+' ↗',80,867,650,48,'Title',32,'bg');n=s.createText(60,857,690,65);s.setURIAnnotation(c['url'],n)
  else:
   line(60,842,750,842,'cyan',2);text(d['takeaway'],60,858,690,92,'Conclusion')
  text(d['note'],60,952,630,60,'Note',21)
  text(f'{i:02d}',711,960,50,30,'Kicker',22,'muted')
 overflows=[f for f in frames if s.textOverflows(f['name'])]
 prefix.with_suffix('.overflow.json').write_text(json.dumps(overflows,ensure_ascii=False,indent=2))
 s.setInfo('Cristián Labra Olivares','Educación III · D','Piloto nativo de composición editorial')
 s.saveDocAs(str(prefix.with_suffix('.sla')))
 pdf=s.PDFfile();pdf.file=str(prefix.with_suffix('.pdf'));pdf.pages=list(range(1,10));pdf.version=15;pdf.compress=True;pdf.quality=0;pdf.resolution=300;pdf.outdst=0;pdf.embedPDF=True;pdf.fonts=['Fira Sans Regular','Fira Sans Medium'];pdf.save();os._exit(0)
except BaseException:
 (P/'out/native/scribus-error.log').write_text(traceback.format_exc());os._exit(1)
