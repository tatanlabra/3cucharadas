from pathlib import Path
import json,urllib.request,urllib.parse
b=Path('/home/ende/Descargas/programaciones/activos/3cucharadas/docs/plans/20261110-difusion-iv-audio-iii-iv/evidence')
def get(u):
 with urllib.request.urlopen(u,timeout=25) as r:return json.load(r)
copy=json.loads((b/'correction-copy.json').read_text())
for lang,id in [('es','117577401287171882'),('en','117577401315592948')]:
 d=get('https://mastodon.social/api/v1/statuses/'+id)
 assert copy[lang] in d['content']
 (b/('mastodon-verified-'+lang+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print('VERIFIED Mastodon',lang,d['url'])
for lang in ['es','en']:
 r=json.loads((b/('bluesky-correction-'+lang+'.json')).read_text())
 d=get('https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?'+urllib.parse.urlencode({'uris':r['uri']}))
 assert len(d['posts'])==1 and d['posts'][0]['record']['text']==copy[lang]
 (b/('bluesky-verified-'+lang+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print('VERIFIED Bluesky',lang,r['url'])
