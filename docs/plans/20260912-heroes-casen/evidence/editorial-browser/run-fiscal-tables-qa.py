import subprocess,json
from pathlib import Path
OUT=Path('/home/ende/Descargas/programaciones/activos/3cucharadas/docs/plans/20260912-heroes-casen/evidence/editorial-browser')
def call(*args):
 p=subprocess.run(['agent-browser','--session','editorial-tables-qa',*args],capture_output=True,text=True,timeout=60)
 if p.returncode:raise RuntimeError(p.stderr+p.stdout)
 return p.stdout
results=[]
for lang in ('es','en'):
 for width in (390,1440):
  for theme in ('light','academic-night'):
   case=f'{lang}-{width}-{theme}'
   call('set','viewport',str(width),'900')
   call('open','http://127.0.0.1:4004/'+('en/' if lang=='en' else '')+'datos/territorio/avaluos-ii-brecha-residencial/')
   values=json.loads(call('eval',f'''(async () => {{if(document.documentElement.dataset.theme!=={json.dumps(theme)})document.querySelector('[data-theme-toggle]').click();await new Promise(r=>setTimeout(r,350));const tables=[...document.querySelectorAll('.avaluos-ii-table')];return tables.map(e=>({{rows:e.querySelectorAll('tbody tr').length,tabindex:e.tabIndex,role:e.getAttribute('role'),name:e.getAttribute('aria-label'),bodyOverflow:document.body.scrollWidth>innerWidth,headers:e.querySelectorAll('th[scope=col]').length,wrappers:[...e.querySelectorAll('.tabla-desliza')].map(w=>({{width:w.clientWidth,scrollWidth:w.scrollWidth,tabindex:w.tabIndex}}))}}))}})()'''))
   assert len(values)==2 and all(v['rows']==15 and v['tabindex']==0 and not v['bodyOverflow'] for v in values)
   audit=json.loads(call('a11y','--selector','.avaluos-ii-table','--json'))
   (OUT/f'{case}-fiscal-tables-axe.json').write_text(json.dumps(audit,indent=2))
   results.append(dict(case=case,tables=values,counts=audit['data']['counts']))
   print(case,audit['data']['counts'],flush=True)
(OUT/'fiscal-tables-matrix.json').write_text(json.dumps(results,indent=2))
call('close')
