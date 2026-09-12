from pathlib import Path
# Reuse the exact browser transport, extractor and source inventory of the matrix.
exec(Path('/tmp/3c-hero-browser/run_matrix.py').read_text().split('results=[]')[0])
longest=[max([p for p in POSTS if p['fields']['lang']==lang],key=lambda p:len(p['fields']['title'])) for lang in ['es','en']]
extras=[]
for post in longest:
 for requested_theme in ['academic-day','academic-night']:
  ab('set','viewport','320','900','1');ab('open','http://127.0.0.1:4038'+post['url'])
  effective='light' if requested_theme=='academic-day' else 'academic-night'
  if evaluate('document.documentElement.dataset.theme')!=effective:ab('click','[data-theme-toggle]')
  r=evaluate('('+js+')()');key=post['fields']['lang']+'-320-'+requested_theme
  for field in ['hero_html','disclosure_html']:r[field+'_sha256']=hashlib.sha256(r.pop(field).encode()).hexdigest()
  ab('screenshot',str(SHOTS/(key+'.png')))
  ab('focus','#ai-disclosure summary');ab('press','Enter')
  axe=ab('a11y','--selector','.page__hero--editorial, #ai-disclosure')
  extras.append({'kind':'320px-longest-title','id':key,'observed':r,'axe':{k:axe[k] for k in ['axeVersion','counts','violations','incomplete']}})
# Native browser accelerator test; record measured effect, never assume zoom.
ab('set','viewport','1440','900','1');ab('open','http://127.0.0.1:4038'+longest[0]['url']);ab('press','Control+0')
before=evaluate('({width:innerWidth,dpr:devicePixelRatio,visual_scale:visualViewport.scale})')
for _ in range(5):ab('press','Control+Equal')
after=evaluate('({width:innerWidth,dpr:devicePixelRatio,visual_scale:visualViewport.scale})')
(OUT/'native-zoom-probe.json').write_text(json.dumps({'before':before,'after':after,'keys':'Control+0 then five Control+Equal','actual_native_200_percent_observed':after['width']==before['width']/2},indent=2)+'\n')
ab('press','Control+0')
for post in longest:
 for requested_theme in ['academic-day','academic-night']:
  # 1440 physical px / 2 = 720 CSS px, DPR2: explicit reflow/scale emulation.
  ab('set','viewport','720','450','2');ab('open','http://127.0.0.1:4038'+post['url'])
  effective='light' if requested_theme=='academic-day' else 'academic-night'
  if evaluate('document.documentElement.dataset.theme')!=effective:ab('click','[data-theme-toggle]')
  r=evaluate('('+js+')()');key=post['fields']['lang']+'-200percent-reflow-'+requested_theme
  for field in ['hero_html','disclosure_html']:r[field+'_sha256']=hashlib.sha256(r.pop(field).encode()).hexdigest()
  ab('screenshot',str(SHOTS/(key+'.png')))
  ab('focus','#ai-disclosure summary');ab('press','Enter');axe=ab('a11y','--selector','.page__hero--editorial, #ai-disclosure')
  extras.append({'kind':'200percent-equivalent-reflow-emulation','id':key,'setup':'720 CSS viewport,450 CSS height,DPR2 ->1440x900physical; native browser zoom only if native-zoom-probe says observed','observed':r,'axe':{k:axe[k] for k in ['axeVersion','counts','violations','incomplete']}})
(OUT/'extras.json').write_text(json.dumps(extras,indent=2)+'\n')
# A reversible browser-only negative control for the one-h1 criterion.
before=evaluate("document.querySelector('.page__hero--editorial').outerHTML")
evaluate("const n=document.querySelector('h1').cloneNode(true);n.id='qa-duplicate-title';document.querySelector('.page__hero--editorial .wrapper').append(n)")
red=evaluate('('+js+')()');evaluate("document.querySelector('#qa-duplicate-title').remove()")
green=evaluate('('+js+')()');after=evaluate("document.querySelector('.page__hero--editorial').outerHTML")
(OUT/'negative-control.json').write_text(json.dumps({'mutation':'duplicate h1 in live isolated browser DOM only','red_h1_count':red['h1_count'],'green_h1_count':green['h1_count'],'restored_identical_sha256':before==after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()},indent=2)+'\n')
for kind in ['mobile-light','mobile-dark','desktop-light','desktop-dark']:
 ab('set','viewport','1620','1000','1');ab('open','file:///tmp/3c-hero-browser/contact-'+kind+'.html');ab('screenshot','--full',str(OUT/('contact-'+kind+'.png')))
print('EXTRAS COMPLETE',len(extras),flush=True)
