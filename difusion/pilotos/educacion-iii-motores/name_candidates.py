"""Human-facing names; internal A-D IDs remain stable for receipts."""
from pathlib import Path
import shutil,json
P=Path(__file__).resolve().parent;O=P/'out/native'
NAMES={'A':('Typst','Typst'),'B':('Beamer / LuaLaTeX','Beamer'),'C':('HTML/CSS · Chromium','HTML-CSS'),'D':('Scribus','Scribus')}
for code,(label,stem) in NAMES.items():shutil.copy2(O/f'{code}.pdf',O/f'{stem}.pdf')
p=O/'index.html';text=p.read_text().replace('Revisa primero legibilidad, jerarquía, espacio y gráficos; después revela los motores.','Compara legibilidad, jerarquía, espacio y gráficos; revisa también las diferencias operativas de cada motor.').replace('Revelar motores y mediciones','Tecnologías y mediciones')
for code,(label,stem) in NAMES.items():
 text=text.replace(f'Propuesta {code}',label).replace(f'Abrir PDF {code}',f'Abrir PDF · {label}').replace(f'href="{code}.pdf"',f'href="{stem}.pdf"').replace(f'<td>{code}</td>',f'<td>{label}</td>')
text=text.replace('const select=document.querySelector', 'const labels='+json.dumps({k:v[0] for k,v in NAMES.items()},ensure_ascii=False)+';\nconst select=document.querySelector').replace('img.alt=`Propuesta ${c}, página ${n}`','img.alt=`${labels[c]}, página ${n}`').replace('Ejemplo: C, página 4:','Ejemplo: HTML/CSS, página 4:')
p.write_text(text)
