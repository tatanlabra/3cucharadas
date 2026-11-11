import hashlib,json,re,subprocess,unicodedata,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(s):return ''.join(unicodedata.normalize('NFKC',s).replace('−','-').replace('–','-').replace('\u00ad','').split())
def fmt(n):return ('+' if n>0 else '−' if n<0 else '')+f'{abs(n):.2f}'.replace('.',',')
def expected(d):
 values=[d[k] for k in ['kicker','title','body','takeaway','note']]
 values+=d.get('items',[])+d.get('steps',[])+d.get('branches',[])
 for x in d.get('cards',[]):values += [x['label'],x['text']]
 for x in d.get('rows',[]):values += [x['label']]+[fmt(x[k]) for k in ['value','lo','hi']]
 if 'interval' in d:values += [d['interval'],'puntos porcentuales']
 return values

def source_errors(repo,content,lock):
 c=json.loads(content.read_text());l=json.loads(lock.read_text());errors=[]
 if sha(content)!=l['content_sha256']:errors.append('CONTENT_CHANGED_AFTER_FREEZE')
 source=(repo/c['source']).resolve()
 if not source.is_relative_to(repo):raise ValueError('Source outside repository')
 if sha(source)!=l['source_sha256']:errors.append('SOURCE_CHANGED_AFTER_FREEZE')
 if not c.get('slides'):errors.append('NO_SLIDES')
 text=source.read_text()
 for d in c['slides']:
  if d['kind'] not in ['cover','cta','chart','method','diagram','limits','actions']:errors.append('UNKNOWN_SLIDE_KIND')
  for key in ['kicker','title','body','takeaway','note','source_claims']:
   if not d.get(key):errors.append('MISSING_FIELD '+key)
  for claim in d['source_claims']:
   if '<!-- CLAIM: '+claim+' -->' not in text:errors.append('MISSING_ANCHOR '+claim)
  for row in d.get('rows',[]):
   if not d['domain'][0]<=row['lo']<=row['value']<=row['hi']<=d['domain'][1]:errors.append('INTERVAL_OUT_OF_DOMAIN')
   for k in ['value','lo','hi']:
    if f'{abs(row[k]):.2f}'.replace('.',',') not in text:errors.append('NUMBER_NOT_IN_SOURCE')
 for name,digest in l['assets'].items():
  if sha(repo/name)!=digest:errors.append('SOURCE_ASSET_CHANGED')
 return errors

def pdf_report(pdf,content):
 c=json.loads(content.read_text());r=PdfReader(pdf);errors=[]
 if len(r.pages)!=len(c['slides']):errors.append('PAGE_COUNT')
 for i,page in enumerate(r.pages[:len(c['slides'])]):
  t=norm(page.extract_text())
  if not t:errors.append(f'RASTER_ONLY {i+1}')
  for s in expected(c['slides'][i]):
   if norm(s) not in t:errors.append(f'MISSING_TEXT {i+1}: {s}')
  if abs(float(page.mediabox.width)-810)>.2 or abs(float(page.mediabox.height)-1012.5)>.2:errors.append('PAGE_SIZE')
 fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True).splitlines()[2:]
 if not fonts:errors.append('NO_EMBEDDED_FONTS')
 for f in fonts:
  if not re.search(r'\s+yes\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$',f):errors.append('FONT_NOT_EMBEDDED')
  if 'FiraSans' not in f and 'Fira-Sans' not in f:errors.append('UNEXPECTED_FONT')
 links=[str(a.get_object().get('/A',{}).get('/URI','')) for page in r.pages for a in page.get('/Annots',[])]
 if c['url'] not in links:errors.append('ARTICLE_LINK_MISSING')
 xml=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'],text=True))
 for i,pg in enumerate(xml.findall('.//{*}page')):
  for w in pg.findall('.//{*}word'):
   x,y,x2,y2=[float(w.attrib[k]) for k in ['xMin','yMin','xMax','yMax']]
   if x<0 or y<0 or x2>810.5 or y2>1013:errors.append(f'TEXT_OUTSIDE {i+1}')
 return {'passed':not errors,'errors':errors,'pages':len(r.pages),'fonts':fonts,'links':links,'pdf_sha256':sha(pdf),'tagged':bool(r.trailer['/Root'].get('/StructTreeRoot'))}
