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
for idx,intervention in enumerate(['poll','passive','passive','poll']):
 s='presentation-canary-repeat-'+str(idx)
 try:
  cmd(s,'set','viewport','1440','1000','1');cmd(s,'set','media','light')
  cmd(s,'open','http://127.0.0.1:4044/fast.html')
  if intervention=='poll':cmd(s,'wait','--fn','Boolean(window.__PERF_FINAL__)')
  else:time.sleep(5.3)
  sample=cmd(s,'eval','window.__PERF_FINAL__')['result']
  rows.append({'intervention':intervention,'index':idx,'sample':sample})
  (OUT/'repeat-runs.json').write_text(json.dumps(rows,indent=2))
  print(json.dumps({'intervention':intervention,'index':idx,'cwv':sample['cwv']}),flush=True)
 finally:cmd(s,'close')
