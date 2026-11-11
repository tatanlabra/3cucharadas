#!/usr/bin/env python3
from pathlib import Path
import subprocess,re
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;O=P/'out/native';font=ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Medium.ttf',22)
names={'A':'Typst','B':'Beamer','C':'HTML/CSS','D':'Scribus'}
for code in 'ABCD':
 dest=O/'previews'/code;dest.mkdir(parents=True,exist_ok=True)
 subprocess.run(['pdftoppm','-r','96','-png',str(O/(code+'.pdf')),str(dest/'page')],check=True)
 imgs=sorted((p for p in dest.glob('page-*.png') if re.fullmatch(r'page-\d+\.png',p.name)),key=lambda p:int(p.stem.split('-')[1]))
 canvas=Image.new('RGB',(1080,1400),'#0d1016');draw=ImageDraw.Draw(canvas)
 for i,p in enumerate(imgs):
  im=Image.open(p).convert('RGB');thumb=im.resize((328,410),Image.Resampling.LANCZOS)
  x=18+(i%3)*360;y=48+(i//3)*450;canvas.paste(thumb,(x,y));draw.text((x,y-28),f'{names[code]} · {i+1:02d}',font=font,fill='white')
  for width in [320,390]:im.resize((width,round(width*1.25)),Image.Resampling.LANCZOS).save(dest/(p.stem+f'-{width}.png'))
 canvas.save(O/f'{code}-mosaic.png')
 print(code,len(imgs),flush=True)
for page in range(1,10):
 canvas=Image.new('RGB',(1560,540),'#0d1016');draw=ImageDraw.Draw(canvas)
 for j,code in enumerate('ABCD'):
  im=Image.open(O/'previews'/code/f'page-{page}-390.png')
  canvas.paste(im,(390*j,40));draw.text((390*j+12,8),f'{names[code]} · {page:02d}',font=font,fill='white')
 canvas.save(O/f'compare-{page:02d}.png')
