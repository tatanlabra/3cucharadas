#!/usr/bin/env python3
import pathlib,subprocess,json,time
OUT=pathlib.Path(__file__).parent
INIT=OUT.parent/'formal-tools/measurement-init.js';BUILTIN=OUT.parent/'formal-tools/embedded-vitals-init.js'
rows=[]
def cmd(s,*args):
 argv=['agent-browser','--session',s,'--allowed-domains','127.0.0.1','--init-script',str(BUILTIN),'--init-script',str(INIT),'--json',*args]
 r=subprocess.run(argv,capture_output=True,text=True,timeout=45)
 with (OUT/'intervention-commands.jsonl').open('a') as f:f.write(json.dumps({'argv':argv,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})+'\n')
 d=json.loads(r.stdout)
 if not d.get('success'):raise RuntimeError(d)
 return d.get('data')
for intervention in ['passive','screenshot']:
 s='presentation-canary-'+intervention
 try:
  cmd(s,'set','viewport','1440','1000','1');cmd(s,'set','media','light')
  processes=[]
  for p in pathlib.Path('/proc').iterdir():
   if not p.name.isdigit():continue
   try:
    a=(p/'cmdline').read_bytes().decode().split('\0')
    if a and '/.agent-browser/browsers/' in a[0] and a[0].endswith('/chrome'):
     processes.append({'pid':int(p.name),'exe':a[0],'flags':[v if not any(t in v for t in ['user-data-dir','remote-debugging','crashpad','field-trial','variations']) else v.split('=',1)[0] for v in a[1:] if v.startswith('--')]})
   except (OSError,UnicodeError):pass
  (OUT/(intervention+'-actual-flags.json')).write_text(json.dumps(processes,indent=2))
  for nav in ['cold','warm']:
   cmd(s,'open','http://127.0.0.1:4044/fast.html') if nav=='cold' else cmd(s,'reload')
   if intervention=='screenshot':cmd(s,'screenshot',str(OUT/('diagnostic-'+nav+'.png')))
   time.sleep(5.3)
   sample=cmd(s,'eval','window.__PERF_FINAL__')['result']
   row={'intervention':intervention,'navigation':nav,'sample':sample};rows.append(row)
   (OUT/'intervention-runs.json').write_text(json.dumps(rows,indent=2))
   print(json.dumps({'intervention':intervention,'navigation':nav,'cwv':sample['cwv']}),flush=True)
 finally:cmd(s,'close')
