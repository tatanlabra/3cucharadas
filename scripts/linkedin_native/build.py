import argparse,json,os,shutil,subprocess,tempfile,time
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from .template import build as template
from .verify import source_errors,pdf_report,sha
MODULE=Path(__file__).resolve().parent
REPO=MODULE.parents[1]
def main():
 ap=argparse.ArgumentParser(description='Carrusel HTML/CSS nativo: fuente congelada → PDF comprobado. No envía ni publica.')
 ap.add_argument('--filename',default='carrusel-linkedin.pdf');ap.add_argument('--content',required=True,type=Path);ap.add_argument('--lock',type=Path);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--verify-only',action='store_true');a=ap.parse_args()
 
 if Path(a.filename).name!=a.filename or not a.filename.endswith('.pdf'):ap.error('--filename must be a PDF basename')
 content=a.content.resolve();lock=(a.lock or content.with_name('source-lock.json')).resolve();out=a.output.resolve()
 try:
  errors=source_errors(REPO,content,lock)
  if errors:print(json.dumps({'passed':False,'errors':errors}));return 1
  c=json.loads(content.read_text());start=time.perf_counter()
  if a.verify_only:
   report=pdf_report(out/a.filename,content)
   receipt=json.loads((out/'build.json').read_text())
   for name,digest in receipt['inputs'].items():
    if sha(Path(name))!=digest:report['errors'].append('INPUT_CHANGED '+name)
   if sha(out/a.filename)!=receipt['pdf_sha256']:report['errors'].append('PDF_CHANGED')
   report['passed']=not report['errors'];print(json.dumps(report,ensure_ascii=False));return 0 if report['passed'] else 1
  inputs=[content,lock,*sorted(MODULE.glob('*.py')),MODULE/'render.mjs',*sorted((content.parent/'assets').iterdir())]
  hashes={str(p):sha(p) for p in inputs if p.is_file()};out.mkdir(parents=True,exist_ok=True)
  with tempfile.TemporaryDirectory(prefix='.build-',dir=out) as tmp:
   stage=Path(tmp);shutil.copytree(content.parent/'assets',stage/'assets');html=stage/'carrusel.html';pdf=stage/a.filename;template(c,html,stage/'assets')
   browsers=sorted((Path.home()/'.agent-browser/browsers').glob('chrome-*/chrome'))
   chromium=os.environ.get('CHROMIUM_PATH') or (str(browsers[-1]) if browsers else '')
   env={k:v for k,v in os.environ.items() if k in ['PATH','HOME','LANG','LC_ALL','TMPDIR','DISPLAY','XDG_RUNTIME_DIR']}
   env['CHROMIUM_PATH']=chromium;env['PLAYWRIGHT_MODULE']=os.environ.get('PLAYWRIGHT_MODULE',str(REPO.parents[1]/'penta-agent/tools/playwright-local-mcp/node_modules/playwright-core'))
   with (out/'last-build.log').open('w') as log:r=subprocess.run(['node',str(MODULE/'render.mjs'),str(html),str(pdf),str(stage/'layout.json')],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
   if r.returncode:
    if (stage/'layout.json').exists():shutil.copy2(stage/'layout.json',out/'failed-layout.json')
    print('RENDER_FAILED; previous successful artifact preserved; see last-build.log');return 1
   writer=PdfWriter(clone_from=PdfReader(pdf))
   for page in writer.pages:page.mediabox.upper_right=(810,1012.5)
   writer.add_metadata({'/Title':c['title']+' · 3 Cucharadas','/Author':'Cristián Labra Olivares','/Subject':'Carrusel LinkedIn · HTML/CSS nativo'})
   writer.write(stage/'normalized.pdf');(stage/'normalized.pdf').replace(pdf)
   report=pdf_report(pdf,content)
   if any(sha(Path(p))!=h for p,h in hashes.items()):report['errors'].append('INPUT_CHANGED_DURING_BUILD');report['passed']=False
   (stage/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
   if not report['passed']:shutil.copy2(stage/'qa.json',out/'failed-qa.json');print(json.dumps(report));return 1
   receipt={'engine':'HTML/CSS + Chromium','seconds':round(time.perf_counter()-start,3),'inputs':hashes,'pdf_sha256':sha(pdf),'source_sha256':sha(REPO/c['source']),'content_sha256':sha(content),'chromium':chromium,'pages':len(c['slides'])}
   (stage/'build.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
   for item in stage.iterdir():
    if item.is_dir():shutil.copytree(item,out/item.name,dirs_exist_ok=True)
    else:shutil.copy2(item,out/item.name)
  print(json.dumps({'passed':True,'pdf':str(out/a.filename),'pages':len(c['slides']),'sha256':receipt['pdf_sha256']}));return 0
 except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:
  print('PRECONDITION_ERROR '+type(error).__name__+': '+str(error));return 3
