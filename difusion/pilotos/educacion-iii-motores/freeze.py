from pathlib import Path
import hashlib,json,datetime
p=Path(__file__).resolve().parent; repo=p.parents[2]
c=json.loads((p/'content.json').read_text())
s=repo/c['source']; raw=s.read_text()
assert len(c['slides'])==9
for slide in c['slides']:
 for claim in slide['source_claims']: assert claim in raw,claim
m={'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':c['source'],'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'content_sha256':hashlib.sha256((p/'content.json').read_bytes()).hexdigest(),'decisions':['9 láminas actualizadas','fuentes especializadas','cuatro motores locales','misma identidad; composición libre'],'assets':{}}
for rel in ['assets/images/heroes-v2/costos-cierre-escolar-trayectorias/hero-1600x900.webp','assets/images/3cucharadas-logo-128.webp']:
 m['assets'][rel]=hashlib.sha256((repo/rel).read_bytes()).hexdigest()
(p/'source-lock.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
print('Frozen',m['content_sha256'])
