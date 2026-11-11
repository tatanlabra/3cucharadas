"""Run with the official Scribus Scripter interpreter, not system Python."""
import scribus as s
import json,sys,os,traceback
from pathlib import Path
P=Path(__file__).resolve().parent
try:
 prefix=Path(sys.argv[1]);pages=json.loads(prefix.with_suffix('.scene.json').read_text())
 s.newDocument((810,1012.5),(0,0,0,0),s.PORTRAIT,1,s.UNIT_POINTS,s.NOFACINGPAGES,s.FIRSTPAGERIGHT,1)
 colors=set(o['color'] for ops in pages for o in ops if 'color' in o)
 for c in colors:s.defineColorRGB('c'+c,*[int(c[i:i+2],16) for i in (0,2,4)])
 overflows=[]
 for i,ops in enumerate(pages):
  if i:s.newPage(-1)
  for j,o in enumerate(ops):
   k=o['kind'];x=o['x']*.75;y=o['y']*.75;name=f'p{i+1}_{j}'
   if k=='text':
    n=s.createText(x,y,o['w']*.75,o['h']*.75,name);s.setText(o['text'],n)
    s.setFont('Fira Sans '+('Medium' if o['weight']==500 else 'SemiBold' if o['weight']==600 else 'Regular'),n)
    s.setFontSize(o['size']*.75,n);s.setTextColor('c'+o['color'],n)
    s.setTextDistances(0,0,0,0,n);s.setLineSpacingMode(0,n);s.setLineSpacing(o['size']*o['leading']*.75,n)
    if s.textOverflows(n):overflows.append(name)
    if o.get('link'):
     ann=s.createText(x,y,o['w']*.75,o['h']*.75,name+'_link');s.setURIAnnotation(o['link'],ann)
   elif k in ['rect','circle']:
    n=(s.createEllipse if k=='circle' else s.createRect)(x,y,o['w']*.75,o['h']*.75,name)
    s.setFillColor('c'+o['color'],n);s.setLineColor('None',n)
   elif k=='line':
    n=s.createLine(x,y,o['x2']*.75,o['y2']*.75,name);s.setLineColor('c'+o['color'],n);s.setLineWidth(o['width']*.75,n)
   else:
    n=s.createImage(x,y,o['w']*.75,o['h']*.75,name);s.loadImage(o['path'],n);s.setScaleImageToFrame(True,False,n)
 s.setInfo('Cristián Labra Olivares','Educación III · propuesta D','Piloto de composición editorial')
 s.saveDocAs(str(prefix.with_suffix('.sla')))
 pdf=s.PDFfile();pdf.file=str(prefix.with_suffix('.pdf'));pdf.pages=list(range(1,10));pdf.version=15;pdf.compress=True;pdf.quality=0;pdf.resolution=300;pdf.embedPDF=True
 pdf.fonts=['Fira Sans Regular','Fira Sans Medium','Fira Sans SemiBold'];pdf.save()
 prefix.with_suffix('.overflow.json').write_text(json.dumps(overflows))
 os._exit(0)
except BaseException:
 (P/'out/scribus-error.log').write_text(traceback.format_exc())
 os._exit(1)
