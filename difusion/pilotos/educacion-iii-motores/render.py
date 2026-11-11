#!/usr/bin/env python3
"""Four native layout engines, one frozen editorial source; no full-page raster PDF."""
import argparse, json, hashlib, subprocess, time, os, html, shutil
from pathlib import Path
from PIL import Image, ImageFont
P=Path(__file__).resolve().parent
REPO=P.parents[2]; OUT=P/'out'; OUT.mkdir(exist_ok=True)
COL={'bg':'161616','ink':'f2f5f8','muted':'b5beca','cyan':'64d8e9','purple':'a79cff','pink':'f08ca3','panel':'202329','rule':'424953'}
FONTS={w:Path('/usr/share/fonts/TTF')/('FiraSans-'+n+'.ttf') for w,n in [(400,'Regular'),(500,'Medium'),(600,'SemiBold')]}
CODE={'typst':'A','beamer':'B','html':'C','scribus':'D'}

def fmt(n): return ('+' if n>0 else '−' if n<0 else '')+f'{abs(n):.2f}'.replace('.',',')
def wrap(s,size,width,weight=400):
 f=ImageFont.truetype(str(FONTS[weight]),size); out=[]
 for para in s.split('\n'):
  line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if line and f.getlength(trial)>width-18:out.append(line);line=word
   else:line=trial
  out.append(line)
 return out

class Scene:
 def __init__(self): self.ops=[]
 def text(self,s,x,y,w,size=44,color='ink',weight=400,link=None,leading=1.22):
  lines=wrap(s,size,w,weight); h=len(lines)*size*leading+10
  self.ops.append(dict(kind='text',text='\n'.join(lines),x=x,y=y,w=w,h=h,size=size,color=COL.get(color,color),weight=weight,leading=leading,link=link))
  return y+h
 def rect(self,x,y,w,h,color):self.ops.append(dict(kind='rect',x=x,y=y,w=w,h=h,color=COL.get(color,color)))
 def line(self,x,y,x2,y2,color='rule',width=2):self.ops.append(dict(kind='line',x=x,y=y,x2=x2,y2=y2,color=COL.get(color,color),width=width))
 def circle(self,x,y,r,color):self.ops.append(dict(kind='circle',x=x-r,y=y-r,w=2*r,h=2*r,color=COL.get(color,color)))
 def image(self,path,x,y,w,h):self.ops.append(dict(kind='image',path=str(path),x=x,y=y,w=w,h=h))

def assets():
 a=OUT/'assets';a.mkdir(exist_ok=True)
 hero=REPO/'assets/images/heroes-v2/costos-cierre-escolar-trayectorias/hero-1600x900.webp'
 
 if not (a/'hero.png').exists(): Image.open(hero).convert('RGB').save(a/'hero.png')
 
 if not (a/'logo.png').exists(): Image.open(REPO/'assets/images/3cucharadas-logo-128.webp').convert('RGBA').save(a/'logo.png')
 return a

def scenes(content,engine):
 a=assets(); pages=[]
 for idx,d in enumerate(content['slides'],1):
  s=Scene();s.rect(0,0,1080,1350,'bg')
  # A: asymmetric editorial; B: framed academic; C: cards; D: magazine rail.
  m=80 if engine=='typst' else 64 if engine in ['beamer','html'] else 80
  w=1080-2*m; accent='purple' if engine=='beamer' else 'cyan'
  if engine=='scribus':
   s.rect(0,0,26,1350,'cyan');s.text(f'{idx:02d}',m,55,150,70,'purple',500)
   s.text('3 Cucharadas',m+175,72,600,34,'ink',500)
  else:
   s.rect(m-4,52,54,54,'ink');s.image(a/'logo.png',m,56,46,46);s.text('3 Cucharadas',m+64,52,600,34,'ink',500)
  s.text(f'{idx:02d} / 09',895,65,130,28,'muted')
  s.line(m,132,1080-m,132,'rule')
  if d['kind'] in ['cover','cta']:
   if engine=='typst':
    s.image(a/'hero.png',380,160,620,349);s.rect(80,180,270,10,'cyan');ty=535;tw=w
   elif engine=='beamer':
    s.image(a/'hero.png',64,160,952,450);ty=630;tw=w
   elif engine=='html':
    s.image(a/'hero.png',0,150,1080,510);s.rect(64,590,952,270,'panel');ty=630;tw=w-48
   else:
    s.image(a/'hero.png',80,170,920,410);ty=630;tw=w
   # Keep content legible below illustration; image itself carries no text.
   s.text(d['kicker'],m,ty-48,w,30,'cyan',500)
   end=s.text(d['title'],m if engine!='html' else m+24,ty,tw,76 if engine=='typst' else 68,'ink',500,leading=1.10)
   end=s.text(d['body'],m,end+22,w,44,'ink')
   if d['kind']=='cta':
    s.rect(m,1100,w,85,'cyan');s.text(d['takeaway']+' ↗',m+24,1114,w-48,44,'161616',500,link=content['url'])
   else:s.text(d['takeaway'],m,max(end+24,1080),w,44,'cyan',500)
   s.text(d['note'],m,1205,w,34,'muted')
  else:
   s.text(d['kicker'],m,166,w,30,'cyan',500)
   size=68 if engine!='scribus' else 64
   end=s.text(d['title'],m,220,w,size,'ink',500,leading=1.10)
   end=s.text(d['body'],m,end+24,w,44)
   y=end+35
   if d['kind']=='chart':
    lo,hi=d['domain']
    if engine=='beamer':
     cw=(w-36)/2
     for j,row in enumerate(d['rows']):
      xx=m+j*(cw+36);c='cyan' if j==0 else 'purple'
      s.rect(xx,y,cw,300,'panel');s.rect(xx,y,cw,4,c)
      s.text(row['label'],xx+22,y+18,cw-44,34,c,500)
      s.text(fmt(row['value']),xx+22,y+65,cw-44,70,'ink',500)
      s.text(f"[{fmt(row['lo'])}; {fmt(row['hi'])}]",xx+22,y+160,cw-44,34,'muted')
      px=lambda v:xx+35+(v-lo)/(hi-lo)*(cw-70)
      yy=y+230
      s.line(px(lo),yy,px(hi),yy,'rule',2)
      s.line(px(row['lo']),yy,px(row['hi']),yy,c,6);s.circle(px(row['value']),yy,9,c)
      for v in ['lo','hi']:s.line(px(row[v]),yy-10,px(row[v]),yy+10,c,3)
      for v in [lo,hi]:s.text(str(v).replace('-','−'),px(v)-15,yy+18,80,34,'muted')
     s.text(d['interval']+' · puntos porcentuales',m,y+322,w,34,'muted')
    elif engine in ['html','scribus']:
     x0=m+355;x1=1080-m-35;px=lambda v:x0+(v-lo)/(hi-lo)*(x1-x0)
     for j,row in enumerate(d['rows']):
      yy=y+j*145;c='cyan' if j==0 else 'purple'
      if engine=='html':s.rect(m-12,yy-5,w+24,135,'panel')
      else:s.line(m,yy-8,1080-m,yy-8,'rule')
      s.text(row['label'],m+12,yy+2,325,34,'muted')
      s.text(fmt(row['value']),m+12,yy+46,325,60,c,500)
      s.text(f"[{fmt(row['lo'])}; {fmt(row['hi'])}]",x0,yy+8,x1-x0+25,34,c,500)
      s.line(x0,yy+90,x1,yy+90,'rule',2)
      for v in d['ticks']:s.line(px(v),yy+65,px(v),yy+110,'rule',2)
      s.line(px(row['lo']),yy+90,px(row['hi']),yy+90,c,6);s.circle(px(row['value']),yy+90,9,c)
      for v in ['lo','hi']:s.line(px(row[v]),yy+80,px(row[v]),yy+100,c,3)
     for v in d['ticks']:s.text(str(v).replace('-','−'),px(v)-20,y+278,70,34,'muted')
     s.text(d['interval']+' · puntos porcentuales',m,y+333,w,34,'muted')
    else:
     x0=m+30;x1=1080-m-30;px=lambda v:x0+(v-lo)/(hi-lo)*(x1-x0)
     base=y+245
     for t in d['ticks']:
      x=px(t);s.line(x,y+45,x,base,'muted' if t==0 else 'rule',3 if t==0 else 1)
      s.text(str(t).replace('-', '−'),x-23,base+8,80,34,'muted')
     for j,row in enumerate(d['rows']):
      yy=y+70+j*130;c='cyan' if j==0 else 'purple'
      label=row['label']+'  ·  '+fmt(row['value'])+f"  [{fmt(row['lo'])}; {fmt(row['hi'])}]"
      s.text(label,m,yy-70,w,34,c,500)
      s.line(px(row['lo']),yy,px(row['hi']),yy,c,6)
      for v in ['lo','hi']:s.line(px(row[v]),yy-12,px(row[v]),yy+12,c,4)
      s.circle(px(row['value']),yy,10,c)
     s.text(d['interval']+' · puntos porcentuales',m,base+58,w,34,'muted')
   elif d['kind']=='method':
    if engine=='scribus':
     for j,c in enumerate(d['cards']):
      yy=y+j*145;s.line(m,yy,1080-m,yy,'rule');s.text(c['label'],m,yy+15,440,66,'cyan' if j==0 else 'purple',500);s.text(c['text'],m+470,yy+30,400,38,'muted')
    else:
     cw=(w-30)/2
     for j,c in enumerate(d['cards']):
      xx=m+j*(cw+30);s.rect(xx,y,cw,235,'panel');s.rect(xx,y,cw,5,'cyan' if j==0 else 'purple');s.text(c['label'],xx+24,y+45,cw-48,54,'ink',500);s.text(c['text'],xx+24,y+135,cw-48,38,'muted')
   elif d['kind']=='diagram':
    # Conceptual chain, no flow magnitudes or claims about unobserved destinations.
    for j,label in enumerate(d['steps']):
     yy=y+j*80;s.circle(m+22,yy+26,9,'cyan');
     if j<2:s.line(m+22,yy+35,m+22,yy+98,'rule',3)
     s.text(label,m+60,yy,w-60,44,'ink',500)
    for j,label in enumerate(d['branches']):
     xx=m+j*(w/2);s.rect(xx,y+260,w/2-16,140,'panel');s.text(label,xx+20,y+280,w/2-55,40,'purple',500)
   else:
    for j,item in enumerate(d['items']):
     if engine=='beamer':s.line(m,y-8,1080-m,y-8,'rule')
     if engine=='html':s.rect(m-12,y-8,w+24,len(wrap(item,44,w-68))*54+28,'panel')
     s.text(f'{j+1:02d}',m,y,65,34,'cyan',500)
     y=s.text(item,m+75,y,w-75,44)+16
   # Editorial conclusion zone and source note stay separate from the chart.
   s.line(m,1034,1080-m,1034,accent,3)
   end=s.text(d['takeaway'],m,1055,w,44,accent,500)
   s.text(d['note'],m,max(1180,end+12),w,34,'muted',leading=1.15)
  s.text('EDUCACIÓN III',m,1310,w,24,'muted',500)
  s.rect(m,1342,w*(idx/9),4,'cyan')
  pages.append(s.ops)
 return pages

def export_html(pages,dest):
 styles=''.join(f'@font-face{{font-family:Fira;src:url("{f.as_uri()}");font-weight:{w}}}' for w,f in FONTS.items())
 chunks=[f'<!doctype html><html lang="es"><meta charset="utf-8"><title>Educación III · propuesta C</title><style>{styles}@page{{size:810pt 1012.5pt;margin:0}}*{{box-sizing:border-box}}body{{margin:0;background:#161616}}section{{position:relative;width:1080px;height:1350px;break-after:page;overflow:hidden}}section:last-child{{break-after:auto}}.obj{{position:absolute}}a{{color:inherit;text-decoration:none}}@media print{{body{{print-color-adjust:exact;-webkit-print-color-adjust:exact}}}}</style><body>']
 for ops in pages:
  chunks.append('<section>')
  for o in ops:
   k=o['kind'];base=f"left:{o['x']}px;top:{o['y']}px;"
   if k=='text':
    txt=html.escape(o['text']);txt=f'<a href="{html.escape(o["link"])}">{txt}</a>' if o['link'] else txt
    chunks.append(f'<div class="obj" style="{base}width:{o["w"]}px;font:{o["weight"]} {o["size"]}px/{o["leading"]} Fira;white-space:pre;color:#{o["color"]}">{txt}</div>')
   elif k in ['rect','circle']:chunks.append(f'<div class="obj" style="{base}width:{o["w"]}px;height:{o["h"]}px;background:#{o["color"]};border-radius:{"50%" if k=="circle" else "0"}"></div>')
   elif k=='image':chunks.append(f'<img class="obj" src="{Path(o["path"]).as_uri()}" style="{base}width:{o["w"]}px;height:{o["h"]}px" alt="">')
   elif k=='line':chunks.append(f'<svg class="obj" style="left:0;top:0;width:1080px;height:1350px"><line x1="{o["x"]}" y1="{o["y"]}" x2="{o["x2"]}" y2="{o["y2"]}" stroke="#{o["color"]}" stroke-width="{o["width"]}"/></svg>')
  chunks.append('</section>')
 chunks.append('</body></html>');dest.write_text(''.join(chunks))

def export_typst(pages,dest):
 q=lambda x:json.dumps(x,ensure_ascii=False)
 out=['#set page(width: 810pt, height: 1012.5pt, margin: 0pt)','#set text(font: "Fira Sans", lang: "es")','#set par(leading: 0pt)']
 for i,ops in enumerate(pages):
  if i:out.append('#pagebreak()')
  for o in ops:
   xy=f'dx:{o["x"]*.75}pt,dy:{o["y"]*.75}pt';k=o['kind']
   if k=='text':
    rows=[]
    for line in o['text'].split('\n'):
     rows.append(f'#box(height:{o["size"]*o["leading"]*.75}pt)[#text(size:{o["size"]*.75}pt,weight:{o["weight"]},fill:rgb("{o["color"]}"),top-edge:"ascender",bottom-edge:"descender",{q(line)})]')
    inner='#stack(dir: ttb, spacing: 0pt, '+','.join('['+r+']' for r in rows)+')'
    if o['link']:inner=f'#link({q(o["link"])})[{inner}]'
    body=f'box(width:{o["w"]*.75}pt)[{inner}]'
   elif k in ['rect','circle']:
    shape='ellipse' if k=='circle' else 'rect';body=f'{shape}(width:{o["w"]*.75}pt,height:{o["h"]*.75}pt,fill:rgb("{o["color"]}"),stroke:none)'
   elif k=='image':body=f'image({q(str(Path(o["path"]).relative_to(dest.parent)))},width:{o["w"]*.75}pt,height:{o["h"]*.75}pt)'
   else:body=f'line(end:({(o["x2"]-o["x"])*.75}pt,{(o["y2"]-o["y"])*.75}pt),stroke:(paint:rgb("{o["color"]}"),thickness:{o["width"]*.75}pt))'
   out.append(f'#place(top+left,{xy})[{"#"+body}]')
 dest.write_text('\n'.join(out))

def tex_escape(s):
 table={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
 return ''.join(table.get(c,c) for c in s)

def export_tex(pages,dest):
 out=[r'\documentclass{beamer}',r'\usepackage{fontspec,tikz,graphicx}',r'\setsansfont{Fira Sans}[BoldFont={Fira Sans Medium}]',r'\setbeamertemplate{navigation symbols}{}',r'\setbeamertemplate{headline}{}',r'\setbeamertemplate{footline}{}',r'\geometry{paperwidth=810bp,paperheight=1012.5bp}',r'\hypersetup{pdftitle={Educación III · propuesta B},pdfauthor={Cristián Labra Olivares}}',r'\begin{document}']
 for ops in pages:
  out.extend([r'\begin{frame}[plain]',r'\begin{tikzpicture}[remember picture,overlay,x=0.75bp,y=-0.75bp]',r'\begin{scope}[shift={(current page.north west)}]'])
  for o in ops:
   k=o['kind'];xy=f'({o["x"]},{o["y"]})';color=o.get('color','ffffff');out.append(r'\definecolor{oc}{HTML}{'+color+'}')
   if k=='text':
    txt=r'\\'.join(tex_escape(x).replace(' ',r'\hspace{0.25em}') for x in o['text'].split('\n'))
    if o['link']:txt=r'\href{'+o['link']+'}{'+txt+'}'
    font=r'\fontsize{'+str(o['size']*.75)+'bp}{'+str(o['size']*o['leading']*.75)+r'bp}\selectfont'+(r'\bfseries ' if o['weight']>=500 else ' ')
    out.append(r'\node[anchor=north west,inner sep=0,outer sep=0,text=oc,text width='+str(o['w']*.75)+r'bp,align=left] at '+xy+' {'+font+txt+'};')
   elif k=='rect':out.append(r'\fill[oc] '+xy+' rectangle '+f'({o["x"]+o["w"]},{o["y"]+o["h"]});')
   elif k=='circle':out.append(r'\fill[oc] '+f'({o["x"]+o["w"]/2},{o["y"]+o["h"]/2}) circle[radius={o["w"]*.375}bp];')
   elif k=='line':out.append(r'\draw[oc,line width='+str(o['width']*.75)+r'bp] '+xy+' -- '+f'({o["x2"]},{o["y2"]});')
   elif k=='image':out.append(r'\node[anchor=north west,inner sep=0] at '+xy+r' {\includegraphics[width='+str(o['w']*.75)+'bp,height='+str(o['h']*.75)+'bp]{'+o['path']+'}};')
  out.extend([r'\end{scope}',r'\end{tikzpicture}',r'\end{frame}'])
 out.append(r'\end{document}');dest.write_text('\n'.join(out))

def run(cmd,log,env=None,timeout=180):
 start=time.perf_counter()
 env=dict(os.environ) if env is None else env
 cache=P/'.tools/tex-cache-ready';cache.mkdir(exist_ok=True)
 env.update(TEXMFVAR=str(cache),TEXMFCACHE=str(cache))
 with log.open('w') as f:r=subprocess.run(cmd,cwd=P,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=timeout)
 if r.returncode:raise RuntimeError(f'{cmd[0]} exit {r.returncode}: {log}')
 return round(time.perf_counter()-start,3)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('engine',choices=[*CODE,'all']);ap.add_argument('--content',type=Path,default=P/'content.json');ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--generate-only',action='store_true');args=ap.parse_args()
 c=json.loads(args.content.read_text());args.output.mkdir(parents=True,exist_ok=True)
 for engine in CODE if args.engine=='all' else [args.engine]:
  pages=scenes(c,engine);prefix=args.output/CODE[engine]
  prefix.with_suffix('.scene.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
  if engine=='typst':export_typst(pages,prefix.with_suffix('.typ'))
  if engine=='beamer':export_tex(pages,prefix.with_suffix('.tex'))
  if engine=='html':export_html(pages,prefix.with_suffix('.html'))
  if args.generate_only:continue
  log=prefix.with_suffix('.build.log')
  if engine=='typst':
   cmd=[str(P/'.tools/root/usr/bin/typst'),'compile','--font-path','/usr/share/fonts/TTF','--root',str(P),str(prefix.with_suffix('.typ')),str(prefix.with_suffix('.pdf'))]
  elif engine=='beamer':cmd=['lualatex','--interaction=nonstopmode','--halt-on-error','--output-directory='+str(args.output),str(prefix.with_suffix('.tex'))]
  elif engine=='html':
   cmd=['node',str(P/'html_render.mjs'),str(prefix.with_suffix('.html')),str(prefix.with_suffix('.pdf'))]
  else:
   root=P/'.tools/root/usr'
   for d in ['scribus-data','scribus-cache','tmp']: (P/'.tools'/d).mkdir(exist_ok=True)
   cmd=['bwrap','--ro-bind','/','/','--dev-bind','/dev','/dev','--bind',str(P),str(P),'--bind','/tmp','/tmp','--overlay-src','/usr','--overlay-src',str(root),'--ro-overlay','/usr','--setenv','XDG_DATA_HOME',str(P/'.tools/scribus-data'),'--setenv','XDG_CACHE_HOME',str(P/'.tools/scribus-cache'),'--setenv','TMPDIR',str(P/'.tools/tmp'),'/usr/bin/scribus','-platform','offscreen','-g','-ns','-pr',str(P/'.tools/scribus-prefs'),'-py',str(P/'scribus_render.py'),str(prefix)]
  seconds=run(cmd,log,timeout=300)
  if engine=='html':
   from pypdf import PdfReader,PdfWriter
   pdf=prefix.with_suffix('.pdf');writer=PdfWriter(clone_from=PdfReader(pdf))
   for page in writer.pages:
    page.mediabox.upper_right=(810,1012.5)
    if '/CropBox' in page: page.cropbox.upper_right=(810,1012.5)
   tmp=pdf.with_suffix('.normalized.pdf');writer.write(tmp);tmp.replace(pdf)
  receipt={'engine':engine,'seconds':seconds,'content_sha256':hashlib.sha256(args.content.read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(prefix.with_suffix('.pdf').read_bytes()).hexdigest(),'command':cmd,'generated_at':time.strftime('%Y-%m-%dT%H:%M:%S%z')}
  prefix.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2));print(engine,seconds,'s',flush=True)
if __name__=='__main__':main()
