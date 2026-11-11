#!/usr/bin/env python3
"""Artifact checks. Failure exits 1; unreadable/precondition failure exits 3."""
import argparse,json,hashlib,subprocess,sys,re,unicodedata,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from render import P,REPO,CODE,scenes

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ''.join(unicodedata.normalize('NFKC',s).replace('−','-').replace('–','-').replace('\u00ad','').split())
def check_source():
 c=json.loads((P/'content.json').read_text());lock=json.loads((P/'source-lock.json').read_text());source=(REPO/c['source']).read_text()
 errors=[]
 if sha(P/'content.json')!=lock['content_sha256']:errors.append('CONTENT_CHANGED_AFTER_FREEZE')
 if sha(REPO/c['source'])!=lock['source_sha256']:errors.append('SOURCE_CHANGED_AFTER_FREEZE')
 if len(c['slides'])!=9:errors.append('SLIDE_COUNT')
 for slide in c['slides']:
  for claim in slide['source_claims']:
   if '<!-- CLAIM: '+claim+' -->' not in source:errors.append('MISSING_ANCHOR '+claim)
  for row in slide.get('rows',[]):
   for k in ['value','lo','hi']:
    value=f"{abs(row[k]):.2f}".replace('.',',')
    if value not in source:errors.append('NUMBER_NOT_IN_SOURCE '+slide['id']+' '+value)
 for asset,h in lock['assets'].items():
  if sha(REPO/asset)!=h:errors.append('ASSET_CHANGED '+asset)
 return c,errors

def check(engine,pdf=None):
 c,errors=check_source();code=CODE[engine];pdf=Path(pdf) if pdf else P/'out'/f'{code}.pdf'
 ops=scenes(c,engine);reader=PdfReader(pdf)
 if len(reader.pages)!=9:errors.append('PAGE_COUNT '+str(len(reader.pages)))
 details=[]
 for i,page in enumerate(reader.pages):
  if i>=9:break
  if abs(float(page.mediabox.width)-810)>.2 or abs(float(page.mediabox.height)-1012.5)>.2:errors.append(f'PAGE_SIZE {i+1}')
  txt=norm(page.extract_text())
  if not txt:errors.append(f'RASTER_ONLY {i+1}')
  for o in ops[i]:
   if o['kind']=='text' and norm(o['text']) not in txt:errors.append(f'MISSING_TEXT {i+1}: '+o['text'].replace('\n',' ')[:110])
  texts=[o for o in ops[i] if o['kind']=='text']
  for j,a in enumerate(texts):
   if a['y']+a['h']>1350:errors.append(f'SCENE_OUTSIDE {i+1}')
   for b in texts[j+1:]:
    if min(a['x']+a['w'],b['x']+b['w'])>max(a['x'],b['x']) and min(a['y']+a['h']-10,b['y']+b['h']-10)>max(a['y'],b['y']):errors.append(f'SCENE_OVERLAP {i+1}: '+a['text'][:25]+' / '+b['text'][:25])
  details.append({'page':i+1,'characters':len(txt)})
 fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True).splitlines()[2:]
 if not fonts:errors.append('NO_EMBEDDED_FONTS')
 for f in fonts:
  if not re.search(r'\s+yes\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',f):errors.append('FONT_NOT_EMBEDDED '+f)
  if 'FiraSans' not in f and 'Fira-Sans' not in f:errors.append('UNEXPECTED_FONT '+f)
 xml=subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'],text=True)
 root=ET.fromstring(xml)
 for i,pg in enumerate(root.findall('.//{*}page')):
  for word in pg.findall('.//{*}word'):
   if float(word.attrib['xMin'])<-.5 or float(word.attrib['yMin'])<-.5 or float(word.attrib['xMax'])>810.5 or float(word.attrib['yMax'])>1013:errors.append(f'PDF_TEXT_OUTSIDE {i+1}: {word.text}')
 links=[]
 for page in reader.pages:
  for ann in page.get('/Annots',[]):
   obj=ann.get_object(); action=obj.get('/A',{})
   if action.get('/URI'):links.append(str(action['/URI']))
 if c['url'] not in links:errors.append('ARTICLE_LINK_MISSING')
 if engine=='scribus' and pdf==P/'out'/f'{code}.pdf':
  overflow=json.loads(pdf.with_suffix('.overflow.json').read_text())
  if overflow:errors.append('SCRIBUS_OVERFLOW '+str(overflow))
 return {'engine':engine,'pdf':str(pdf.relative_to(P)) if pdf.is_relative_to(P) else str(pdf),'pdf_sha256':sha(pdf),'source_sha256':sha(REPO/c['source']),'content_sha256':sha(P/'content.json'),'passed':not errors,'errors':errors,'pages':details,'fonts':fonts,'links':links,'tagged':bool(reader.trailer['/Root'].get('/StructTreeRoot'))}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--engine',choices=[*CODE,'all'],default='all');ap.add_argument('--pdf',type=Path);ap.add_argument('--source-only',action='store_true');ap.add_argument('--receipt',type=Path);a=ap.parse_args()
 try:
  if a.source_only:
   _,errors=check_source();r={'passed':not errors,'errors':errors}
  else:
   items=[check(e,a.pdf) for e in (CODE if a.engine=='all' else [a.engine])];r={'passed':all(x['passed'] for x in items),'results':items}
  if a.receipt:a.receipt.parent.mkdir(exist_ok=True,parents=True);a.receipt.write_text(json.dumps(r,ensure_ascii=False,indent=2))
  print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['passed'] else 1
 except Exception as e:
  print('PRECONDITION_ERROR '+str(e),file=sys.stderr);return 3
if __name__=='__main__':sys.exit(main())
