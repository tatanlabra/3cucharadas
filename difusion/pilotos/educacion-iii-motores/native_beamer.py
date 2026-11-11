"""Beamer composition: native TeX paragraphs/minipages, TikZ intervals."""
def esc(s):
 return ''.join({'&':r'\&','%':r'\%','_':r'\_','#':r'\#','$':r'\$','{':r'\{','}':r'\}'}.get(x,x) for x in s)
def fmt(n):return ('+' if n>0 else '−' if n<0 else '')+f'{abs(n):.2f}'.replace('.',',')
def build(c,out,assets):
 def t(s,size=30,color='ink',bold=False):return '{\\color{'+color+'}\\fontsize{'+str(size)+'bp}{'+str(size*1.22)+'bp}\\selectfont'+(r'\bfseries' if bold else '')+r'\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000\spaceskip=.25em\xspaceskip=.25em '+esc(s)+r'\par}'
 pre=r'''\documentclass{beamer}
\usepackage{fontspec,tikz,graphicx}
\setsansfont{Fira Sans}[BoldFont={Fira Sans Medium}]
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{headline}{}\setbeamertemplate{footline}{}
\geometry{paperwidth=810bp,paperheight=1012.5bp}
\setbeamersize{text margin left=50bp,text margin right=50bp}
\definecolor{darkbg}{HTML}{161616}\definecolor{ink}{HTML}{F2F5F8}\definecolor{muted}{HTML}{B5BECA}\definecolor{cyan}{HTML}{64D8E9}\definecolor{purple}{HTML}{A79CFF}\definecolor{panel}{HTML}{202329}\definecolor{rule}{HTML}{424953}
\setbeamercolor{background canvas}{bg=darkbg}\setbeamercolor{normal text}{fg=ink}
\hypersetup{pdftitle={Educación III · B},pdfauthor={Cristián Labra Olivares}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}\raggedright
\begin{document}
'''
 pages=[]
 for i,d in enumerate(c['slides'],1):
  p=[r'\begin{frame}[plain,t]\vspace*{30bp}\begin{minipage}[t][930bp][t]{710bp}',t('3 Cucharadas  /  EDUCACIÓN III',22,'muted'),r'\vspace{28bp}',t(d['kicker'],22,'purple',True)]
  special=d['kind'] in ['cover','cta']
  if special:
   p += [r'\vspace{16bp}',r'\includegraphics[width=710bp,height=320bp,keepaspectratio]{'+str(assets/'hero.png')+'}'+r'\par',r'\vspace{22bp}',t(d['title'],57,'ink',True),r'\vspace{18bp}',t(d['body'],30)]
  else:
   p += [r'\vspace{18bp}',t(d['title'],46,'ink',True),r'\vspace{18bp}',t(d['body'],30),r'\vspace{24bp}']
   if d['kind']=='chart':
    lo,hi=d['domain'];x=lambda v:18+(v-lo)/(hi-lo)*270
    p += [r'\begin{minipage}{710bp}']
    for j,r in enumerate(d['rows']):
     color='cyan' if j==0 else 'purple'
     p += [r'\begin{minipage}[t]{337bp}',r'{\color{'+color+r'}\rule{337bp}{3bp}}',r'\vspace{14bp}',t(r['label'],27,'muted'),r'\vspace{8bp}',t(fmt(r['value']),72,color,True),r'\vspace{12bp}',t(f'[{fmt(r["lo"])}; {fmt(r["hi"])}]',26,'ink'),r'\vspace{16bp}',r'\begin{tikzpicture}[x=1bp,y=1bp]']
     for v in d['ticks']:
      p += [r'\draw[rule] ('+str(x(v))+',0) -- ('+str(x(v))+',24);',r'\node[anchor=north,text=muted,font=\fontsize{21bp}{24bp}\selectfont] at ('+str(x(v))+',-8) {'+esc(str(v))+'};']
     p += [r'\draw['+color+',line width=3bp] ('+str(x(r['lo']))+',12) -- ('+str(x(r['hi']))+',12);',r'\fill['+color+'] ('+str(x(r['value']))+',12) circle (5bp);',r'\end{tikzpicture}\end{minipage}']
     if j==0:p += [r'\hfill']
    p += [r'\end{minipage}\par',r'\vspace{28bp}',t(d['interval']+' · puntos porcentuales',23,'muted')]
   elif d['kind']=='diagram':
    for j,v in enumerate(d['steps']):p += [t(f'{j+1:02d}   '+v,34,'ink',True),r'\vspace{10bp}']
    p += [r'\vspace{12bp}']
    for v in d['branches']:p += [t('→ '+v,30,'purple'),r'\vspace{8bp}']
   elif d['kind']=='method':
    for j,r in enumerate(d['cards']):p += [r'{\color{rule}\rule{710bp}{1bp}}',r'\vspace{12bp}',t(r['label']+'  /  '+r['text'],38,'cyan' if j==0 else 'purple',True),r'\vspace{22bp}']
   elif 'items' in d:
    for j,v in enumerate(d['items']):p += [r'\begin{minipage}[t]{44bp}',t(str(j+1),28,'purple',True),r'\end{minipage}\begin{minipage}[t]{660bp}',t(v,30),r'\end{minipage}\par',r'\vspace{22bp}']
  p += [r'\vfill',r'{\color{purple}\rule{710bp}{3bp}}',r'\vspace{14bp}']
  if d['kind']=='cta':p += [r'\href{'+c['url']+'}{'+t(d['takeaway']+' ↗',33,'cyan',True).replace(r'\par','')+'}'+r'\par']
  else:p += [t(d['takeaway'],31,'purple',True)]
  p += [r'\vspace{16bp}',t(d['note'],23,'muted'),r'\vspace{16bp}',t(f'{i:02d} / 09',20,'muted'),r'\end{minipage}\end{frame}'];pages.append('\n'.join(p))
 out.write_text(pre+'\n'.join(pages)+r'\end{document}')
