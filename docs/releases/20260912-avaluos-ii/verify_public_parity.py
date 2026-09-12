import json,hashlib,subprocess,zipfile,re,datetime,sys
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
base='https://3cucharadas.cl'
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.assets=set();self.text=[];self.feed(s)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for field in ('src','poster'):
   if field in a:self.assets.add(a[field])
  if 'srcset' in a:self.assets.update(p.strip().split()[0] for p in a['srcset'].split(',') if p.strip())
  if tag=='link' and a.get('rel')=='stylesheet':self.assets.add(a.get('href',''))
  for u in re.findall(r'url\([\'\"]?([^\)\'\"]+)',a.get('style','')):self.assets.add(u)
 def handle_data(self,data):self.text.append(data)
def fetch(url):
 p=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','35',url],capture_output=True)
 if p.returncode:raise RuntimeError(f'{url}: curl {p.returncode}: {p.stderr.decode()[:200]}')
 return p.stdout
z=zipfile.ZipFile('/tmp/3c-release-artifacts.zip')
paths=['/datos/territorio/avaluos-ii-brecha-residencial/','/en/datos/territorio/avaluos-ii-brecha-residencial/','/ai-transparency/','/en/ai-transparency/','/catastro_sii_brecha/']
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pipeline':2843148339,'sha':'b46381156ed259bbbdc2aea1e615ca3596174eb8','artifact_sha256':hashlib.sha256(Path('/tmp/3c-release-artifacts.zip').read_bytes()).hexdigest(),'pages':[],'assets':[],'errors':[]}
assets={}
for path in paths:
 try:
  expected=z.read('public'+path+'index.html').decode();actual=fetch(base+path).decode()
  ep,ap=Page(expected),Page(actual)
  def localrefs(p):
   return {urlsplit(urljoin(base+path,u)).path for u in p.assets if urlsplit(urljoin(base+path,u)).netloc=='3cucharadas.cl'}
  missing=sorted(localrefs(ep)-localrefs(ap))
  # Text comparison collapses whitespace only; timestamp/cachebuster markup is not evidence of a content difference.
  norm=lambda p:re.sub(r'\s+',' ',' '.join(p.text)).strip()
  text_match=norm(ep)==norm(ap)
  report['pages'].append({'path':path,'http_status':200,'text_matches_artifact':text_match,'missing_asset_references':missing,'html_sha256':hashlib.sha256(actual.encode()).hexdigest()})
  if missing or not text_match:report['errors'].append(path+': rendered text or asset references differ')
  for u in ap.assets:
   url=urljoin(base+path,u);parts=urlsplit(url)
   key='public'+unquote(parts.path)
   if parts.netloc=='3cucharadas.cl' and key in z.namelist():assets[url]=key
 except Exception as e:report['errors'].append(str(e))
def check(item):
 url,key=item
 try:
  b=fetch(url);actual=hashlib.sha256(b).hexdigest();expected=hashlib.sha256(z.read(key)).hexdigest()
  return {'url':url,'bytes':len(b),'sha256':actual,'artifact_sha256':expected,'matches':actual==expected}
 except Exception as e:return {'url':url,'matches':False,'error':str(e)}
with ThreadPoolExecutor(max_workers=4) as ex:report['assets']=list(ex.map(check,sorted(assets.items())))
for a in report['assets']:
 if not a['matches']:report['errors'].append(a['url']+': asset mismatch or unavailable')
report['status']='PASS' if report['pages'] and report['assets'] and not report['errors'] else 'FAIL'
Path(sys.argv[1]).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'pages':len(report['pages']),'assets':len(report['assets']),'errors':report['errors']},indent=2))
sys.exit(0 if report['status']=='PASS' else 1)
