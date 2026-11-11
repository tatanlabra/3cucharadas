#!/usr/bin/env python3
"""Native round: independent compositions; no scene.py or PIL line wrapping."""
import argparse,json,hashlib,time,subprocess,os
from pathlib import Path
P=Path(__file__).resolve().parent
CODE={'typst':'A','beamer':'B','html':'C','scribus':'D'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('engine',choices=[*CODE,'all']);ap.add_argument('--content',type=Path,default=P/'content.json');ap.add_argument('--output',type=Path,default=P/'out/native');a=ap.parse_args();a.output=a.output.resolve();a.content=a.content.resolve();a.output.mkdir(parents=True,exist_ok=True)
 content=a.content.read_bytes();c=json.loads(content);assets=P/'out/assets';env=dict(os.environ,TEXMFVAR=str(P/'.tools/tex-cache-ready'),TEXMFCACHE=str(P/'.tools/tex-cache-ready'))
 for engine in CODE if a.engine=='all' else [a.engine]:
  prefix=a.output/CODE[engine];start=time.perf_counter()
  if engine=='typst':
   from native_typst import build
   source=prefix.with_suffix('.typ');build(c,source,assets);cmd=[str(P/'.tools/root/usr/bin/typst'),'compile','--root',str(P),'--font-path','/usr/share/fonts/TTF',str(source),str(prefix.with_suffix('.pdf'))]
  elif engine=='beamer':
   from native_beamer import build
   source=prefix.with_suffix('.tex');build(c,source,assets);cmd=['lualatex','--interaction=nonstopmode','--halt-on-error','--output-directory='+str(a.output),str(source)]
  elif engine=='html':
   from native_html import build
   source=prefix.with_suffix('.html');build(c,source,assets);cmd=['node',str(P/'html_render.mjs'),str(source),str(prefix.with_suffix('.pdf'))]
  else:
   source=prefix.with_suffix('.content.json');source.write_bytes(content)
   cmd=['bwrap','--ro-bind','/','/','--dev-bind','/dev','/dev','--bind',str(P),str(P),'--bind','/tmp','/tmp','--overlay-src','/usr','--overlay-src',str(P/'.tools/root/usr'),'--ro-overlay','/usr','--setenv','XDG_DATA_HOME',str(P/'.tools/scribus-data'),'--setenv','XDG_CACHE_HOME',str(P/'.tools/scribus-cache'),'--setenv','TMPDIR',str(P/'.tools/tmp'),'/usr/bin/scribus','-platform','offscreen','-g','-ns','-pr',str(P/'.tools/scribus-prefs'),'-py',str(P/'native_scribus.py'),str(prefix)]
  prefix.with_suffix('.receipt.json').write_text(json.dumps({'status':'building','engine':engine}))
  with prefix.with_suffix('.build.log').open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,cwd=P,timeout=180)
  if r.returncode:raise RuntimeError(f'{engine}: exit {r.returncode}; {prefix}.build.log')
  if engine=='html':
   from pypdf import PdfReader,PdfWriter
   pdf=prefix.with_suffix('.pdf');w=PdfWriter(clone_from=PdfReader(pdf))
   for page in w.pages:page.mediabox.upper_right=(810,1012.5)
   tmp=prefix.with_suffix('.tmp.pdf');w.write(tmp);tmp.replace(pdf)
  if a.content.read_bytes()!=content:raise RuntimeError('CONTENT_CHANGED_DURING_RENDER')
  receipt={'status':'success','engine':engine,'native_layout':True,'seconds':round(time.perf_counter()-start,3),'content_sha256':hashlib.sha256(content).hexdigest(),'pdf_sha256':sha(prefix.with_suffix('.pdf')),'source_sha256':sha(source),'generator_sha256':sha(P/('native_'+engine+'.py')),'command':cmd}
  prefix.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2));print(engine,receipt['seconds'],flush=True)
if __name__=='__main__':main()
