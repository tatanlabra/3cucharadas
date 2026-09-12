#!/usr/bin/env python3
import sys,json,pathlib
fixture=sys.argv[1]
rows=[r for r in json.loads((pathlib.Path(__file__).parent/'playwright-runs.json').read_text()) if r['fixture']==fixture]
assert len(rows)==4
values=[r['sample']['lcp'][-1]['startTime'] if r['sample']['lcp'] else None for r in rows]
passed=all(v is not None and v<=2500 for v in values)
print(json.dumps({'fixture':fixture,'standard_lcp_ms':values,'threshold_ms':2500,'pass':passed}))
sys.exit(0 if passed else 1)
