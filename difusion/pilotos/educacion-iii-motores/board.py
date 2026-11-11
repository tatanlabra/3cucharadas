#!/usr/bin/env python3
import json, time, shutil
from pathlib import Path
p=Path(__file__).with_name('state.json')
while True:
 try:
  d=json.loads(p.read_text()); w=shutil.get_terminal_size().columns
  lines=['EDUCACIÓN III · PLAN_STATE v2',d['updated'],'']
  for x in d['items']: lines.append(x['state']+' '+x['title'])
  lines+=['',d['note']]
  print('\033[H\033[2J'+'\n'.join(l[:w-1] for l in lines),flush=True)
  time.sleep(2)
 except KeyboardInterrupt: break
