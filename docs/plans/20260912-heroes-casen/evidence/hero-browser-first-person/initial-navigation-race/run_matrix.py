import json,subprocess,pathlib,hashlib,time,datetime,sys
OUT=pathlib.Path('/tmp/3c-hero-browser-first-person');SHOTS=OUT/'screenshots';SHOTS.mkdir(exist_ok=True)
POSTS=json.loads((OUT/'inventory.json').read_text())
LOG=(OUT/'commands.jsonl').open('a')
def ab(*args):
 argv=['agent-browser','--session','heroes-first-person',*args,'--json']
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
 return {url:location.href,document_title:document.title,lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,width:innerWidth,dpr:devicePixelRatio,h1_count:document.querySelectorAll('h1').length,hero_count:document.querySelectorAll('.page__hero--editorial').length,hero_rect:rect(hero),hero_scroll_width:hero?.scrollWidth,hero_client_width:hero?.clientWidth,title_rect:rect(title),title_text:title?.textContent.trim(),caption:caption?.textContent.trim(),caption_href:caption?.querySelector('a')?.getAttribute('href'),image:img?{src:img.getAttribute('src'),srcset:img.getAttribute('srcset'),sizes:img.getAttribute('sizes'),current:img.currentSrc,complete:img.complete,natural_width:img.naturalWidth,alt:img.getAttribute('alt'),aria_hidden:img.closest('picture').getAttribute('aria-hidden')}:null,preloads:[...document.querySelectorAll('link[rel=preload][as=image]')].map(x=>({href:x.getAttribute('href'),srcset:x.getAttribute('imagesrcset'),sizes:x.getAttribute('imagesizes')})),disclosure_count:document.querySelectorAll('#ai-disclosure').length,disclosure_level:d?.dataset.aiLevel,disclosure_text:d?.textContent.trim(),components:d?[{component:'text',origin:d.dataset.aiTextOrigin},{component:'hero',origin:d.dataset.aiHeroOrigin}]:[],disclosure_tag:d?.tagName,disclosure_href:d?.querySelector('a')?.getAttribute('href'),badge_count:hero?.querySelectorAll('[data-ai-level]').length,page_overflow:document.documentElement.scrollWidth-innerWidth,hero_overflow_nodes:[...hero?.querySelectorAll('*')||[]].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.left<-.5||r.right>innerWidth+.5)}).map(e=>e.tagName+'.'+e.className),hero_html:hero?.outerHTML,disclosure_html:d?.outerHTML};
}'''

results=[]
for width in [390,1440]:
 ab('set','viewport',str(width),'900','1')
 for post in POSTS:
  for theme in ['academic-day','academic-night']:
   ab('open','http://127.0.0.1:4038'+post['url'])
   key=f"{post['fields']['ref']}-{post['fields']['lang']}-{width}-{theme}"
   effective_theme='light' if theme=='academic-day' else 'academic-night'
   if evaluate("document.documentElement.dataset.theme")!=effective_theme:ab('click','[data-theme-toggle]')
   evaluate("(async()=>{await document.fonts.ready; await new Promise(r=>setTimeout(r,600));window.scrollTo(0,0)})()")
   r=evaluate('('+js+')()');f=post['fields'];fail=[];lang=f['lang'];policy='/en/ai-transparency/' if lang=='en' else '/ai-transparency/'
   if r['theme']!=effective_theme:fail.append('actual UI theme mismatch')
   if r['url']!='http://127.0.0.1:4038'+post['url']:fail.append('wrong page')
   if r['h1_count']!=1 or r['hero_count']!=1:fail.append('hero/title count')
   if r['disclosure_count']!=1 or r['disclosure_level']!=f['ai_disclosure']['level']:fail.append('disclosure level/count')
   if r['disclosure_tag']!='P' or r['badge_count']!=0:fail.append('brief paragraph without old badge')
   if r['disclosure_href']!=policy:fail.append('disclosure policy locale')
   if len(r['disclosure_text'].split())>25:fail.append('disclosure not brief')
   origins={c['component']:c['origin'] for c in r['components']}
   if origins!=f['ai_disclosure']['components']:fail.append('component provenance differs')
   prefixes={'es':{'some_ai':'Preparé este artículo con ayuda de IA.','no_ai':'Preparé este artículo sin IA.','fully_autonomous':'Generé este artículo íntegramente con IA.','not_disclosed':'Aún no he declarado aquí mi uso de IA.'},'en':{'some_ai':'I used AI to help prepare this article.','no_ai':'I made this article without AI.','fully_autonomous':'I generated this article entirely with AI.','not_disclosed':'I have not declared my AI use here yet.'}}
   if not r['disclosure_text'].startswith(prefixes[lang][f['ai_disclosure']['level']]):fail.append('first-person wording')
   expected_image=f['header']['overlay_image_mobile' if width==390 else 'overlay_image']
   if not r['image'] or not r['image']['complete'] or not r['image']['natural_width'] or not r['image']['current'].endswith(expected_image):fail.append('responsive image not loaded/expected')
   if r['image']['alt']!='' or r['image']['aria_hidden']!='true':fail.append('decorative image semantics')
   if r['preloads']!=[{'href':r['image']['src'],'srcset':r['image']['srcset'],'sizes':r['image']['sizes']}]:fail.append('preload mismatch')
   if r['hero_scroll_width']>r['hero_client_width']+1 or r['hero_overflow_nodes']:fail.append('hero horizontal overflow')
   if not r['caption'] or r['caption_href']!=policy+'#'+f['ref']:fail.append('caption localized policy anchor')
   captions={'es':{'generated':'Creé esta portada con IA','human':'Uso una portada de autoría humana','unknown':'No tengo documentado el origen de esta portada'},'en':{'generated':'I created this cover with AI','human':'I use a human-created cover','unknown':'I have not documented this cover’s origin'}}
   if r['caption']!=captions[lang][origins.get('hero','unknown')]:fail.append('caption origin / first person')
   for field in ['hero_html','disclosure_html']:r[field+'_sha256']=hashlib.sha256(r.pop(field).encode()).hexdigest()
   ab('screenshot',str(SHOTS/(key+'.png')))
   axe=ab('a11y','--selector','.page__hero--editorial, #ai-disclosure')
   if axe['counts']['violations']:fail.append('axe component violations')
   ab('focus','#ai-disclosure a')
   keyboard=evaluate("({focused:document.activeElement===document.querySelector('#ai-disclosure a'),outline:getComputedStyle(document.activeElement).outlineStyle,outline_width:getComputedStyle(document.activeElement).outlineWidth})")
   if not keyboard['focused'] or keyboard['outline']=='none' or keyboard['outline_width']=='0px':fail.append('keyboard policy link focus')
   ab('focus','.page__hero-caption a');ab('press','Enter')
   anchor='#'+f['ref'];sel='details[id='+json.dumps(f['ref'])+']'
   ab('focus',sel+' summary');ab('press','Enter')
   p=evaluate("(()=>{const d=document.querySelector("+json.dumps(sel)+");return {url:location.href,lang:document.documentElement.lang,title:document.title,open:d?.open,focused:document.activeElement===d?.querySelector('summary'),text:d?.textContent.trim(),html:d?.outerHTML,components:[...d?.querySelectorAll('[data-ai-component]')||[]].map(x=>({component:x.dataset.aiComponent,origin:x.dataset.aiOrigin}))}})()")
   if p['url']!='http://127.0.0.1:4038'+policy+anchor or p['lang']!=lang:fail.append('keyboard caption navigation policy/anchor/locale')
   if not p['open'] or not p['focused']:fail.append('policy detail keyboard open/focus')
   if {c['component']:c['origin'] for c in p['components']}!=origins:fail.append('policy components mismatch')
   tool=post['catalog_piece'].get('provenance',{}).get('tool')
   if tool and tool not in p['text']:fail.append('documented tool absent from policy')
   if not tool and any(x in p['text'] for x in ['ImageGen','ChatGPT','Gemini','DeepSeek','Codex']):fail.append('undocumented tool claim in policy')
   p['html_sha256']=hashlib.sha256(p.pop('html').encode()).hexdigest()
   policy_axe=ab('a11y','--selector',sel)
   if policy_axe['counts']['violations']:fail.append('policy detail axe violations')
   record={'id':key,'post_file':post['file'],'metadata_sha256':post['metadata_sha256'],'observed':r,'keyboard':keyboard,'policy':p,'axe':{k:axe[k] for k in ['axeVersion','counts','violations','incomplete']},'policy_axe':{k:policy_axe[k] for k in ['axeVersion','counts','violations','incomplete']},'screenshot':'screenshots/'+key+'.png','failures':fail}
   results.append(record);(OUT/'matrix.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
   print(json.dumps({'completed':len(results),'id':key,'failures':fail,'axe':axe['counts'],'policy_axe':policy_axe['counts']}),flush=True)
print('MATRIX COMPLETE',len(results),'failed cases',sum(bool(r['failures']) for r in results),flush=True)
ab('close')
