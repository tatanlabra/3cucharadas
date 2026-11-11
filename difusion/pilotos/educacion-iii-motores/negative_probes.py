#!/usr/bin/env python3
"""Real artifacts: wrong number, omitted page and rasterized pages. Preserve exit codes."""
import json,subprocess,sys,hashlib
from pathlib import Path
from PIL import Image
from pypdf import PdfReader,PdfWriter
from native_build import P
D=P/'out/native/probes';D.mkdir(exist_ok=True)
c=json.loads((P/'content.json').read_text());c['slides'][3]['rows'][0]['value']=9.59
(D/'wrong.json').write_text(json.dumps(c,ensure_ascii=False))
subprocess.run([sys.executable,str(P/'native_build.py'),'typst','--content',str(D/'wrong.json'),'--output',str(D/'wrong')],check=True)
r=PdfReader(P/'out/native/A.pdf');w=PdfWriter()
for page in r.pages[:-1]:w.add_page(page)
w.write(D/'missing-page.pdf')
imgs=[Image.open(P/f'out/native/previews/A/page-{i}.png').convert('RGB') for i in range(1,10)]
imgs[0].save(D/'raster.pdf',save_all=True,append_images=imgs[1:],resolution=96)
cases=[('wrong-number',D/'wrong/A.pdf','MISSING_TEXT'),('missing-page',D/'missing-page.pdf','PAGE_COUNT'),('raster-only',D/'raster.pdf','RASTER_ONLY')];results=[]
for name,pdf,marker in cases:
 receipt=D/(name+'.json');cmd=[sys.executable,str(P/'native_verify.py'),'--engine','typst','--pdf',str(pdf),'--receipt',str(receipt)]
 r=subprocess.run(cmd,stdout=subprocess.DEVNULL);errors=json.loads(receipt.read_text())['results'][0]['errors'];valid=r.returncode==1 and any(marker in e for e in errors)
 results.append({'probe':name,'exit_code':r.returncode,'expected_marker':marker,'observed':valid,'artifact_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'command':cmd,'receipt':str(receipt.relative_to(P))})
 print(name,'exit',r.returncode,'expected rejection',valid)
 if not valid:raise RuntimeError('Invalid negative probe '+name)
cmd=[sys.executable,str(P/'native_verify.py'),'--receipt',str(D/'green.json')];green=subprocess.run(cmd,stdout=subprocess.DEVNULL)
(D/'summary.json').write_text(json.dumps({'red':results,'green_exit':green.returncode},indent=2));print('green exit',green.returncode);sys.exit(green.returncode)
