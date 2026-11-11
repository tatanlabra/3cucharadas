"""Typst composition: flowing stack/grid, native wrapping, fractional space."""
import json,os,re
q=lambda s:json.dumps(s,ensure_ascii=False)
def fmt(n):return ('+' if n>0 else '−' if n<0 else '')+f'{abs(n):.2f}'.replace('.',',')
def build(c,out,assets):
 def txt(t,size=31,color='ink',weight=400):return f'#text(size:{size}pt,fill:{color},weight:{weight},{q(t)})'
 def chart(d):
  lo,hi=d['domain'];x=lambda v:18+(v-lo)/(hi-lo)*635;blocks=[]
  for j,r in enumerate(d['rows']):
   color='cyan' if j==0 else 'purple'
   shapes=[f'#place(dx:{x(v)}pt,dy:0pt)[#line(end:(0pt,30pt),stroke:rule)]' for v in d['ticks']]
   shapes += [f'#place(dx:{x(r["lo"])}pt,dy:15pt)[#line(end:({x(r["hi"])-x(r["lo"])}pt,0pt),stroke:(paint:{color},thickness:3pt))]',f'#place(dx:{x(r["value"])-5}pt,dy:10pt)[#circle(radius:5pt,fill:{color},stroke:none)]']
   shapes += [f'#place(dx:{x(v)-12}pt,dy:36pt)[{txt(str(v).replace("-","−"),23,"muted")}]' for v in d['ticks']]
   blocks.append('['+txt(r['label']+' · '+fmt(r['value'])+f' [{fmt(r["lo"])}; {fmt(r["hi"])}]',26,color,500)+']')
   blocks.append('[#box(width:100%,height:64pt)['+''.join(shapes)+']]')
  blocks.append('['+txt(d['interval']+' · puntos porcentuales',23,'muted')+']')
  return '#stack(dir:ttb,spacing:12pt,'+','.join(blocks)+')'
 header='''#let ink=rgb("f2f5f8")
#let muted=rgb("b5beca")
#let cyan=rgb("64d8e9")
#let purple=rgb("a79cff")
#let rule=rgb("424953")
#set page(width:810pt,height:1012.5pt,margin:(x:60pt,y:42pt),fill:rgb("161616"))
#set text(font:"Fira Sans",size:31pt,fill:ink,lang:"es")
#set par(leading:0.6em,justify:false)
'''
 pages=[]
 for i,d in enumerate(c['slides'],1):
  parts=[f'[#grid(columns:(1fr,auto),[{txt("3 Cucharadas",24,"ink",500)}],[{txt(f"{i:02d} / 09",22,"muted")}])]', '[#v(24pt,weak:false)]','['+txt(d['kicker'],23,'cyan',500)+']']
  special=d['kind'] in ['cover','cta']
  if special:
   parts+=['[#v(12pt,weak:false)]','['+txt(d['title'],66,'ink',500)+']','[#v(18pt,weak:false)]',f'[#align(right)[#image({q(os.path.relpath(assets/"hero.png",out.parent))},width:570pt,height:280pt,fit:"cover")]]','[#v(18pt,weak:false)]','['+txt(d['body'])+']']
  else:
   parts+=['[#v(12pt,weak:false)]','['+txt(d['title'],48,'ink',500)+']','[#v(18pt,weak:false)]','['+txt(d['body'])+']','[#v(26pt,weak:false)]']
   parts+=['0.35fr']
   if d['kind']=='chart':parts+=['['+chart(d)+']']
   elif d['kind']=='method':
    parts+=['[#grid(columns:(1fr,1fr),gutter:24pt,'+','.join('[#line(length:100%,stroke:'+('cyan' if j==0 else 'purple')+')\n#v(18pt,weak:false)\n'+txt(r['label'],41,'ink',500)+'\n#v(12pt,weak:false)\n'+txt(r['text'],28,'muted')+']' for j,r in enumerate(d['cards']))+')]']
   elif d['kind']=='diagram':
    parts+=['[#stack(dir:ttb,spacing:12pt,'+','.join('['+txt(f'{j+1:02d}  '+v,31,'ink',500)+']' for j,v in enumerate(d['steps']))+')]','[#v(20pt,weak:false)]','[#grid(columns:(1fr,1fr),gutter:20pt,'+','.join('['+txt(v,30,'purple',500)+']' for v in d['branches'])+')]']
   elif 'items' in d:
    parts+=['[#stack(dir:ttb,spacing:18pt,'+','.join('[#grid(columns:(38pt,1fr),gutter:12pt,['+txt(f'{j+1:02d}',24,'cyan')+'],['+txt(v,31)+'])]' for j,v in enumerate(d['items']))+')]']
  tail=txt(d['takeaway'],31,'cyan',500)
  if d['kind']=='cta':tail=f'#link({q(c["url"])})[{tail} ↗]'
  parts+=['[#v(1fr)]','[#line(length:100%,stroke:cyan)]','[#v(15pt,weak:false)]','['+tail+']','[#v(18pt,weak:false)]','['+txt(d['note'],23,'muted')+']']
  pages.append('#block(width:100%,height:100%)[#stack(dir:ttb,spacing:0pt,'+','.join(parts)+')]')
 source=header+'\n#pagebreak()\n'.join(pages)
 source=re.sub(r'\[#v\((\d+)pt,weak:false\)\]',r'\1pt',source).replace('[#v(1fr)]','0.65fr')
 out.write_text(source)
