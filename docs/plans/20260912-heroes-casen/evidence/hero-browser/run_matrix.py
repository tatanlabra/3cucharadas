import json,subprocess,pathlib,hashlib,time,datetime,sys
OUT=pathlib.Path('/tmp/3c-hero-browser');SHOTS=OUT/'screenshots';SHOTS.mkdir(exist_ok=True)
POSTS=json.loads((OUT/'inventory.json').read_text())
LOG=(OUT/'commands.jsonl').open('a')
def ab(*args):
 argv=['agent-browser','--session','heroes-all',*args,'--json']
 p=subprocess.run(argv,text=True,capture_output=True,timeout=80)
 try: d=json.loads(p.stdout)
 except Exception: raise RuntimeError(f'Invalid CLI JSON {args}: {p.returncode} {p.stdout[:300]} {p.stderr[:300]}')
 LOG.write(json.dumps({'argv':argv,'exit_code':p.returncode,'success':d.get('success'),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n');LOG.flush()
 if p.returncode or not d.get('success'): raise RuntimeError(f'CLI error {args}: {d}')
 return d.get('data',{})
def evaluate(js):return ab('eval',js)['result']
js=r'''async () => {
 const hero=document.querySelector('.page__hero--editorial'),img=hero?.querySelector('picture img'),d=document.querySelector('#ai-disclosure'),title=hero?.querySelector('h1'),caption=hero?.querySelector('.page__hero-caption');
 if(img)try{await img.decode()}catch(e){}
 const rect=e=>e?.getBoundingClientRect().toJSON();
 return {url:location.href,document_title:document.title,lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,width:innerWidth,dpr:devicePixelRatio,h1_count:document.querySelectorAll('h1').length,hero_count:document.querySelectorAll('.page__hero--editorial').length,hero_rect:rect(hero),hero_scroll_width:hero?.scrollWidth,hero_client_width:hero?.clientWidth,title_rect:rect(title),title_text:title?.textContent.trim(),caption:caption?.textContent.trim(),caption_href:caption?.querySelector('a')?.getAttribute('href'),image:img?{src:img.getAttribute('src'),srcset:img.getAttribute('srcset'),sizes:img.getAttribute('sizes'),current:img.currentSrc,complete:img.complete,natural_width:img.naturalWidth,alt:img.getAttribute('alt'),aria_hidden:img.closest('picture').getAttribute('aria-hidden')}:null,preloads:[...document.querySelectorAll('link[rel=preload][as=image]')].map(x=>({href:x.getAttribute('href'),srcset:x.getAttribute('imagesrcset'),sizes:x.getAttribute('imagesizes')})),disclosure_count:document.querySelectorAll('#ai-disclosure').length,disclosure_level:d?.dataset.aiLevel,disclosure_text:d?.textContent.trim(),components:[...d?.querySelectorAll('[data-ai-component]')||[]].map(x=>({component:x.dataset.aiComponent,origin:x.dataset.aiOrigin})),page_overflow:document.documentElement.scrollWidth-innerWidth,hero_overflow_nodes:[...hero?.querySelectorAll('*')||[]].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.left<-.5||r.right>innerWidth+.5)}).map(e=>e.tagName+'.'+e.className),hero_html:hero?.outerHTML,disclosure_html:d?.outerHTML};
}'''
results=[]
for width in [390,1440]:
 ab('set','viewport',str(width),'900')
 for post in POSTS:
  ab('open','http://127.0.0.1:4038'+post['url'])
  for theme in ['academic-day','academic-night']:
   key=f"{post['fields']['ref']}-{post['fields']['lang']}-{width}-{theme}"
   effective_theme='light' if theme=='academic-day' else 'academic-night'
   if evaluate("document.documentElement.dataset.theme")!=effective_theme:ab('click','[data-theme-toggle]')
   evaluate("document.querySelector('#ai-disclosure').open=false;window.scrollTo(0,0)")
   r=evaluate('('+js+')()');f=post['fields'];fail=[]
   if r['theme']!=effective_theme:fail.append('actual UI theme mismatch')
   if r['url']!='http://127.0.0.1:4038'+post['url']:fail.append('wrong page')
   if r['h1_count']!=1 or r['hero_count']!=1:fail.append('hero/title count')
   if r['disclosure_count']!=1 or r['disclosure_level']!=f['ai_disclosure']['level']:fail.append('disclosure level/count')
   origins={c['component']:c['origin'] for c in r['components']}
   if origins!=f['ai_disclosure']['components']:fail.append('component provenance differs')
   expected_image=f['header']['overlay_image_mobile' if width==390 else 'overlay_image']
   if not r['image'] or not r['image']['complete'] or not r['image']['natural_width'] or not r['image']['current'].endswith(expected_image):fail.append('responsive image not loaded/expected')
   if r['image']['alt']!='' or r['image']['aria_hidden']!='true':fail.append('decorative image semantics')
   if r['preloads']!=[{'href':r['image']['src'],'srcset':r['image']['srcset'],'sizes':r['image']['sizes']}]:fail.append('preload mismatch')
   if r['hero_scroll_width']>r['hero_client_width']+1 or r['hero_overflow_nodes']:fail.append('hero horizontal overflow')
   if not r['caption'] or r['caption_href']!='#ai-disclosure':fail.append('caption link absent')
   aihero=origins.get('hero');caption=r['caption'].lower()
   if aihero=='generated' and not any(x in caption for x in ['hecho con ia','made with ai']):fail.append('generated hero caption absent')
   if aihero=='unknown' and not any(x in caption for x in ['origen de imagen no documentado','image origin undocumented']):fail.append('unknown hero caption misleading')
   tool=post['catalog_piece'].get('provenance',{}).get('tool');text=r['disclosure_text']
   if tool and tool not in text:fail.append('documented tool absent')
   if not tool and any(x in text for x in ['Herramienta documentada:','Documented tool:']):fail.append('undocumented tool claim')
   for field in ['hero_html','disclosure_html']:r[field+'_sha256']=hashlib.sha256(r.pop(field).encode()).hexdigest()
   ab('screenshot','.page__hero--editorial',str(SHOTS/(key+'.png')))
   ab('focus','#ai-disclosure summary');ab('press','Enter')
   keyboard=evaluate("({open:document.querySelector('#ai-disclosure').open,focused:document.activeElement===document.querySelector('#ai-disclosure summary'),outline:getComputedStyle(document.activeElement).outlineStyle,outline_width:getComputedStyle(document.activeElement).outlineWidth})")
   if not keyboard['open'] or not keyboard['focused'] or keyboard['outline']=='none' or keyboard['outline_width']=='0px':fail.append('keyboard details/focus')
   axe=ab('a11y','--selector','.page__hero--editorial, #ai-disclosure')
   if axe['counts']['violations']:fail.append('axe component violations')
   ab('press','Enter')
   if evaluate("document.querySelector('#ai-disclosure').open"):fail.append('keyboard close failed')
   record={'id':key,'post_file':post['file'],'metadata_sha256':post['metadata_sha256'],'observed':r,'keyboard':keyboard,'axe':{k:axe[k] for k in ['axeVersion','counts','violations','incomplete']},'screenshot':'screenshots/'+key+'.png','failures':fail}
   results.append(record);(OUT/'matrix.json').write_text(json.dumps(results,indent=2)+'\n')
   print(json.dumps({'completed':len(results),'id':key,'failures':fail,'axe':axe['counts'],'global_overflow':r['page_overflow']}),flush=True)
print('MATRIX COMPLETE',len(results),'failed cases',sum(bool(r['failures']) for r in results),flush=True)
