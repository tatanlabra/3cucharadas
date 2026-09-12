import pathlib,json,hashlib
P=pathlib.Path('/tmp/3c-hero-browser-first-person');ns={};exec((P/'run_matrix.py').read_text().split('\nresults=[]')[0],ns);ab=ns['ab'];evaluate=ns['evaluate'];js=ns['js'];posts=ns['POSTS'];results=[]
longest=[max([p for p in posts if p['fields']['lang']==lang],key=lambda p:len(p['fields']['title'])) for lang in ['es','en']]
for width,height,dpr,label in [(320,900,1,'320'),(720,450,2,'200percent-equivalent-reflow')]:
 for p in longest:
  for requested in ['academic-day','academic-night']:
   ab('set','viewport',str(width),str(height),str(dpr));ab('open','http://127.0.0.1:4038'+p['url']);theme='light' if requested=='academic-day' else 'academic-night'
   if evaluate('document.documentElement.dataset.theme')!=theme:ab('click','[data-theme-toggle]')
   evaluate('(async()=>{await document.fonts.ready;await new Promise(r=>setTimeout(r,600));window.scrollTo(0,0)})()')
   r=evaluate('('+js+')()');fail=[]
   if r['h1_count']!=1 or r['disclosure_tag']!='P' or r['badge_count']!=0:fail.append('structure')
   if r['hero_overflow_nodes'] or r['page_overflow']!=0:fail.append('overflow')
   if not r['image']['complete'] or not r['image']['natural_width']:fail.append('image')
   for field in ['hero_html','disclosure_html']:r[field+'_sha256']=hashlib.sha256(r.pop(field).encode()).hexdigest()
   key=p['fields']['lang']+'-'+label+'-'+requested;ab('screenshot',str(P/'screenshots'/(key+'.png')));axe=ab('a11y','--selector','.page__hero--editorial, #ai-disclosure')
   if axe['counts']['violations']:fail.append('axe')
   results.append({'id':key,'observed':r,'failures':fail,'axe':{k:axe[k]for k in ['axeVersion','counts','violations','incomplete']},'scope':'reflow equivalent, no native browser UI zoom claim' if dpr==2 else '320CSS'});(P/'extras.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
for kind,width,theme in [('mobile-light',390,'academic-day'),('mobile-dark',390,'academic-night'),('desktop-light',1440,'academic-day'),('desktop-dark',1440,'academic-night')]:
 cards=[]
 for p in posts:
  name=f"{p['fields']['ref']}-{p['fields']['lang']}-{width}-{theme}"
  cards.append('<figure><img src="screenshots/'+name+'.png"><figcaption>'+name+'</figcaption></figure>')
 w=390 if width==390 else 720;cols=4 if width==390 else 2
 html='<!doctype html><html lang="es"><meta charset="utf-8"><style>body{background:#ddd;font:14px sans-serif;margin:12px}main{display:grid;grid-template-columns:repeat('+str(cols)+','+str(w)+'px);gap:10px}figure{margin:0;background:white}img{display:block;width:'+str(w)+'px;height:auto}figcaption{padding:6px;overflow-wrap:anywhere}</style><h1>Primera persona: '+kind+'</h1><main>'+''.join(cards)+'</main>'
 path=P/('contact-'+kind+'.html');path.write_text(html);ab('set','viewport','1620','1000','1');ab('open',path.as_uri());ab('screenshot','--full',str(P/('contact-'+kind+'.png')))
ab('close');print('EXTRAS',len(results),'failures',sum(bool(r['failures'])for r in results))
