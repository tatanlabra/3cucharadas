#!/usr/bin/env python3
"""Deterministic crop/resize/encode of selected editorial art; no image synthesis."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageOps
import yaml

class Quoted(str):
    """Keep locale-formatted figures strings in Ruby/Psych as well as PyYAML."""

yaml.SafeDumper.add_representer(Quoted, lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:str', value, style='"'))

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/plans/20260912-heroes-casen/evidence/images'
VARIANTS = {
    'hero': (1600, 900, 250000, 'hero'),
    'hero-mobile': (800, 450, 100000, 'hero'),
    'teaser': (1280, 720, 180000, 'teaser'),
    'teaser-mobile': (640, 360, 70000, 'teaser'),
    'og': (1200, 630, 180000, 'og'),
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def encode(source, output, size, budget, compact):
    frame = source
    if compact:
        width, height = frame.size
        frame = frame.crop((round(width*.08), round(height*.04), width, round(height*.96)))
    frame = ImageOps.fit(frame, size, method=Image.Resampling.LANCZOS, centering=(.65,.5))
    for quality in (88,84,80,76,72):
        frame.save(output, 'WEBP', quality=quality, method=6, exact=True)
        if output.stat().st_size <= budget:
            return quality
    raise ValueError(f'Image quality/weight conflict: {output}; do not silently overcompress')

def build(selection):
    inventory=json.loads((EVIDENCE.parent/'inventory.json').read_text())
    public=[]
    for ref, item in selection.items():
        posts=[p['file'] for p in inventory if p['ref']==ref]
        if len(posts)!=2:
            raise ValueError(f'Expected a bilingual pair for {ref}')
        source=Path(item['source'])
        if not source.is_absolute():
            source=ROOT/source
        if not source.is_file():
            raise FileNotFoundError(source)
        master=EVIDENCE/'sources'/(ref+source.suffix)
        master.parent.mkdir(parents=True,exist_ok=True)
        if master.exists() and digest(master)!=digest(source):
            raise ValueError('An immutable master already exists with different content')
        if not master.exists():
            shutil.copyfile(source,master)
        image=ImageOps.exif_transpose(Image.open(master)).convert('RGB')
        destination=ROOT/'assets/images/heroes-v2'/ref
        destination.mkdir(parents=True,exist_ok=True)
        visual_id=item['visual_id']
        catalog_path=ROOT/'_data/visuales'/(visual_id+'.yml')
        catalog=yaml.safe_load(catalog_path.read_text()) if catalog_path.exists() else {'slug':visual_id,'ref':ref,'posts':posts,'piezas':[]}
        catalog['ref']=ref
        catalog['posts']=posts
        catalog['piezas']=[x for x in catalog.get('piezas',[]) if not x['id'].startswith('editorial-v2-')]
        for piece in catalog['piezas']:
            if 'cifras' in piece:
                piece['cifras'] = [Quoted(str(value)) for value in piece['cifras']]
        paths={}
        for name,(width,height,budget,role) in VARIANTS.items():
            file=destination/f'{name}-{width}x{height}.webp'
            quality=encode(image,file,(width,height),budget,name in ('teaser','teaser-mobile','og'))
            relative=file.relative_to(ROOT).as_posix()
            piece={'id':'editorial-v2-'+name,'rol':role,'archivo':relative,'estado':'publicable',
                   'origen':'ia-integrada' if item['ai_generated'] else 'procedencia-no-documentada',
                   'ancho':width,'alto':height,'bytes':file.stat().st_size,'sha256':digest(file),
                   'alt':item['alt'],
                   'provenance':{'status':item['provenance_status'],'source_sha256':digest(master),
                                 'note':item['note'],'encoding':f'WebP quality={quality}; Lanczos; deterministic derivative'}}
            if item.get('tool'):
                piece['provenance'].update(tool=item['tool'],provider='OpenAI',interface='Codex')
            catalog['piezas'].append(piece)
            paths[name]='/'+relative
        catalog_path.write_text(yaml.safe_dump(catalog,allow_unicode=True,sort_keys=False,width=110))
        public.append({'ref':ref,'visual_id':visual_id,'paths':paths,'ai_generated':item['ai_generated'],'alt':item['alt']})
    (EVIDENCE/'derivatives.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'families':len(public),'derivatives':len(public)*len(VARIANTS)},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--selection',type=Path,default=EVIDENCE/'selected-sources.json')
    args=parser.parse_args()
    build(json.loads(args.selection.read_text()))
