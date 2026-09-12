from pathlib import Path
exec(Path('/tmp/3c-hero-browser/run_matrix.py').read_text().split('results=[]')[0])
routes=[('/','home-es'),('/en/','home-en'),('/datos/territorio/avaluos-ii-brecha-residencial/','related-es'),('/en/datos/territorio/avaluos-ii-brecha-residencial/','related-en'),('/year-archive/','archive-es'),('/en/year-archive/','archive-en')]
results=[]
for width in [390,1440]:
 ab('set','viewport',str(width),'900','1')
 for url,name in routes:
  ab('open','http://127.0.0.1:4038'+url)
  for theme in ['light','academic-night']:
   if evaluate('document.documentElement.dataset.theme')!=theme:ab('click','[data-theme-toggle]')
   data=evaluate(r'''(async()=>{
    const articles=[...document.querySelectorAll('.archive__item')];
    for(const i of document.querySelectorAll('.archive__item-teaser img')){i.scrollIntoView({block:'center'});await new Promise(r=>setTimeout(r,120));try{await i.decode()}catch(e){}}
    return {url:location.href,theme:document.documentElement.dataset.theme,width:innerWidth,dpr:devicePixelRatio,overflow:document.documentElement.scrollWidth-innerWidth,cards:articles.map(a=>{let h=a.querySelector('.archive__item-title'),i=a.querySelector('img');return {title:h?.textContent.trim(),title_scroll:h?.scrollWidth,title_client:h?.clientWidth,title_rect:h?.getBoundingClientRect().toJSON(),font_size:getComputedStyle(h).fontSize,text_color:getComputedStyle(h).color,img:i?{src:i.getAttribute('src'),srcset:i.getAttribute('srcset'),sizes:i.getAttribute('sizes'),current:i.currentSrc,complete:i.complete,natural_width:i.naturalWidth}:null}}),html:articles.map(a=>a.outerHTML).join('\n')};
   })()''')
   failures=[]
   if not data['cards']:failures.append('empty card inventory')
   for c in data['cards']:
    if not c['title'] or c['title_scroll']>c['title_client']+1:failures.append('card title missing/overflow')
    img=c['img']
    if not name.startswith('archive'):
     if not img or not img['srcset'] or 'teaser-mobile-640x360.webp 640w' not in img['srcset']:failures.append('mobile srcset missing')
     elif not img['complete'] or not img['natural_width'] or not img['current'].endswith('/teaser-mobile-640x360.webp'):failures.append('mobile candidate not loaded')
   if data['overflow']>1:failures.append('global overflow')
   data['fragment_sha256']=hashlib.sha256(data.pop('html').encode()).hexdigest()
   axe=ab('a11y','--selector','.archive__item')
   if axe['counts']['violations']:failures.append('axe card violations')
   evaluate("document.querySelector('.archive__item').scrollIntoView({block:'start'})")
   shot=SHOTS/f'{name}-{width}-{theme}.png';ab('screenshot',str(shot))
   built=Path('/tmp/3c-heroes-cardfix-site')/url.lstrip('/')/'index.html'
   r={'id':f'{name}-{width}-{theme}','observed':data,'axe':{k:axe[k] for k in ['axeVersion','counts','violations','incomplete']},'html_file_sha256':hashlib.sha256(built.read_bytes()).hexdigest(),'screenshot':'screenshots/'+shot.name,'failures':failures};results.append(r)
   (OUT/'cards-after.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'completed':len(results),'id':r['id'],'failures':failures,'axe':axe['counts']}),flush=True)
print('CARDS COMPLETE',len(results),'failed',sum(bool(r['failures']) for r in results),flush=True)
