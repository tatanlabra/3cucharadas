#!/usr/bin/env python3
import pathlib,subprocess,json,time,hashlib
OUT=pathlib.Path(__file__).parent
INIT=OUT.parent/'formal-tools/measurement-init.js'
BUILTIN=OUT.parent/'formal-tools/embedded-vitals-init.js'
rows=[]
def run(session,mode,*args):
 argv=['agent-browser','--session',session,'--allowed-domains','127.0.0.1','--init-script',str(BUILTIN),'--init-script',str(INIT),'--json']
 if mode=='headed':argv+=['--headed']
 argv+=list(args)
 r=subprocess.run(argv,capture_output=True,text=True,timeout=45)
 with (OUT/'commands.jsonl').open('a') as f:f.write(json.dumps({'argv':argv,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})+'\n')
 data=json.loads(r.stdout)
 if r.returncode or not data.get('success'):raise RuntimeError(data)
 return data.get('data')
for mode in ['headless','headed']:
 for fixture in ['fast','late']:
  session='presentation-canary-'+mode+'-'+fixture
  try:
   run(session,mode,'set','viewport','1440','1000','1')
   run(session,mode,'set','media','light')
   for nav in ['cold','warm']:
    run(session,mode,'open','http://127.0.0.1:4044/'+fixture+'.html') if nav=='cold' else run(session,mode,'reload')
    run(session,mode,'wait','--fn','Boolean(window.__PERF_FINAL__)')
    row={'mode':mode,'fixture':fixture,'navigation':nav,'sample':run(session,mode,'eval','window.__PERF_FINAL__')['result']}
    rows.append(row);(OUT/'canary-runs.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps({'mode':mode,'fixture':fixture,'navigation':nav,'lcp':row['sample']['cwv'],'paints':row['sample']['observation']['paints']}),flush=True)
   # Capture command-line flags only from isolated canary browser; no session data.
   processes=[]
   for proc in pathlib.Path('/proc').iterdir():
    if not proc.name.isdigit():continue
    try:
     args=(proc/'cmdline').read_bytes().decode().split('\0')
     if any(session in arg for arg in args) and args and 'chrome' in args[0]:processes.append({'pid':int(proc.name),'exe':args[0],'flags':[a.split('=',1)[0] for a in args[1:] if a.startswith('--')]})
    except (OSError,UnicodeError):pass
   (OUT/(session+'-flags.json')).write_text(json.dumps(processes,indent=2))
  finally:
   try:run(session,mode,'close')
   except Exception as exc:print(str(exc),flush=True)
