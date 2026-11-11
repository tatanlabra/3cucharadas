#!/usr/bin/env python3
"""Exercise native-PDF rejection with real corrupt artifacts; never change production inputs."""
import argparse,json,os,subprocess,sys
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from PIL import Image
from linkedin_native.template import build
from linkedin_native.verify import pdf_report,source_errors,sha
ROOT=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--content',required=True,type=Path);a.add_argument('--pdf',required=True,type=Path);a.add_argument('--output',required=True,type=Path);a.add_argument('--check-pdf',action='store_true');x=a.parse_args()
if x.check_pdf:
 r=pdf_report(x.pdf,x.content);print(json.dumps(r));sys.exit(0 if r['passed'] else 1)
x.content=x.content.resolve();x.pdf=x.pdf.resolve();x.output=x.output.resolve();x.output.mkdir(parents=True,exist_ok=True)
c=json.loads(x.content.read_text());results=[]
def check(name,pdf,marker=None):
 r=subprocess.run([sys.executable,__file__,'--check-pdf','--content',str(x.content),'--pdf',str(pdf),'--output',str(x.output)],capture_output=True,text=True)
 report=json.loads(r.stdout);(x.output/(name+'.json')).write_text(json.dumps(report,indent=2,ensure_ascii=False))
 ok=r.returncode==(1 if marker else 0) and (not marker or any(marker in e for e in report['errors']))
 results.append({'case':name,'exit':r.returncode,'marker':marker,'expected_result':ok,'artifact_sha256':sha(pdf)})
def render(content,name):
 html=x.output/(name+'.html');pdf=x.output/(name+'.pdf');build(content,html,x.content.parent/'assets')
 # The template uses packaged relative assets.
 import shutil
 shutil.copytree(x.content.parent/'assets',x.output/'assets',dirs_exist_ok=True)
 env=os.environ.copy();env['CHROMIUM_PATH']=env.get('CHROMIUM_PATH',str(sorted((Path.home()/'.agent-browser/browsers').glob('chrome-*/chrome'))[-1]));env['PLAYWRIGHT_MODULE']=env.get('PLAYWRIGHT_MODULE',str(ROOT.parents[1]/'penta-agent/tools/playwright-local-mcp/node_modules/playwright-core'))
 r=subprocess.run(['node',str(ROOT/'scripts/linkedin_native/render.mjs'),str(html),str(pdf),str(x.output/(name+'-layout.json'))],env=env,capture_output=True,text=True,timeout=120)
 return r,pdf
wrong=json.loads(json.dumps(c));chart=next(d for d in wrong['slides'] if d.get('rows'));chart['rows'][0]['value']+=0.01
r,pdf=render(wrong,'wrong-number');assert r.returncode==0,r.stderr;check('wrong-number',pdf,'MISSING_TEXT')
w=PdfWriter()
for p in PdfReader(x.pdf).pages[:-1]:w.add_page(p)
w.write(x.output/'missing-page.pdf');check('missing-page',x.output/'missing-page.pdf','PAGE_COUNT')
subprocess.run(['pdftoppm','-scale-to','780','-png',str(x.pdf),str(x.output/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
images=[Image.open(p).convert('RGB') for p in sorted(x.output.glob('page-*.png'))];images[0].save(x.output/'raster.pdf',save_all=True,append_images=images[1:],resolution=96);check('raster',x.output/'raster.pdf','RASTER_ONLY')
over=json.loads(json.dumps(c));over['slides'][0]['body']='Texto largo de prueba. '*1000
r,pdf=render(over,'overflow');report=json.loads((x.output/'overflow-layout.json').read_text());results.append({'case':'overflow','exit':r.returncode,'marker':'SLIDE_OVERFLOW','expected_result':r.returncode==1 and any('SLIDE_OVERFLOW' in e for e in report['errors'])})
mutant=x.output/'changed-content.json';mutant.write_text(json.dumps(wrong));errors=source_errors(ROOT,mutant,x.content.with_name('source-lock.json'));results.append({'case':'frozen-content','errors':errors,'expected_result':'CONTENT_CHANGED_AFTER_FREEZE' in errors})
check('green',x.pdf)
summary={'passed':all(r['expected_result'] for r in results),'cases':results};(x.output/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));sys.exit(0 if summary['passed'] else 1)
