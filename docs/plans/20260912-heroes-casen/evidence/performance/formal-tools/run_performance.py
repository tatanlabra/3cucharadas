#!/usr/bin/env python3
"""Paired local diagnostic/formal benchmark. Stdlib only; agent-browser is the primary driver.
Usage: python3 run_performance.py --candidate-root /tmp/site --pairs 1 --label pilot --output /tmp/out
Servers 4041/4042 must already be running with the canonical serve_range_static.mjs.
Cold=new browser/session without restored state; warm=reload same session. OS page cache not flushed.
"""
import argparse,copy,datetime,hashlib,json,os,pathlib,platform,statistics,subprocess,time,urllib.request
P=argparse.ArgumentParser();P.add_argument('--candidate-root',required=True);P.add_argument('--baseline-root',default='/tmp/3c-heroes-baseline-site');P.add_argument('--pairs',type=int,default=1);P.add_argument('--label',default='pilot');P.add_argument('--output',required=True);a=P.parse_args()
assert a.pairs>=1
OUT=pathlib.Path(a.output);OUT.mkdir(parents=True,exist_ok=True);HERE=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/ende/Descargas/programaciones/activos/3cucharadas')
PAGES={'avaluos-ii':'/datos/territorio/avaluos-ii-brecha-residencial/','casen-long':'/datos/politica-publica/julia/casen/casen2024-julia-waffles-politica-publica/'}
ROOTS={'baseline':pathlib.Path(a.baseline_root),'candidate':pathlib.Path(a.candidate_root)};PORTS={'baseline':4041,'candidate':4042}
rows=[];log=OUT/'commands.jsonl';active=[];cpu_windows=[]
def cpu_snapshot():
 total=list(map(int,pathlib.Path('/proc/stat').read_text().splitlines()[0].split()[1:]));procs={}
 for p in pathlib.Path('/proc').iterdir():
  if p.name.isdigit():
   try:
    stat=(p/'stat').read_text();end=stat.rfind(')');rest=stat[end+2:].split();procs[p.name]={'comm':stat[stat.find('(')+1:end],'ticks':int(rest[11])+int(rest[12])}
   except (OSError,ValueError,IndexError):pass
 return {'at':time.monotonic(),'cpu_ticks':total,'loadavg':os.getloadavg(),'procs':procs}
def cpu_delta(before,after):
 ticks=[b-a for a,b in zip(before['cpu_ticks'],after['cpu_ticks'])];total=sum(ticks[:8]);dt=after['at']-before['at'];hz=os.sysconf('SC_CLK_TCK');top=[]
 for pid,p in after['procs'].items():
  if pid in before['procs']:
   usage=(p['ticks']-before['procs'][pid]['ticks'])/hz/dt
   if usage>0:top.append({'pid':int(pid),'comm':p['comm'],'cpu_core_equivalents':usage})
 return {'duration_s':dt,'cpu_busy_percent':100*(total-ticks[3]-ticks[4])/total if total else None,'loadavg_start':before['loadavg'],'loadavg_end':after['loadavg'],'top_processes':sorted(top,key=lambda p:p['cpu_core_equivalents'],reverse=True)[:12]}

def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(session,*args,allow_failure=False):
 argv=['agent-browser','--session',session,'--allowed-domains','127.0.0.1','--init-script',str(HERE/'embedded-vitals-init.js'),'--init-script',str(HERE/'measurement-init.js'),'--json',*map(str,args)]
 start=time.time();r=subprocess.run(argv,capture_output=True,text=True,timeout=90)
 try:payload=json.loads(r.stdout)
 except ValueError:payload={'success':False,'error':'unparseable stdout','raw':r.stdout}
 with log.open('a') as f:f.write(json.dumps({'time':start,'duration_s':time.time()-start,'argv':argv,'exit_code':r.returncode,'stderr':r.stderr,'response':payload})+'\n')
 if (r.returncode or not payload.get('success')) and not allow_failure:raise RuntimeError(str(payload))
 return payload.get('data')
def ev(session,js):return cmd(session,'eval',js)['result']
def window_cls(entries):
 best=score=0.;start=previous=None
 for e in sorted(entries,key=lambda x:x['startTime']):
  t=e['startTime']
  if start is None or t-previous>=1000 or t-start>=5000: start=t;score=0.
  score+=e['value'];best=max(best,score);previous=t
 return best
# Deterministic negative controls validate missing metrics and threshold predicates, not observed performance.
def assess(base,cand):
 if base is None or cand is None:return 'missing'
 return 'pass' if cand<=2500 and cand<=base*1.1 else 'fail'
controls=[{'name':'missing','observed':assess(1000,None),'expected':'missing'}, {'name':'regression','observed':assess(1000,1200),'expected':'fail'}, {'name':'absolute','observed':assess(3000,2800),'expected':'fail'}, {'name':'green','observed':assess(1000,1050),'expected':'pass'}, {'name':'cls-windows','observed':window_cls([{'startTime':0,'value':.05},{'startTime':500,'value':.06},{'startTime':2000,'value':.08}]),'expected':.11}]
assert all(x['observed']==x['expected'] for x in controls);dump('measurement-controls.json',controls)
manifest={side:{'root':str(root),'pages':{name:sha(root/url.lstrip('/')/'index.html') for name,url in PAGES.items()}} for side,root in ROOTS.items()}
settings={'label':a.label,'acceptance_candidate':False if a.label.startswith('pilot') else True,'pairs':a.pairs,'pages':PAGES,'viewport':[1440,1000],'dpr':1,'media':'light, no-preference motion','cpu':'no emulated throttling (native host)','network':'loopback, no emulated latency/bandwidth throttle, allowed-domains 127.0.0.1; external requests blocked','cold':'new isolated browser process/session per page/build/pair, no restore/profile; OS disk cache not flushed','warm':'second navigation via reload in same browser/session; server Cache-Control no-store, not an HTTP cache-hit claim','window_ms':5000,'interaction':'none during measurement; no scroll or theme clicks','cpu_measurement':'10 second window before each page pair; per-navigation global CPU and process deltas; all samples retained without load-based exclusion','order':'AB then BA alternated by pair and page index; cold then warm within each build','host':{'platform':platform.platform(),'cpu_count':os.cpu_count(),'cpu_model':next((l.split(':',1)[1].strip() for l in pathlib.Path('/proc/cpuinfo').read_text().splitlines() if l.startswith('model name')),None)},'tool_versions':{'agent_browser':subprocess.check_output(['agent-browser','--version'],text=True).strip(),'node':subprocess.check_output(['node','--version'],text=True).strip()},'hashes':{'server':sha(REPO/'scripts/catastro_sii/serve_range_static.mjs'),'agent_browser_binary':sha(pathlib.Path('/home/ende/.local/lib/node_modules/agent-browser/bin/agent-browser-linux-x64')),'embedded_init':sha(HERE/'embedded-vitals-init.js'),'measurement_init':sha(HERE/'measurement-init.js'),'harness':sha(pathlib.Path(__file__))},'inputs':manifest}
# Verify actual no-store headers before measurements; HTML bytes bound above.
settings['server_headers']={side:dict(urllib.request.urlopen(f'http://127.0.0.1:{PORTS[side]}'+next(iter(PAGES.values()))).headers) for side in ROOTS}
assert all(h.get('Cache-Control')=='no-store' for h in settings['server_headers'].values());dump('settings.json',settings)
try:
 for pair in range(1,a.pairs+1):
  for page_index,(page,url) in enumerate(PAGES.items()):
   cpu_start=cpu_snapshot();time.sleep(10);cpu_window={'pair':pair,'page':page,**cpu_delta(cpu_start,cpu_snapshot())};cpu_windows.append(cpu_window);dump('cpu-before-pairs.json',cpu_windows)
   order=['baseline','candidate'] if (pair+page_index)%2 else ['candidate','baseline']
   for side in order:
    session=f'hperf-{a.label}-{pair}-{page}-{side}';active.append(session)
    cmd(session,'set','viewport','1440','1000','1')
    cmd(session,'set','media','light')
    session_info=cmd(session,'session','info')
    for temperature in ['cold','warm']:
     row={'pair':pair,'page':page,'side':side,'temperature':temperature,'session':session,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'loadavg_start':os.getloadavg(),'session_info':session_info,'missing':True}
     cpu_before=cpu_snapshot()
     try:
      nav=cmd(session,'open',f'http://127.0.0.1:{PORTS[side]}{url}') if temperature=='cold' else cmd(session,'reload')
      cmd(session,'wait','--fn','Boolean(window.__PERF_FINAL__)')
      sample=ev(session,'window.__PERF_FINAL__');row['sample']=sample
      origin_after=ev(session,'performance.timeOrigin')
      assert origin_after==sample['timeOrigin'],'measurement unexpectedly navigated'
      assert sample['device']['width']==1440 and sample['device']['height']==1000 and sample['device']['dpr']==1
      assert sample['device']['theme']=='light','unexpected measured theme'
      assert sample['url']==f'http://127.0.0.1:{PORTS[side]}{url}' and sample['readyState']=='complete'
      assert len(sample['h1'])==1 and sample['visibility']=='visible'
      cwv=sample['cwv'];supported=sample['observation']['supported'];lcp=cwv['lcp']['startTime'] if cwv and cwv.get('lcp') else None
      row['metrics']={'lcp_ms':lcp,'cls_raw_sum':cwv.get('cls') if cwv else None,'cls_session_window':window_cls(sample['observation']['shifts']) if 'layout-shift' in supported and not sample['observation']['errors'] else None,'fcp_ms':cwv.get('fcp') if cwv else None}
      row['missing']=lcp is None or row['metrics']['cls_session_window'] is None
      row['loadavg_end']=os.getloadavg();row['eval_snapshot_did_not_navigate']=True;row['collector']='embedded agent-browser vitals observer via reviewed pre-navigation init; native vitals command excluded because it reloads'
      row['post_window_fonts_checkpoint']=ev(session,"(async()=>{const start=performance.now();await document.fonts.ready;await new Promise(resolve=>setTimeout(resolve,0));return {start,end:performance.now(),timeOrigin:performance.timeOrigin,visibility:document.visibilityState,focused:document.hasFocus(),fontsStatus:document.fonts.status,cwv:window.__AB_VITALS__,note:'supplementary after-window checkpoint; does not replace primary snapshot or impute missing metrics'}})()")
      row['resources_sha256']={}
      for res in sample['resources']:
       u=urllib.parse.urlsplit(res['name'])
       if u.hostname=='127.0.0.1':
        f=ROOTS[side]/urllib.parse.unquote(u.path).lstrip('/')
        if f.is_file():row['resources_sha256'][u.path]=sha(f)
      print(f"{pair} {page} {side} {temperature}: {row['metrics']}",flush=True)
     except Exception as e:row['error']=str(e);print('MISSING',row['error'],flush=True)
     row['cpu_during_navigation']=cpu_delta(cpu_before,cpu_snapshot())
     rows.append(row);dump('runs.json',rows)
    cmd(session,'close',allow_failure=True);active.remove(session)
finally:
 for session in active:cmd(session,'close',allow_failure=True)
summary=[]
for page in PAGES:
 for temperature in ['cold','warm']:
  group={side:[r for r in rows if r['page']==page and r['temperature']==temperature and r['side']==side] for side in ROOTS}
  medians={side:statistics.median([r['metrics']['lcp_ms'] for r in group[side]]) if len(group[side])==a.pairs and all(not r['missing'] for r in group[side]) else None for side in ROOTS}
  result={'page':page,'temperature':temperature,'n_expected_each':a.pairs,'median_lcp_ms':medians,'regression_percent':(medians['candidate']/medians['baseline']-1)*100 if all(x is not None and x>0 for x in medians.values()) else None,'lcp_threshold_diagnostic':assess(medians['baseline'],medians['candidate']),'baseline_lcp_absolute_pass':medians['baseline']<=2500 if medians['baseline'] is not None else None,'max_cls':{side:max((r['metrics']['cls_session_window'] for r in group[side]),default=None) if all(not r['missing'] for r in group[side]) else None for side in ROOTS}}
  summary.append(result)
dump('summary.json',{'label':a.label,'formal_acceptance':False if a.label.startswith('pilot') or a.pairs<5 else 'requires root review and frozen final inputs','groups':summary,'missing_runs':sum(r['missing'] for r in rows),'n_runs':len(rows)})
print(json.dumps(summary,indent=2),flush=True)
