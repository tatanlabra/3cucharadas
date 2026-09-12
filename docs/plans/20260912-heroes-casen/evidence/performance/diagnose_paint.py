from pathlib import Path
import subprocess,json,time,os,datetime
ROOT=Path('/tmp/3c-heroes-performance');OUT=ROOT/'paint-diagnostic';OUT.mkdir(exist_ok=True)
rows=[];log=OUT/'commands.jsonl'
def run(session,*args):
 argv=['agent-browser','--session',session,'--allowed-domains','127.0.0.1','--init-script',str(ROOT/'embedded-vitals-init.js'),'--init-script',str(ROOT/'measurement-init.js'),'--init-script',str(ROOT/'diagnostic-init.js'),'--json',*args];start=time.time();r=subprocess.run(argv,capture_output=True,text=True,timeout=90);j=json.loads(r.stdout)
 with log.open('a')as f:f.write(json.dumps({'argv':argv,'exit_code':r.returncode,'duration':time.time()-start,'response':j,'stderr':r.stderr})+'\n')
 if r.returncode or not j.get('success'):raise RuntimeError(j)
 return j['data']
def ev(s,js):return run(s,'eval',js)['result']
js="""(()=>({now:performance.now(),timeOrigin:performance.timeOrigin,visibility:document.visibilityState,focused:document.hasFocus(),diag:window.__PAINT_DIAG__,cwv:window.__AB_VITALS__,paints:performance.getEntriesByType('paint'),fonts:{status:document.fonts.status,list:[...document.fonts].map(f=>({family:f.family,status:f.status,display:f.display}))},styles:[...document.querySelectorAll('html,body,.page__hero--overlay,h1')].map(e=>({tag:e.tagName,class:e.className,opacity:getComputedStyle(e).opacity,visibility:getComputedStyle(e).visibility,display:getComputedStyle(e).display})),resources:performance.getEntriesByType('resource').map(e=>e.toJSON())}))()"""
for side,port in [('baseline',4041),('candidate',4042)]:
 session='hperf-paint-'+side
 row={'side':side,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'loadavg':os.getloadavg(),'cpuStatBefore':Path('/proc/stat').read_text().splitlines()[0]}
 try:
  run(session,'set','viewport','1440','1000','1');run(session,'set','media','light');row['session']=run(session,'session','info')
  run(session,'open',f'http://127.0.0.1:{port}/datos/territorio/avaluos-ii-brecha-residencial/')
  run(session,'wait','--fn','Boolean(window.__PERF_FINAL__)');row['fiveSecondSnapshot']=ev(session,'window.__PERF_FINAL__');row['beforeFontsAwait']=ev(session,js)
  row['fontsAwait']=ev(session,'(async()=>{const start=performance.now();await document.fonts.ready;return {start,end:performance.now(),status:document.fonts.status}})()')
  row['beforeScreenshot']=ev(session,js)
  run(session,'screenshot',str(OUT/(side+'.png')))
  row['afterScreenshot']=ev(session,js)
  row['decodeRemainingWait']=ev(session,"(async()=>{const i=document.querySelector('.page__hero-image');if(!i)return {reason:'CSS background; no img decode probe'};const start=performance.now();await i.decode();return {start,end:performance.now(),currentSrc:i.currentSrc,complete:i.complete,naturalWidth:i.naturalWidth,note:'post-measurement decode() wait; does not measure original decode duration'}})()")
  row['cpuStatAfter']=Path('/proc/stat').read_text().splitlines()[0]
  print(side,'5sec',row['fiveSecondSnapshot']['cwv'],'after screenshot',row['afterScreenshot']['cwv'],flush=True)
 finally:run(session,'close')
 rows.append(row);(OUT/'runs.json').write_text(json.dumps(rows,indent=2)+'\n')
