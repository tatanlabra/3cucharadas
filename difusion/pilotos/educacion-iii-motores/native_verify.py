#!/usr/bin/env python3
"""Content, native text, page bounds and text collisions; visual QA remains separate."""
import argparse,json,subprocess,re,sys,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from verify import check_source,norm
from native_build import P,CODE
from native_html import fmt

def expected(d):
 out=[d[k] for k in ['kicker','title','body','takeaway','note']]
 out+=d.get('items',[])+d.get('steps',[])+d.get('branches',[])
 for r in d.get('cards',[]):out += [r['label'],r['text']]
 for r in d.get('rows',[]):out += [r['label']]+[fmt(r[k]) for k in ['value','lo','hi']]
 if 'interval' in d:out += [d['interval'],'puntos porcentuales']
 return out

def check(engine,pdf,c):
 _,errors=check_source();r=PdfReader(pdf)
 if pdf.with_suffix('.receipt.json').exists():
  build=json.loads(pdf.with_suffix('.receipt.json').read_text())
  if build.get('status')!='success' or build.get('pdf_sha256')!=hashlib.sha256(pdf.read_bytes()).hexdigest():errors.append('STALE_OR_FAILED_BUILD')
 if len(r.pages)!=9:errors.append('PAGE_COUNT '+str(len(r.pages)))
 for i,page in enumerate(r.pages):
  if i>=9:break
  text=norm(page.extract_text()).replace('\u2212','-')
  if not text:errors.append(f'RASTER_ONLY {i+1}')
  for value in expected(c['slides'][i]):
   if norm(value) not in text:errors.append(f'MISSING_TEXT {i+1}: {value}')
  if abs(float(page.mediabox.width)-810)>.2 or abs(float(page.mediabox.height)-1012.5)>.2:errors.append(f'PAGE_SIZE {i+1}')
 fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True).splitlines()[2:]
 if not fonts:errors.append('NO_EMBEDDED_FONTS')
 for f in fonts:
  if not re.search(r'\s+yes\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',f):errors.append('FONT_NOT_EMBEDDED '+f)
  if 'FiraSans' not in f and 'Fira-Sans' not in f:errors.append('UNEXPECTED_FONT '+f)
 root=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'],text=True));collisions=[]
 for i,pg in enumerate(root.findall('.//{*}page'),1):
  words=pg.findall('.//{*}word')
  for j,w in enumerate(words):
   x,y,x2,y2=[float(w.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
   if x<0 or y<0 or x2>810.5 or y2>1013:errors.append(f'TEXT_OUTSIDE {i}: {w.text}')
   for v in words[j+1:]:
    a,b,a2,b2=[float(v.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
    # Heuristic only: Fira PDF font boxes include whitespace. Compare central 64% vertically; visual review remains mandatory.
    if min(x2,a2)-max(x,a)>2 and min(y2-(y2-y)*.18,b2-(b2-b)*.18)-max(y+(y2-y)*.18,b+(b2-b)*.18)>2:collisions.append(f'{i}: {w.text} / {v.text}')
 if collisions:errors += ['TEXT_COLLISION '+x for x in collisions]
 links=[str(a.get_object().get('/A',{}).get('/URI','')) for p in r.pages for a in p.get('/Annots',[])]
 if c['url'] not in links:errors.append('ARTICLE_LINK_MISSING')
 if engine=='scribus' and pdf.with_suffix('.overflow.json').exists():
  overflow=json.loads(pdf.with_suffix('.overflow.json').read_text())
  if overflow:errors += ['FRAME_OVERFLOW '+str(x) for x in overflow]
 if engine=='beamer' and pdf.with_suffix('.log').exists():
  warnings=re.findall(r'Overfull[^\n]+',pdf.with_suffix('.log').read_text())
  if warnings:errors+=warnings
 return {'engine':engine,'pdf':str(pdf),'passed':not errors,'errors':errors,'pages':len(r.pages),'bytes':pdf.stat().st_size,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'fonts':fonts,'tagged':bool(r.trailer['/Root'].get('/StructTreeRoot'))}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--engine',choices=[*CODE,'all'],default='all');ap.add_argument('--root',type=Path,default=P/'out/native');ap.add_argument('--content',type=Path,default=P/'content.json');ap.add_argument('--pdf',type=Path);ap.add_argument('--receipt',type=Path);a=ap.parse_args()
 try:
  c=json.loads(a.content.read_text());results=[check(e,a.pdf or a.root/(CODE[e]+'.pdf'),c) for e in (CODE if a.engine=='all' else [a.engine])];r={'passed':all(x['passed'] for x in results),'results':results}
  if a.receipt:a.receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2))
  print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['passed'] else 1
 except Exception as e:print('PRECONDITION_ERROR '+str(e),file=sys.stderr);return 3
if __name__=='__main__':sys.exit(main())
