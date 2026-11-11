import sys,json,urllib.request,urllib.parse,hashlib
from pathlib import Path
sys.path.insert(0,'/home/ende/Descargas/programaciones/activos/3cucharadas/difusion/src')
from cucharadas_difusion.networks import load_secrets,BlueskyClient
BASE=Path('/home/ende/Descargas/programaciones/activos/3cucharadas/docs/plans/20261110-difusion-iv-audio-iii-iv/evidence');BASE.mkdir(exist_ok=True)
url='https://3cucharadas.cl/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/'
texts={
'es':'Corrección del Post IV: la revisión reemplaza resultados y figuras anteriores. Los contrastes de acceso total admiten diferencias negativas y positivas; no identifican efectos causales del cierre ni una caída inequívoca en IP/CFT en la era moderna.',
'en':'Correction to Part IV: the revision replaces earlier results and figures. Overall access contrasts allow negative and positive differences; they identify neither causal closure effects nor an unambiguous decline in technical/professional enrolment in the modern era.'}
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'3cucharadas-difusion/0.2'}),timeout=30) as r:return json.load(r)
def save(name,d): (BASE/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
live='--live' in sys.argv
if not live:
 for lang,id in [('es','117577401287171882'),('en','117577401315592948')]:
  d=get('https://mastodon.social/api/v1/statuses/'+id);save('mastodon-before-'+lang+'.json',d);print('Mastodon',lang,d['content'])
 did=get('https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=labra.bsky.social')['did']
 uris=['at://'+did+'/app.bsky.feed.post/'+k for k in ['3mzqvfxyl5s2n','3mzqvfzpsd72p']]
 q=urllib.parse.urlencode([('uris',u) for u in uris]); d=get('https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?'+q);save('bluesky-before.json',d)
 for p in d['posts']:print('Bluesky',p['uri'],p['record']['text'])
 for l,t in texts.items():print('COPY',l,len(t),t)
 save('correction-copy.json',texts);sys.exit()
secrets=load_secrets()
for lang,id in [('es','117577401287171882'),('en','117577401315592948')]:
 receipt=BASE/('mastodon-corrected-'+lang+'.json')
 if receipt.exists():print('SKIP receipt',lang);continue
 old=json.loads((BASE/('mastodon-before-'+lang+'.json')).read_text())
 body={'status':texts[lang]+' '+(url if lang=='es' else url.replace('.cl/','.cl/en/')),'language':lang,'media_ids':[m['id'] for m in old['media_attachments']]}
 req=urllib.request.Request('https://mastodon.social/api/v1/statuses/'+id,data=json.dumps(body).encode(),method='PUT',headers={'Authorization':'Bearer '+secrets['MASTODON_TOKEN'],'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=30) as r:d=json.load(r)
 save(receipt.name,d);print('EDITED',d['url'])
client=BlueskyClient(secrets)._client()
old=json.loads((BASE/'bluesky-before.json').read_text())['posts']
root=next(x for x in old if x['uri'].endswith('/3mzqvfxyl5s2n'))
for lang,suffix in [('es','3mzqvfxyl5s2n'),('en','3mzqvfzpsd72p')]:
 receipt=BASE/('bluesky-correction-'+lang+'.json')
 if receipt.exists(): print('SKIP receipt',lang);continue
 parent=next(x for x in old if x['uri'].endswith('/'+suffix))
 keysfile=BASE/'bluesky-correction-rkeys.json'
 if not keysfile.exists():
  import time
  alphabet='234567abcdefghijklmnopqrstuvwxyz'
  def tid(n):
   out=''
   for _ in range(13): out=alphabet[n&31]+out; n>>=5
   return out
  n=(time.time_ns()//1000)<<10
  save(keysfile.name,{'es':tid(n),'en':tid(n+1)})
 rkey=json.loads(keysfile.read_text())[lang]
 record={'$type':'app.bsky.feed.post','text':texts[lang],'langs':[lang],'createdAt':client.get_current_time_iso(),'reply':{'root':{'uri':root['uri'],'cid':root['cid']},'parent':{'uri':parent['uri'],'cid':parent['cid']}}}
 result=client.com.atproto.repo.create_record({'repo':client.me.did,'collection':'app.bsky.feed.post','rkey':rkey,'record':record})
 d={'uri':result.uri,'cid':result.cid,'url':'https://bsky.app/profile/labra.bsky.social/post/'+rkey,'text':texts[lang]};save(receipt.name,d);print('POSTED',d['url'])
