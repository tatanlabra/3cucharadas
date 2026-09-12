import subprocess,json,time,hashlib
from pathlib import Path
ROOT=Path('/home/ende/Descargas/programaciones/activos/3cucharadas')
OUT=ROOT/'docs/plans/20260912-heroes-casen/evidence/editorial-browser'
SESSION='editorial-qa'

def call(*args, timeout=50):
 p=subprocess.run(['agent-browser','--session',SESSION,*args],capture_output=True,text=True,timeout=timeout)
 if p.returncode:
  raise RuntimeError(f'{args}: {p.returncode}: {p.stderr} {p.stdout}')
 return p.stdout.strip()
def ev(code):return json.loads(call('eval',code))
rows=json.loads((ROOT.parent/'catastros_sii/v5_brecha/artifacts/casen_shared_site/estimates.json').read_text())['rows']
expected={r['territory_code']:r for r in rows if r['scope'] in ('national','region') or r['territory_code'] in ('5101','5109')}
results=[]
for lang in ('es','en'):
 for width in (390,1440):
  for theme in ('light','academic-night'):
   case=f'{lang}-{width}-{theme}'
   url='http://127.0.0.1:4004/'+('en/' if lang=='en' else '')+'datos/territorio/avaluos-ii-brecha-residencial/'
   call('set','viewport',str(width),'900');call('open',url)
   ev(f'(() => {{if(document.documentElement.dataset.theme!=={json.dumps(theme)})document.querySelector("[data-theme-toggle]").click();return document.documentElement.dataset.theme}})()')
   ev('(() => {for(const r of document.querySelectorAll("tr[data-territory]")){const d=r.closest("details");if(d&&!d.open)d.querySelector("summary").click();r.closest("div[role=region]").dataset.editorialQa="table";}for(const i of document.querySelectorAll("img")){if(/gap-top15|casen-shared-site|monetary-top15/.test(i.src))i.closest("figure").dataset.editorialQa="figure";}return true})()')
   record=ev('''(async () => {
    const images=[...document.querySelectorAll('img')].filter(i=>/gap-top15|casen-shared-site|monetary-top15/.test(i.src)&&getComputedStyle(i).display!=='none');
    const figures=[];
    for(const i of images){i.scrollIntoView({block:'center'});await i.decode();const w=i.parentElement;const response=await fetch(i.currentSrc);const bytes=await response.arrayBuffer();const svg=new TextDecoder().decode(bytes);const sha=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(v=>v.toString(16).padStart(2,'0')).join('');w.focus();const focused=document.activeElement===w;const outline=getComputedStyle(w).outline;w.scrollLeft=0;const before=w.scrollLeft;w.scrollLeft=100;const scrollWorks=w.scrollLeft>before;w.scrollLeft=0;
     figures.push({src:i.getAttribute('src'),currentSrc:i.currentSrc,sha256:sha,width:i.getBoundingClientRect().width,height:i.getBoundingClientRect().height,naturalWidth:i.naturalWidth,loaded:i.complete&&i.naturalWidth>0,wrapperWidth:w.clientWidth,wrapperScrollWidth:w.scrollWidth,tabindex:w.tabIndex,focused,outline,scrollWorks,embeddedFonts:(svg.match(/data:font\\/woff2;base64,/g)||[]).length,selectableTextNodes:(svg.match(/<text /g)||[]).length,alt:i.alt});}
    const tables=[...document.querySelectorAll('tr[data-territory]')].map(r=>({code:r.dataset.territory,cells:[...r.cells].map(c=>c.textContent.trim()),scope:r.cells[0].getAttribute('scope'),containerTabIndex:r.closest('div[role=region]').tabIndex}));
    return {url:location.href,theme:document.documentElement.dataset.theme,viewport:innerWidth,bodyWidth:document.body.scrollWidth,rootWidth:document.documentElement.scrollWidth,figures,tables,disclosureOpen:[...document.querySelectorAll('details')].filter(d=>d.querySelector('tr[data-territory]')).every(d=>d.open)};
   })()''')
   record['case']=case;record['checks']={};record['defects']=[]
   def check(name,ok,detail=''):
    record['checks'][name]=bool(ok)
    if not ok:record['defects'].append({'check':name,'detail':detail})
   check('exact_url',record['url']==url);check('correct_theme',record['theme']==theme)
   check('no_body_overflow',record['bodyWidth']<=width and record['rootWidth']<=width,f"body={record['bodyWidth']}; root={record['rootWidth']}; viewport={width}")
   check('three_visible_figures',len(record['figures'])==3)
   for f in record['figures']:
    name=Path(f['src']).name
    check(name+'-theme',('-dark.svg' in name)==(theme=='academic-night'))
    check(name+'-width',f['width']>=1000)
    check(name+'-loaded',f['loaded'])
    check(name+'-keyboard-focus',f['tabindex']==0 and f['focused'])
    check(name+'-scroll',f['scrollWorks'] or f['wrapperWidth']>=f['width'])
    check(name+'-embedded-fonts',f['embeddedFonts']==2 and f['selectableTextNodes']>10)
    check(name+'-source-hash',f['sha256']==hashlib.sha256((ROOT/f['src'].lstrip('/')).read_bytes()).hexdigest())
   check('19_casen_rows',len(record['tables'])==19)
   check('all_expected_territories',set(r['code'] for r in record['tables'])==set(expected))
   for r in record['tables']:
    e=expected[r['code']];cells=r['cells'];clean=lambda v:v.replace('.','').replace(',','')
    match=cells[0]==e['territory_name'] and int(clean(cells[1]))==e['n_households'] and int(clean(cells[2]))==e['n_missing']
    observed=float(cells[3].replace('%','').replace(',','.').strip());match=match and observed==round(e['estimate']*100,2)
    if e['ci_low'] is None:match=match and cells[4] in ('No corresponde','Not applicable')
    else:
     vals=[float(v.replace('%','').replace(',','.').strip()) for v in cells[4].split('–')]
     match=match and vals==[round(e['ci_low']*100,2),round(e['ci_high']*100,2)]
    check('table-'+r['code'],match and r['scope']=='row' and r['containerTabIndex']==0)
   for kind in ('casen-shared-site','monetary-top15'):
    ev(f'(() => {{const i=[...document.querySelectorAll("img")].find(i=>i.src.includes({json.dumps(kind)})&&getComputedStyle(i).display!=="none");i.parentElement.scrollLeft=0;i.closest("figure").scrollIntoView({{block:"start"}});return true}})()')
    call('screenshot',str(OUT/f'{case}-{kind}.png'))
   if width==390:
    ev('(() => {const i=[...document.querySelectorAll("img")].find(i=>i.src.includes("casen-shared-site")&&getComputedStyle(i).display!=="none");i.parentElement.scrollLeft=i.parentElement.scrollWidth;i.scrollIntoView({block:"end"});return true})()')
    call('screenshot',str(OUT/f'{case}-casen-right-bottom.png'))
   audit=call('a11y','--selector','[data-editorial-qa]','--json',timeout=60)
   (OUT/f'{case}-axe.json').write_text(audit+'\n')
   try:
    ax=json.loads(audit);record['axe_result_keys']=list(ax) if isinstance(ax,dict) else None
   except Exception:record['axe_result_keys']=None
   (OUT/f'{case}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
   results.append(record)
   print(json.dumps({'case':case,'passed':sum(record['checks'].values()),'total':len(record['checks']),'defects':record['defects']},ensure_ascii=False),flush=True)
(OUT/'matrix.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
