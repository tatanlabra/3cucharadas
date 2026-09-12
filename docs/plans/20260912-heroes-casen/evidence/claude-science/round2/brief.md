# D2 round2: focused scientific correction review
Read only. No tools or edits needed; no raw microdata provided. Prior independent Anthropic Sonnet review below verified the statistical core and hand-derived two variance oracles, but raised P1 F1: as.numeric(factor) corruption. Review the corrected R boundary, tests and reported real source metadata; also F3 clarification. Source digest now 14eaab859814dda0d89066b79c7b395b8e1cbb3e90aa7e65f5f080fe3dddec80. Return JSON task_id D2, source_digest, provider, requested_model sonnet, effective_identity_evidence, findings with severity/status/remedy, open_p0_p1, verdict, limitations. Decide explicitly whether F1 is resolved and current D1 accepted. Do not invent executed checks; assess attached red/green receipts plus code. F2 global singleton policy stays deliberately failclosed; actual source has no singleton. Prior science core unchanged.
## Prior review
{
  "task_id": "D2",
  "source_digest": "e40cae6a5f77becf9634b51c1e4b75be3ea21bc1f2cfd56d5dd487c61d5b791f",
  "provider": "anthropic",
  "requested_model": "sonnet (alias)",
  "effective_identity_evidence": {
    "self_report": "claude-sonnet-5 (Sonnet 5), Anthropic — as stated by this session's own harness system-reminder",
    "runtime_evidence": "none observable independent of the harness-injected string; no API/header introspection available from within the session",
    "note": "these are the same source (harness-supplied), not two independent confirmations"
  },
  "findings": [
    {
      "id": "F1",
      "severity": "P1",
      "epistemic_status": "abductive, unconfirmed — cannot verify without the actual RData column classes",
      "file": "scripts/casen_shared_site.py",
      "line": "56-58",
      "claim": "The R extraction script applies as.numeric() uniformly to all selected columns (v9, v28, pco1, region, area, varstrat, varunit, id_vivienda). If any of these columns are stored as base-R factor (rather than numeric/haven_labelled) in the source .RData, as.numeric(factor) returns the factor's *level index*, not its numeric value.",
      "counterexample": "If v9 is a factor with levels sorted lexicographically ('1','10','11','2','3',...,'9'), a household truly coded v9=2 gets remapped to as.numeric()=4 — landing exactly on the 'shared site' positive code (3/4) that this pipeline measures. The corrupted value still falls inside 1..11, so it passes both the codebook sanity check (which validates the Excel dictionary, not the extracted data) and the 'undocumented v9 code' guard. Same risk applies to pco1 (head selection) and varstrat/varunit (design integrity).",
      "remedy": "In the R script, assert `stopifnot(!any(sapply(d[cols], is.factor)))` before conversion (fail closed, consistent with the pipeline's own stated policy), or explicitly `as.numeric(as.character(x))` per factor column. Add an integration test that exercises the actual R subprocess path with a small synthetic .RData fixture — current tests (test_casen_shared_site.py) only feed synthetic pandas DataFrames directly into Python and never execute scripts/casen_shared_site.py:56-58, so this path has zero test coverage."
    },
    {
      "id": "F2",
      "severity": "P2",
      "epistemic_status": "confirmed by code reading; documented as intentional in docs/casen-shared-site-method.md:27",
      "file": "src/casen_shared_site/core.py",
      "line": "100-108",
      "claim": "Singleton-stratum invalidation (`counts.eq(1).any()`) is computed over ALL design strata nationally, not scoped to the estimation domain. A singleton stratum belonging to an unrelated region would null the CI for every other region and the national estimate too.",
      "counterexample": "Not observed in this run (no singleton strata in the current design, per audit.json design block) — this is a latent risk in future waves, not an active defect here.",
      "remedy": "Optional: none needed today. If finer-grained estimability is ever required, scope the singleton check to strata with nonzero e-contribution in-domain. Current behavior fails closed, which is the safe direction."
    },
    {
      "id": "F3",
      "severity": "P2",
      "epistemic_status": "confirmed by code reading",
      "file": "src/casen_shared_site/core.py",
      "line": "48",
      "claim": "`heads['flagged'] = False` is a constant; any real inconsistency raises before this line, so `n_flagged` is vacuously 0 in every successful export.",
      "counterexample": "n/a — always 0 by construction, in every possible successful run.",
      "remedy": "Drop the field, or document explicitly in audit.json/method doc that n_flagged=0 is a tautology of the fail-closed design, not a QA signal."
    }
  ],
  "limitations": [
    "No execution performed (read-only per task instruction); Taylor-ratio arithmetic for 2 of the 3 manual oracles was independently hand-recomputed and matches the stated results exactly (8/81, 3/16) — this is genuine independent verification, not trust of the green test log.",
    "R extraction path, Excel codebook parsing (codebook_values), and Census/Stata reads could not be verified against actual source files (no access to original microdata, none provided).",
    "verification.json's mutation-test claims and formats/hash equality (AggregateArtifacts) are taken as reported, not re-executed.",
    "Green tests do not constitute proof of representativeness, causality, or R-side type safety — consistent with the module's own stated caveat."
  ],
  "verdict": "accept_with_limitations — household/dwelling separation, denominator (all valid v9, no ownership/v28 restriction), full-design PSU domain handling, and Taylor linearization are correctly implemented and partially independently re-derived by hand. Outstanding P1 (F1) is a plausible, unconfirmed silent-corruption risk in the R→Python boundary that the current guards do not actually catch; must be resolved (assert non-factor + add R-path test) before trusting this pipeline against a new CASEN wave."
}

## src/casen_shared_site/rdata.py
```
"""Strict RData boundary: numeric storage only, inspected before conversion.

Original observations never reach disk; R stdout carries selected numeric columns
into Python memory. R stderr carries only declared column/class metadata.
"""
from __future__ import annotations
import io
import subprocess
from pathlib import Path
import pandas as pd

FIELDS = ('folio', 'id_persona', 'id_vivienda', 'pco1', 'v9', 'v28', 'expr',
          'varstrat', 'varunit', 'region', 'area')

R_READER = r'''
args <- commandArgs(TRUE)
e <- new.env()
load(args[1], envir=e)
ds <- Filter(is.data.frame, as.list(e))
if (length(ds) != 1L) stop("INVALID_RDATA_FRAME_COUNT")
d <- ds[[1L]]
cols <- strsplit(args[2], ",", fixed=TRUE)[[1L]]
if (!all(cols %in% names(d))) stop("MISSING_SELECTED_COLUMNS")
cat("CASEN_FRAME\t", nrow(d), "\t", ncol(d), "\n", sep="", file=stderr())
allowed_classes <- c("numeric", "integer", "double", "haven_labelled", "haven_labelled_spss",
                     "vctrs_vctr", "labelled")
safe <- logical(length(cols))
for (i in seq_along(cols)) {
  x <- d[[cols[i]]]
  classes <- class(x)
  cat("CASEN_COLUMN\t", cols[i], "\t", typeof(x), "\t",
      paste(classes, collapse="|"), "\n", sep="", file=stderr())
  safe[i] <- !is.factor(x) && is.numeric(x) &&
             typeof(x) %in% c("integer", "double") &&
             !inherits(x, "integer64") && all(classes %in% allowed_classes) &&
             is.null(dim(x))
}
if (!all(safe)) {
  cat("UNSUPPORTED_R_COLUMN\t", paste(cols[!safe], collapse=","), "\n",
      sep="", file=stderr())
  stop("UNSUPPORTED_R_COLUMN")
}
if (args[3] == "data") {
  # Strip attributes only AFTER validation, preventing custom S3 coercion dispatch.
  out <- as.data.frame(lapply(d[cols], function(x) {
    attributes(x) <- NULL
    as.numeric(x)
  }))
  write.table(out, stdout(), sep=",", row.names=FALSE, na="", quote=FALSE)
}
'''


def _run_r_reader(path: Path, fields, mode, rscript='Rscript'):
    fields = tuple(fields)
    if not fields or len(set(fields)) != len(fields) or not all(f in FIELDS for f in fields):
        raise ValueError('Unsupported selected RData fields')
    result = subprocess.run([rscript, '--vanilla', '-e', R_READER,
                             str(path), ','.join(fields), mode],
                            capture_output=True, check=False)
    metadata = {'columns': {}, 'coercion_policy': 'numeric storage and approved numeric/labelled classes only; factors, character, integer64 and unknown classes rejected before coercion'}
    rejected = []
    for line in result.stderr.decode('utf-8', errors='replace').splitlines():
        parts = line.split('\t')
        if parts[0] == 'CASEN_FRAME' and len(parts) == 3:
            metadata.update(n_rows=int(parts[1]), n_source_columns=int(parts[2]))
        elif parts[0] == 'CASEN_COLUMN' and len(parts) == 4:
            metadata['columns'][parts[1]] = {'storage_type': parts[2], 'classes': parts[3].split('|')}
        elif parts[0] == 'UNSUPPORTED_R_COLUMN' and len(parts) == 2:
            rejected.extend(parts[1].split(','))
    if result.returncode:
        # Do not publish raw stderr, which may contain the private input filename.
        reason = 'unsupported R column types: ' + ','.join(rejected) if rejected else 'RData extraction failed'
        raise ValueError(f'{reason} (R exit {result.returncode})')
    if set(metadata['columns']) != set(fields) or 'n_rows' not in metadata:
        raise ValueError('Incomplete R column type audit')
    metadata.update(selected_columns=len(fields), rejected_columns=0, factors_present=False,
                    integer64_present=False, r_exit_code=result.returncode)
    return result.stdout, metadata


def inspect_rdata_columns(path: Path, fields=FIELDS, rscript='Rscript'):
    """Read only source structure/class metadata; no observation is emitted."""
    output, metadata = _run_r_reader(path, fields, 'metadata', rscript)
    if output:
        raise ValueError('Metadata inspection unexpectedly emitted observation data')
    return metadata


def read_rdata_numeric(path: Path, fields=FIELDS, rscript='Rscript'):
    """Load validated selected numeric columns in memory, with their class audit."""
    output, metadata = _run_r_reader(path, fields, 'data', rscript)
    frame = pd.read_csv(io.BytesIO(output), skip_blank_lines=False)
    if list(frame.columns) != list(fields) or len(frame) != metadata['n_rows']:
        raise ValueError('R extraction output/schema mismatch')
    return frame, metadata

```

## scripts/casen_shared_site.py
```
#!/usr/bin/env python3
"""Read original CASEN sources; export only household aggregates and provenance."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from casen_shared_site.core import prepare_households, estimates, require
from casen_shared_site.rdata import read_rdata_numeric


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def codebook_values(path,sheet,variable):
    data = pd.read_excel(path,sheet_name=sheet,header=None)
    match = data.index[data.iloc[:,1].eq(variable)]
    require(len(match)==1,f'codebook variable ambiguous: {variable}')
    i=int(match[0]); out={}
    while i<len(data) and (i==match[0] or pd.isna(data.iloc[i,1])):
        value,label=data.iloc[i,3],data.iloc[i,4]
        if isinstance(value,(int,float,np.number)) and not pd.isna(value): out[int(value)]=str(label).strip()
        i+=1
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['rdata','communes','codebook','communal-codebook','use-note','commune-universe']:
        parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--out',type=Path,default=ROOT/'artifacts/casen_shared_site')
    args=parser.parse_args()
    inputs={k:getattr(args,k.replace('-','_')) for k in ['rdata','communes','codebook','communal-codebook','use-note','commune-universe']}
    source_hashes={k:sha256(p) for k,p in inputs.items()}
    code_paths=[Path(__file__),*(ROOT/'src/casen_shared_site').glob('*.py')]
    code_hashes={str(p.relative_to(ROOT)):sha256(p) for p in code_paths}
    v9=codebook_values(args.codebook,'V','v9')
    require(set(v9)==set(range(1,12)),'v9 codebook codes changed')
    v28=codebook_values(args.codebook,'V','v28')
    require(set(v28)=={1,2},'v28 codebook codes changed')
    communal_book=pd.read_excel(args.communal_codebook,sheet_name='Base provincia comuna',header=None)
    require({'folio','id_persona','expc','comuna'}.issubset(set(communal_book.iloc[:,1].dropna())), 'communal codebook fields changed')
    region_names=codebook_values(args.codebook,'HdR','region')
    persons,r_metadata=read_rdata_numeric(args.rdata)
    with pd.io.stata.StataReader(args.communes,convert_categoricals=False) as reader:
        labels=reader.value_labels()
        communal=reader.read()
    # Numeric commune codes are labels supplied in the official complementary DTA.
    commune_labels=labels.get('comuna',{})
    if not commune_labels:
        candidates=[m for m in labels.values() if 5101 in m and 13101 in m]
        require(len(candidates)==1,'commune label dictionary unavailable')
        commune_labels=candidates[0]
    commune_names={int(k):str(v).strip() for k,v in commune_labels.items()}
    census=pd.read_excel(args.commune_universe,sheet_name='2',header=3)
    census=census.loc[pd.to_numeric(census['Código comuna'],errors='coerce').gt(0)]
    universe={int(row['Código comuna']):str(row['Comuna']).strip() for _,row in census.iterrows()}
    require(len(universe)==len(census),'duplicate commune in Census universe')
    require(set(commune_names).issubset(universe),'CASEN commune outside Census universe')
    # Keep official CASEN names for sampled communes; Census supplies absent names.
    commune_names={code:commune_names.get(code,name) for code,name in universe.items()}
    heads,audit=prepare_households(persons,communal)
    audit['r_extraction']=r_metadata
    require(set(heads.region.unique())==set(range(1,17)),'source lacks a region')
    rows,sensitivity=estimates(heads,region_names,commune_names)
    missing_codes=sorted(set(universe)-set(heads.comuna.unique()))
    audit['commune_coverage']={'universe_source':args.commune_universe.name,'sheet':'2',
                              'universe_n':len(universe),'sampled_n':int(heads.comuna.nunique()),
                              'no_sample_n':len(missing_codes),
                              'no_sample':[{'territory_code':str(c),'territory_name':universe[c],'estimate':None,'ci_status':'no_sample'} for c in missing_codes]}
    audit.update(schema_version=1,sensitivity=sensitivity,codebook={'v9_valid':v9,'v9_positive':[3,4],'v9_missing_observed':audit['n_missing_v9'],'v28':v28},
                 ci={'method':'with-replacement ultimate-cluster Taylor ratio; complete household design including outside-domain PSU',
                     'z':1.959963985,'singleton_policy':'any singleton => SE/CI null; no undocumented adjustment',
                     'n_psu_definition':'All distinct (varstrat,varunit) pairs in full household sample, even outside domain',
                     'n_strata_definition':'All full-sample variance strata','finite_population_correction':False,
                     'commune':'descriptive, nonrepresentative, no CI'},
)
    audit['r2']={'formula':'R2(p_v) = R1 / (1 - p_v / 2)',
                 'assumptions':'p_v is hypothetical share of DWELLINGS in sites containing exactly two dwellings; all other sites contain one dwelling; R1=roles/dwellings, R2=roles/sites.',
                 'applied_to_fiscal_gap':False,'household_rate_used_as_parameter':False}
    require(source_hashes=={k:sha256(p) for k,p in inputs.items()},'source changed during execution')
    require(code_hashes=={str(p.relative_to(ROOT)):sha256(p) for p in code_paths},'code changed during execution')
    args.out.mkdir(parents=True,exist_ok=True)
    table=pd.DataFrame(rows)
    table.to_csv(args.out/'estimates.csv',index=False)
    table.to_parquet(args.out/'estimates.parquet',index=False)
    def write(name,obj): (args.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    write('estimates.json',{'schema_version':1,'estimand':'p_h: household reports own site shared with other dwellings (v9=3/4) / all valid households','rows':rows})
    write('audit.json',audit)
    require(source_hashes=={k:sha256(p) for k,p in inputs.items()},'source changed during execution')
    provenance={'schema_version':1,'generated_at':datetime.now(timezone.utc).isoformat(),
                'sources':[{'id':k,'filename':p.name,'sha256':source_hashes[k]} for k,p in inputs.items()],
                'official_source':'https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024',
                'use_note':'https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf',
                'code_sha256':code_hashes,
                'outputs_sha256':{name:sha256(args.out/name) for name in ['estimates.csv','estimates.parquet','estimates.json','audit.json']},
                'runtime':{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,
                           'R':subprocess.run(['Rscript','--version'],capture_output=True,text=True,check=True).stdout.strip()},
                'unit':'household','raw_data_exported':False,'sources_unchanged_after_run':True,
                'limitations':['Not a dwelling or site count','Not a fiscal-gap adjustment','Communes nonrepresentative and exploratory','Normal approximation; no singleton correction','No global optimality claim']}
    write('provenance.json',provenance)
    print(json.dumps({'status':'ok','n_persons':len(persons),'n_households':len(heads),'n_rows':len(rows),'national':rows[0]},ensure_ascii=False))

if __name__=='__main__': main()

```

## docs/casen-shared-site-method.md
```
# CASEN 2024: hogares con sitio propio compartido

## Estimando y límites

`p_h = Σ expr × I(v9 ∈ {3,4}) / Σ expr × I(v9 ∈ {1,…,11})`, con una observación por hogar: su jefatura (`pco1=1`). El denominador incluye arrendatarios, cesionarios y las demás tenencias válidas; no se restringe a propietarios. Cada región usa la misma definición con dominio regional. El cálculo comunal usa `expc` y se publica únicamente como descripción exploratoria, sin inferencia representativa ni intervalos.

El indicador cuenta **hogares** que declaran sitio propio compartido con otras viviendas. No identifica todos los sitios compartidos: otros regímenes de tenencia pueden coexistir en un sitio. Tampoco identifica viviendas únicas, sitios únicos, roles fiscales, exenciones ni una fracción causal de la brecha entre roles y viviendas.

La [nota oficial de uso, enero de 2026](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf), páginas 1–5, define cobertura, unidades, factores y cruce por persona. Su distinción territorial sustenta `expr` para nacional/regiones y la advertencia comunal. El [portal oficial CASEN 2024](https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-2024) proporciona la base y los libros de códigos; se congelan sus archivos locales por SHA-256 en `provenance.json`. La encuesta tiene dominios de diseño; ello no garantiza automáticamente precisión suficiente de este indicador particular.

## Fuentes, extracción y validación

- R carga el RData original en un entorno aislado y comprueba almacenamiento y clases de las once columnas antes de convertirlas. Acepta vectores integer/double con clases numéricas o labelled admitidas; rechaza factores, texto, integer64 y clases desconocidas. Después retira atributos y convierte a numeric, evitando despacho S3 de coerción. Los datos seleccionados pasan por memoria a Python; ningún archivo derivado contiene personas, hogares ni identificadores.
- La base complementaria se une por `(folio, id_persona)` con cardinalidad uno a uno y cobertura idéntica en ambos sentidos; no hay unión por posición ni multiplicación de filas.
- Todos los hogares deben tener una sola jefatura; cada campo de vivienda, diseño, geografía, `v9` y `v28` debe ser consistente dentro del hogar. Un incumplimiento aborta la exportación.
- Se exigen pesos de jefatura `expr` y `expc` positivos y finitos, territorios/diseño no faltantes y conservación de todos los pares `(varstrat,varunit)` al pasar de personas a jefaturas.
- El libro de códigos, hoja `V`, contiene `v9=1,…,11`; positivos 3 y 4. `NA` se trata como falta de respuesta; cualquier código no documentado, incluidos sentinelas trasladados desde otra pregunta, aborta. Los códigos no se recodifican a cero.
- `v28=1/2` es una pregunta condicionada. No se usa como filtro general. En el diagnóstico de vivienda se toma el hogar único; en viviendas multihogar se exige un principal único. La selección es un diagnóstico muestral no ponderado, nunca un peso oficial de vivienda.
- `n_flagged=0` es un centinela tautológico de exportación exitosa: las inconsistencias excluyentes abortan antes de exportar. Ese cero no constituye una medición independiente ni evidencia positiva de calidad. La evidencia de los controles reside en las comprobaciones ejecutadas y sus casos de rechazo; `n_missing` se refiere exclusivamente a `v9` ausente.

## Incertidumbre de diseño

Para dominio `d`, total ponderado válido `T_d` y razón `p`, la contribución de cada hogar es `e_j = w_j I(j ∈ d) (y_j-p)/T_d`. Se agregan estas contribuciones por PSU anidada en estrato. La varianza es `Σ_h [m_h/(m_h−1)] Σ_i (e_hi−media_h)^2`.

Se conservan **todas las PSU del diseño**, incluyendo las exteriores al dominio y las que solo contienen respuestas no válidas, con contribución cero. `n_psu`, `n_strata` y `design_df` describen ese diseño completo, no el número de PSU efectivamente observado en una comuna. Para comunas sin muestra los tres se declaran cero y `ci_status=no_sample`.

La aproximación usa reposición a nivel de conglomerado y no aplica corrección de población finita, por faltar los tamaños por etapa. `IC95 = clip(p ± 1.959963985 SE, 0, 1)` es un intervalo normal aproximado, no un intervalo exacto. Cualquier estrato con una sola PSU invalida SE e IC (`not_estimable_singleton`), incluso fuera del dominio: no se inventa una política oficial para singleton. Razones en 0/1 o varianza degenerada producen `not_conclusive_boundary_or_degenerate` con SE/IC nulos, nunca una falsa certeza exacta. Dominio vacío produce estimación nula. Todas las comunas muestreadas tienen `descriptive_nonrepresentative_no_ci`.

La referencia Julia `_taylor_prop_se` se lee sin modificarla. La paridad se limita a fixtures con al menos dos PSU por estrato porque esa función omite singleton, mientras este pipeline los declara no estimables. Coincidencia entre implementaciones es una comprobación de consistencia; la prueba independiente es el oráculo algebraico manual: pesos `(1,2,1,2)`, dos estratos con dos PSU, `p=1/3`, `V=8/81`; otro dominio con dos de tres PSU exige `V=3/16`, que cambia incorrectamente a `1/4` si se elimina la PSU externa.

## Robustez, cobertura y selección

`audit.json:sensitivity` entrega por territorio composición urbano/rural, tasas dentro de cada área, ponderación utilizada y cotas al reponer toda falta de respuesta como negativa o positiva. Son descripciones de composición, no un efecto causal urbano/rural. Si `Y` es el total positivo, `M` el peso faltante y `T` el total de hogares, las cotas son `Y/T` y `(Y+M)/T`. Si no hay faltantes ambas coinciden con la estimación de casos completos; esto no prueba ausencia de sesgos de medición o no respuesta de encuesta.

El universo comunal procede de `V1_Viviendas-y-hogares-censados.xlsx`, Censo 2024, hoja 2. El cruce observado tiene 346 comunas: 335 muestreadas y 11 sin muestra; se incluyen todas por CUT, sin ranking. Las comunas fuera de la muestra CASEN tienen `estimate=null`, `ci_status=no_sample` y conteos muestrales cero; no se imputan tasas cero. `audit.json:commune_coverage` contiene el cruce y los nombres/CUT ausentes. Valparaíso y Viña del Mar fueron seleccionadas después de exploración previa; sus resultados no son contrastes confirmatorios.

## Resultado observado de esta ejecución

| Comprobación | Observación |
|---|---|
| Personas / hogares / viviendas muestrales | 218.367 / 78.654 / 77.618 |
| Positivos `v9=3/4` entre jefaturas | 787 hogares, sin faltantes `v9` |
| Total nacional expandido de hogares válidos | 7.143.171 con `expr` |
| `p_h` nacional | 1,0878222 %; SE 0,0600480 puntos porcentuales |
| IC normal aproximado nacional | 0,9701303–1,2055141 % |
| Diseño completo | 12.512 PSU, 756 estratos, 11.756 grados de libertad |
| Diagnóstico de vivienda | 76.712 viviendas unihogar y 906 multihogar; las 906 tienen principal único |
| Filtro general `v28` | Rechazado: 76.252 jefaturas tienen `v28` faltante |

Como contraste descriptivo, la composición nacional expandida es 88,4510 % urbana y 11,5490 % rural; las respectivas tasas son 1,0668 % y 1,2491 %. Valparaíso tiene 98,5093 % de peso urbano y Viña del Mar 100 %; sus tasas comunales descriptivas son 9,2681 % y 8,5995 %. No hay observaciones rurales en Viña del Mar: la tasa rural es nula en el sentido de dato ausente (`null`), no una tasa cero.

Estas cifras pertenecen a la ejecución y fuentes cuyos hashes figuran en los recibos; no son un oráculo fijado para futuras versiones.

## Anexo algebraico sin aplicación fiscal

Definir `R1 = roles/viviendas` y `p_v` como una proporción **hipotética de viviendas** que están en sitios con exactamente dos viviendas, suponiendo que todos los otros sitios contienen una vivienda. Entonces `sitios = viviendas × (1 − p_v/2)` y `R2(p_v) = roles/sitios = R1/(1 − p_v/2)`. La fórmula cambia si cambia la definición del parámetro o la multiplicidad. **No sustituir `p_v` por `p_h`**, ni usar esta identidad para ajustar la brecha fiscal: no se dispone del enlace representativo vivienda–sitio–rol que permitiría hacerlo.

## Reproducción y aceptación

Desde la raíz del repositorio analítico, definir argumentos con rutas locales autorizadas; las rutas privadas no forman parte de los artefactos públicos:

```sh
/opt/entornos/mamba312/bin/python v5_brecha/scripts/casen_shared_site.py \
  --rdata "$CASEN_RDATA" --communes "$CASEN_COMMUNES" \
  --codebook "$CASEN_CODEBOOK" --communal-codebook "$CASEN_COMMUNAL_CODEBOOK" \
  --use-note "$CASEN_USE_NOTE" --commune-universe "$CENSUS_COMMUNES"
/opt/entornos/mamba312/bin/python -m unittest discover \
  -s v5_brecha/tests -p test_casen_shared_site.py -v
/opt/entornos/mamba312/bin/python v5_brecha/artifacts/casen_shared_site/evidence/reproduce_checks.py \
  --julia-reference "$JULIA_TAYLOR_SOURCE" --julia-project "$JULIA_REFERENCE_PROJECT"
```

No se ejecuta `prepare_sources`, no se instala software y no se escribe en las fuentes externas. `evidence/verification.json` registra suites, hashes y paridad Julia. Seis mutaciones aisladas deben salir no cero: desactivar la guarda numérica de R, quitar PSU exteriores, limitar indebidamente la tenencia del denominador, fabricar IC exacto de borde, contar personas como hogares y omitir singleton. La recuperación usa el código original cuyo hash se conserva. Los fixtures negativos de unión, pesos y claves deben rechazar la entrada. Los artefactos CSV/Parquet/JSON se comparan entre sí y con la partición regional ponderada.

`provenance.json` liga fuentes, código y salidas; el pipeline verifica que los hashes de código capturados al inicio siguen iguales antes de exportar; `evidence/pipeline-receipt.json` liga ejecución y aceptación. Un hash distinto, una falla científica, falta de muestra convertida a cero, o datos privados en la exportación bloquea D1 y exige regenerar/revisar. Un test verde no demuestra causalidad, representatividad comunal ni optimalidad global.

Rollback: retirar únicamente los archivos propios de este módulo y sus agregados tras revisar el diff; conservar evidencia y trabajo ajeno. No modificar las fuentes, el pipeline fiscal anterior ni las proyecciones del blog. No se realiza commit ni publicación desde D1.


## Disposición de revisión D2

- **F1, P1:** observado con un RData sintético real: el reader anterior salía 0 y convertía el factor `v9="2"` a código 4. El defecto se reprodujo antes de corregir; `evidence/D2-F1-red-factor.json` conserva el contraejemplo y el reader anterior permanece en el histórico.
- **F1, estado de la fuente original:** inspección exclusiva de clases y dimensiones observó 11 columnas de almacenamiento double: cinco `haven_labelled/vctrs_vctr/double` y seis `numeric`. No había factor ni integer64. Esto descarta remapeo por factor en ese archivo concreto; no garantiza otras versiones de fuente.
- **F1, corrección:** `src/casen_shared_site/rdata.py` centraliza el reader usado por main y pruebas. Siete pruebas mediante Rscript y RData sintéticos cubren numeric, integer, labelled numérico, factor, carácter, integer64 y salida exclusiva de metadata. Una mutación que desactiva la guarda debe producir fallo observado antes de recuperar verde.
- **F1, fallo adicional de prueba:** la primera ejecución detectó que pandas omitía una fila completamente vacía en el fixture de una sola columna numeric con NA. Se corrigió con `skip_blank_lines=False`; el fallo se conserva en `evidence/D2-F1-r-tests-initial-failure.log` y la recuperación de las siete pruebas en `evidence/D2-F1-r-tests-green.log`.
- **F1, privacidad de metadata:** el guard anterior confundió los nombres `folio`/`id_persona` del esquema con valores de personas. Se conserva ese falso positivo en `evidence/D2-F1-privacy-false-positive.log`; ahora sólo se admite la estructura exacta de clases/almacenamiento y dos fixtures rechazan identificadores fuera de ella o valores ocultos dentro de metadata.
- **F2:** la política de cualquier singleton ⇒ SE/IC no estimable se conserva deliberadamente como restricción conservadora; no se adopta una corrección oficial inexistente.
- **F3:** se explicita que `n_flagged=0` no es prueba positiva independiente de calidad. Los recibos y pruebas de rechazo son la evidencia pertinente.
- **Trazabilidad:** el freeze anterior `e40cae6a5f77becf9634b51c1e4b75be3ea21bc1f2cfd56d5dd487c61d5b791f`, sus archivos, recibos y logs fueron preservados bajo `evidence/history/pre-d2-f1-e40cae6a5f77/`. `evidence/D2-F1-disposition.json` registra el vínculo del candidato y la comparación de agregados; el digest vigente está en [`evidence/freeze.json:source_digest`](../artifacts/casen_shared_site/evidence/freeze.json) y comprende este método, sin incrustarlo autorreferencialmente; la revisión enfocada D2 sigue siendo necesaria.

```

## artifacts/casen_shared_site/evidence/D2-F1-disposition.json
```
{
  "finding": "D2-F1",
  "status": "implemented_and_locally_verified_pending_focused_D2_review",
  "previous_digest": "e40cae6a5f77becf9634b51c1e4b75be3ea21bc1f2cfd56d5dd487c61d5b791f",
  "candidate_freeze": "evidence/freeze.json",
  "candidate_digest_field": "source_digest",
  "legacy_counterexample": "Actual R subprocess synthetic factor code 2 -> 4; legacy binary exit 0, independent oracle exit 1.",
  "current_source_state": "Class/shape inspection only: 11 double columns (5 haven-labelled, 6 numeric), no factor/integer64; remapping not active in inspected source.",
  "fix": "Shared RData reader validates storage/class before stripping attributes/coercion; rejects factors/non-numeric/integer64/unknown classes. Main and actual R subprocess tests use this reader.",
  "additional_observed_failures": {
    "blank_numeric_NA_row": "Fixed pandas skip_blank_lines=False; initial failure retained.",
    "privacy_false_positive": "Column names mistaken for identifier values; exact metadata schema plus two negative injection fixtures now distinguish them."
  },
  "F2": "Conservative global singleton policy retained intentionally",
  "F3": "n_flagged=0 explicitly documented as successful-export sentinel, not independent positive QA",
  "test_count": 31,
  "actual_R_boundary_tests": 7,
  "observed_semantic_mutations": 6,
  "julia_fixtures": 3,
  "aggregate_comparison": {
    "estimates.json": {
      "before_sha256": "b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce",
      "after_sha256": "b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce",
      "byte_identical": true
    },
    "estimates.csv": {
      "before_sha256": "c6c7e9ca08f0b12325ed3f8144df00dd27e6906b7e1ecad4f3ba7b8b8b41e1e3",
      "after_sha256": "c6c7e9ca08f0b12325ed3f8144df00dd27e6906b7e1ecad4f3ba7b8b8b41e1e3",
      "byte_identical": true
    },
    "estimates.parquet": {
      "before_sha256": "5802ad1a03c929ad68b617849c842e65c119add571be5c7e82da8cc549479b02",
      "after_sha256": "5802ad1a03c929ad68b617849c842e65c119add571be5c7e82da8cc549479b02",
      "byte_identical": true
    }
  },
  "metadata_evidence": "evidence/D2-F1-real-column-metadata.json",
  "boundary_replay": "evidence/D2-F1-boundary-replay.json",
  "history": "evidence/history/pre-d2-f1-e40cae6a5f77",
  "privacy": "No original observation rows exported; public evidence contains metadata, aggregates or explicitly synthetic fixtures."
}

```

## artifacts/casen_shared_site/evidence/verification.json
```
{
  "task_id": "D1",
  "status": "verified_local_checks",
  "tests": [
    {
      "name": "tests-green",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 0,
      "log": "tests-green.log",
      "sha256": "824cb42e248a593343d4c2d0274ffc6a769c20931a46d7c0ca1f65095647543a"
    },
    {
      "name": "red-drop-outside-domain-psu",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 1,
      "log": "red-drop-outside-domain-psu.log",
      "sha256": "b745416258c2a495b3e0ab30eabc26200924dc8887317ff4ae108670394aa0c9"
    },
    {
      "name": "red-wrong-ownership-denominator",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 1,
      "log": "red-wrong-ownership-denominator.log",
      "sha256": "586a5b9a20fb14a701f8904bd7836b84ed971ec7c10955b520a95ba2c64644f7"
    },
    {
      "name": "red-false-exact-boundary-ci",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 1,
      "log": "red-false-exact-boundary-ci.log",
      "sha256": "e50b626fbdb1a52c812aa856abb129caa7bd549f7a50993f6f36c16d29366047"
    },
    {
      "name": "red-households-counted-as-persons",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 1,
      "log": "red-households-counted-as-persons.log",
      "sha256": "f71bdf1ba1d5c3efd0ca50c15c9ea09ae6ebc0d3a46051def18d8a376e7be81e"
    },
    {
      "name": "red-singleton-silently-skipped",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 1,
      "log": "red-singleton-silently-skipped.log",
      "sha256": "8381956357d7b6b41d0d46c5b2fd6ad06d2312570bff479f1c6ca5964bc0ed77"
    },
    {
      "name": "red-r-numeric-type-guard",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 1,
      "log": "red-r-numeric-type-guard.log",
      "sha256": "39e21b38a6cb36795f42629f412e84cf93c9a047f1cc0f0791c375fe34462831"
    },
    {
      "name": "tests-green-recovery",
      "command": "python -m unittest discover -s v5_brecha/tests -p test_casen_shared_site.py -v",
      "exit_code": 0,
      "log": "tests-green-recovery.log",
      "sha256": "fed30d0c06ae903aae2b0e31eb672806a76accd7bce8e4cdc39662f224e4583a"
    }
  ],
  "mutants": "Synthetic code copies; each substitution applied once; originals unchanged",
  "code_sha256": {
    "src/casen_shared_site/core.py": "ecd7139d63849d3969785ed22980e166b19b59e0cf78cd99a454a3385f9215a5",
    "src/casen_shared_site/__init__.py": "5fd5525ded8ec6dd2e20997fdcdc61a9b76b7b415ee635ca043541aaf206fc2d",
    "src/casen_shared_site/rdata.py": "3ceea3d56f27b5f066f0541a606d783ee1d06bcfad6b66f9d9798f8f5ccee9b7"
  },
  "test_sha256": "6fb6b1159a01efe2ef0352204c8a71fd1a4a9c3094c88fe41ffd4f8807217f92",
  "harness_sha256": "e3d54e98af9c1143550ae6500ddb9061f97fe56cf96c709d65974427683bf416",
  "julia": {
    "exit_code": 0,
    "version": "julia version 1.10.12",
    "reference_filename": "07b_complex_survey_ci.jl",
    "reference_sha256": "d0a2b89a3cf50ca440c908ed2027c87f6a976ebd4b4ce5fa7d86470a021ae94b",
    "project_sha256": {
      "Project.toml": "66faecd6009a1098604002a1f4fa0285d9a362e420bf03b5d1005762c3831088",
      "Manifest.toml": "3c116302af0fdd87c61ab6f848e2acddda47ed14afe28c4020c065ef45bdd14c"
    },
    "project_unchanged": true,
    "log_sha256": "9457aeb7f313bfaf48cc9589c2076441796bcd719d774308fd898aed18dbfbcb",
    "comparisons": [
      {
        "fixture": [
          [
            1.0,
            2.0,
            1.0,
            2.0
          ],
          [
            1,
            1,
            2,
            2
          ],
          [
            1,
            2,
            3,
            4
          ],
          [
            1,
            1,
            1,
            1
          ],
          [
            1,
            0,
            1,
            0
          ]
        ],
        "python": [
          0.3333333333333333,
          0.31426968052735443,
          0,
          0.9492905887444039,
          4,
          2
        ],
        "julia": [
          0.3333333333333333,
          0.31426968052735443,
          0.0,
          0.9492905887444039,
          4.0,
          2.0
        ],
        "max_abs_error": 0.0
      },
      {
        "fixture": [
          [
            1.0,
            1.0,
            1.0
          ],
          [
            1,
            1,
            1
          ],
          [
            1,
            2,
            3
          ],
          [
            1,
            1,
            0
          ],
          [
            1,
            0,
            0
          ]
        ],
        "python": [
          0.5,
          0.4330127018922193,
          0,
          1,
          3,
          1
        ],
        "julia": [
          0.5,
          0.4330127018922193,
          0.0,
          1.0,
          3.0,
          1.0
        ],
        "max_abs_error": 0.0
      },
      {
        "fixture": [
          [
            2.0,
            3.0,
            5.0,
            7.0,
            11.0,
            13.0
          ],
          [
            1,
            1,
            1,
            2,
            2,
            2
          ],
          [
            1,
            1,
            2,
            1,
            2,
            3
          ],
          [
            1,
            1,
            1,
            0,
            1,
            1
          ],
          [
            1,
            0,
            1,
            1,
            0,
            1
          ]
        ],
        "python": [
          0.5882352941176471,
          0.31425086615204784,
          0,
          1,
          5,
          2
        ],
        "julia": [
          0.5882352941176471,
          0.31425086615204784,
          0.0,
          1.0,
          5.0,
          2.0
        ],
        "max_abs_error": 0.0
      }
    ],
    "limitation": "Parity is consistency, not independence; manual variance oracles are independent. Singleton policy intentionally differs from reference."
  }
}

```

## Current test suite
```python
"""Independent manual oracles and negative controls, no raw-data dependency."""
from pathlib import Path
import importlib.util
import math
import copy
import json
import hashlib
import os
import subprocess
import sys
import unittest
import tempfile
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,os.environ.get('CASEN_TEST_SRC',str(ROOT/'src')))
from casen_shared_site.core import prepare_households,taylor_ratio,estimates
from casen_shared_site.rdata import FIELDS, read_rdata_numeric, inspect_rdata_columns


def validate_public_structure(value, path=()):
    """Allow identifier COLUMN NAMES only in audited class metadata, never values."""
    if path==('r_extraction','columns'):
        if not isinstance(value,dict) or not set(value).issubset(FIELDS):
            raise ValueError('invalid column metadata')
        classes={'numeric','integer','double','haven_labelled','haven_labelled_spss','vctrs_vctr','labelled'}
        for field,meta in value.items():
            if not isinstance(meta,dict) or set(meta)!={'storage_type','classes'}:
                raise ValueError('column metadata may not contain observation values')
            if meta['storage_type'] not in {'double','integer'} or not isinstance(meta['classes'],list) or not meta['classes'] or any(not isinstance(c,str) or c not in classes for c in meta['classes']):
                raise ValueError('invalid column class metadata')
        return
    if isinstance(value,dict):
        if set(value)&{'folio','id_persona','id_vivienda'}:
            raise ValueError('identifier field outside class metadata')
        for key,item in value.items():validate_public_structure(item,path+(key,))
    elif isinstance(value,list):
        for item in value:validate_public_structure(item,path+('item',))


def fixture():
    # Four households, one non-head. v28 absent for both singleton dwellings.
    rows=[(1,1,10,1,3,np.nan,1,1,1,5,1),
          (1,2,10,4,3,np.nan,1,1,1,5,1),
          (2,1,20,1,5,np.nan,2,1,2,5,2),
          (3,1,30,1,4,1,1,2,3,13,1),
          (4,1,30,1,8,2,2,2,4,13,1)]
    p=pd.DataFrame(rows,columns=['folio','id_persona','id_vivienda','pco1','v9','v28','expr','varstrat','varunit','region','area'])
    c=p[['folio','id_persona']].copy();c['expc']=[2,2,4,2,4];c['comuna']=[5101,5101,5101,13101,13101]
    return p,c


class RDataBoundary(unittest.TestCase):
    """Integration through actual installed Rscript, synthetic RData only."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='casen-r-boundary-fixture-')
        self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'synthetic.RData'

    def save(self,expression):
        code='args<-commandArgs(TRUE); value<-'+expression+';casen<-data.frame(row.names=seq_along(value));casen$v9<-value;save(casen,file=args[1])'
        result=subprocess.run(['Rscript','--vanilla','-e',code,str(self.path)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_numeric_codes_preserved_by_actual_r_subprocess(self):
        self.save('c(1,10,11,2,3,4,NA_real_)')
        data,metadata=read_rdata_numeric(self.path,fields=['v9'])
        self.assertEqual(data.v9.iloc[:6].tolist(),[1,10,11,2,3,4])
        self.assertTrue(pd.isna(data.v9.iloc[6]))
        self.assertEqual(metadata['columns']['v9']['storage_type'],'double')
        self.assertEqual(metadata['r_exit_code'],0)

    def test_integer_codes_preserved_by_actual_r_subprocess(self):
        self.save('as.integer(c(1,10,11,2,3,4))')
        data,metadata=read_rdata_numeric(self.path,fields=['v9'])
        self.assertEqual(data.v9.tolist(),[1,10,11,2,3,4])
        self.assertEqual(metadata['columns']['v9']['storage_type'],'integer')

    def test_haven_labelled_numeric_storage_preserved(self):
        # Class attributes follow haven's numeric representation; no new package needed.
        self.save('structure(c(1,10,11,2,3,4),labels=c(owned=1,shared=3),class=c("haven_labelled","vctrs_vctr","double"))')
        data,metadata=read_rdata_numeric(self.path,fields=['v9'])
        self.assertEqual(data.v9.tolist(),[1,10,11,2,3,4])
        self.assertIn('haven_labelled',metadata['columns']['v9']['classes'])

    def test_factor_codes_fail_closed_before_level_index_conversion(self):
        self.save('factor(c("1","10","11","2","3","4"),levels=c("1","10","11","2","3","4"))')
        with self.assertRaisesRegex(ValueError,'unsupported R column types: v9'):
            read_rdata_numeric(self.path,fields=['v9'])

    def test_character_codes_fail_closed_before_numeric_coercion(self):
        self.save('c("1","10","11","2","3","4")')
        with self.assertRaisesRegex(ValueError,'unsupported R column types: v9'):
            read_rdata_numeric(self.path,fields=['v9'])

    def test_integer64_class_rejected_before_silent_precision_change(self):
        self.save('structure(c(1,2,3),class="integer64")')
        with self.assertRaisesRegex(ValueError,'unsupported R column types: v9'):
            read_rdata_numeric(self.path,fields=['v9'])

    def test_metadata_inspection_emits_no_observations(self):
        self.save('c(1,10,11,2)')
        metadata=inspect_rdata_columns(self.path,fields=['v9'])
        self.assertEqual(metadata['n_rows'],4)
        self.assertEqual(set(metadata['columns']),{'v9'})
        self.assertNotIn('values',metadata)


class HouseholdContract(unittest.TestCase):
    def test_household_not_person_or_owner_denominator(self):
        h,a=prepare_households(*fixture())
        self.assertEqual((a['n_persons'],len(h),a['n_dwellings']),(5,4,3))
        self.assertAlmostEqual(h.loc[h.shared,'expr'].sum()/h.expr.sum(),1/3)
        self.assertEqual(h.valid_v9.sum(),4) # rental and ceded included
        self.assertEqual(a['dwelling_diagnostic']['selected_representatives'],3)
        self.assertEqual(a['dwelling_diagnostic']['multiple_with_unique_principal'],1)
        self.assertEqual(a['dwelling_diagnostic']['selected_shared_v9'],2)

    def test_duplicate_head_rejected(self):
        p,c=fixture();p.loc[1,'pco1']=1
        with self.assertRaisesRegex(ValueError,'exactly one'): prepare_households(p,c)

    def test_missing_head_rejected(self):
        p,c=fixture();p.loc[0,'pco1']=2
        with self.assertRaisesRegex(ValueError,'exactly one'): prepare_households(p,c)

    def test_incomplete_join_rejected(self):
        p,c=fixture()
        with self.assertRaisesRegex(ValueError,'identical person'): prepare_households(p,c.iloc[:-1])

    def test_duplicate_join_key_rejected(self):
        p,c=fixture()
        with self.assertRaisesRegex(ValueError,'duplicate person'): prepare_households(p,pd.concat([c,c.iloc[:1]]))

    def test_nonpositive_weight_rejected(self):
        p,c=fixture();p.loc[0,'expr']=0
        with self.assertRaisesRegex(ValueError,'invalid expr'): prepare_households(p,c)

    def test_inconsistent_household_rejected(self):
        p,c=fixture();p.loc[1,'v9']=4
        with self.assertRaisesRegex(ValueError,'inconsistent household'): prepare_households(p,c)

    def test_unknown_code_rejected(self):
        for code in [12,-88,-99]:
            p,c=fixture();p.loc[2,'v9']=code
            with self.assertRaisesRegex(ValueError,'undocumented v9'): prepare_households(p,c)

    def test_missing_is_not_negative_and_bounds(self):
        p,c=fixture();p.loc[2,'v9']=np.nan
        h,a=prepare_households(p,c)
        rows,s=estimates(h,{i:str(i) for i in range(1,17)},{5101:'Valparaíso',13101:'Santiago'})
        self.assertEqual(a['n_missing_v9'],1)
        self.assertEqual(rows[0]['n_valid'],3)
        self.assertAlmostEqual(rows[0]['estimate'],.5)
        self.assertAlmostEqual(s[0]['missing_all_negative'],1/3)
        self.assertAlmostEqual(s[0]['missing_all_positive'],2/3)
        self.assertEqual(s[0]['area']['rural']['estimate'],None)
        self.assertAlmostEqual(s[0]['area']['urban']['weighted_household_share'],2/3)

    def test_multihousehold_ambiguous_principal_diagnostic_only(self):
        p,c=fixture();p.loc[4,'v28']=1
        h,a=prepare_households(p,c)
        self.assertEqual(len(h),4)
        self.assertEqual(a['dwelling_diagnostic']['multiple_without_unique_principal'],1)
        self.assertEqual(a['dwelling_diagnostic']['selected_representatives'],2)

    def test_communal_no_ci_no_ranking(self):
        h,_=prepare_households(*fixture())
        rows,_=estimates(h,{i:str(i) for i in range(1,17)},{5101:'Valparaíso',13101:'Santiago'})
        communes=[r for r in rows if r['scope']=='commune']
        self.assertEqual([r['territory_code'] for r in communes],['5101','13101'])
        for r in communes:
            self.assertEqual(r['weight'],'expc')
            self.assertEqual(r['ci_status'],'descriptive_nonrepresentative_no_ci')
            self.assertIsNone(r['ci_low']); self.assertIsNone(r['se'])

    def test_absent_commune_is_null_not_zero(self):
        h,_=prepare_households(*fixture())
        rows,s=estimates(h,{i:str(i) for i in range(1,17)},{5101:'Valparaíso',13101:'Santiago',2202:'Ollagüe'})
        row=next(r for r in rows if r['territory_code']=='2202')
        self.assertEqual(row['ci_status'],'no_sample')
        self.assertIsNone(row['estimate']);self.assertIsNone(row['ci_low'])
        self.assertEqual((row['n_households'],row['n_psu']),(0,0))


class TaylorContract(unittest.TestCase):
    def test_manual_two_strata_oracle(self):
        # w=(1,2,1,2), y=(1,0,1,0), T=6, p=1/3.
        # e=(1/9,-1/9,1/9,-1/9), variance=2*(2*2/81)=8/81.
        r=taylor_ratio([1,2,1,2],[1,1,2,2],[1,2,3,4],[1]*4,[1,0,1,0])
        self.assertAlmostEqual(r['estimate'],1/3)
        self.assertAlmostEqual(r['se'],math.sqrt(8/81))
        self.assertEqual((r['n_psu'],r['n_strata'],r['design_df']),(4,2,2))
        self.assertEqual(r['ci_low'],0)

    def test_manual_outside_domain_psu_oracle(self):
        # One stratum, 3 PSU: domain={first,second}; e=(1/4,-1/4,0).
        # Variance=3/2*(1/16+1/16)=3/16, versus wrong 1/4 when filtered.
        r=taylor_ratio([1,1,1],[1]*3,[1,2,3],[1,1,0],[1,0,0])
        self.assertAlmostEqual(r['se'],math.sqrt(3)/4)
        self.assertEqual(r['n_psu'],3)
        self.assertNotAlmostEqual(r['se'],.5)

    def test_singleton_inside_and_outside_domain_null(self):
        for d in ([1,1,1],[1,1,0]):
            r=taylor_ratio([1]*3,[1,1,2],[1,2,3],d,[1,0,0])
            self.assertEqual(r['ci_status'],'not_estimable_singleton')
            self.assertEqual((r['n_psu'],r['n_strata'],r['design_df']),(3,2,1))
            self.assertIsNone(r['se']);self.assertIsNone(r['ci_low'])

    def test_boundary_and_degenerate_no_false_exact_ci(self):
        for y in ([0,0],[1,1]):
            r=taylor_ratio([1,1],[1,1],[1,2],[1,1],y)
            self.assertEqual(r['ci_status'],'not_conclusive_boundary_or_degenerate')
            self.assertIsNone(r['ci_low'])
        r=taylor_ratio([1]*4,[1]*4,[1,1,2,2],[1]*4,[1,0,1,0])
        self.assertEqual(r['ci_status'],'not_conclusive_boundary_or_degenerate')

    def test_empty_domain_not_zero(self):
        r=taylor_ratio([1,1],[1,1],[1,2],[0,0],[1,0])
        self.assertIsNone(r['estimate']);self.assertIsNone(r['ci_low'])

    def test_psu_nested_by_stratum(self):
        r=taylor_ratio([1,2,1,2],[1,1,2,2],[1,2,1,2],[1]*4,[1,0,1,0])
        self.assertEqual(r['n_psu'],4)
        self.assertAlmostEqual(r['se'],math.sqrt(8/81))

    def test_invalid_weights_rejected(self):
        for w in ([0,1],[np.nan,1],[-1,1]):
            with self.assertRaisesRegex(ValueError,'invalid Taylor weights'):
                taylor_ratio(w,[1,1],[1,2],[1,1],[1,0])


class AggregateArtifacts(unittest.TestCase):
    def setUp(self):
        self.path=ROOT/'artifacts/casen_shared_site'
        self.rows=json.loads((self.path/'estimates.json').read_text())['rows']
        self.audit=json.loads((self.path/'audit.json').read_text())

    def test_formats_and_hashes_match(self):
        csv=pd.read_csv(self.path/'estimates.csv',dtype={'territory_code':str})
        pq=pd.read_parquet(self.path/'estimates.parquet')
        js=pd.DataFrame(self.rows)
        pd.testing.assert_frame_equal(csv,pq,check_dtype=False,atol=1e-13,rtol=1e-13)
        pd.testing.assert_frame_equal(js,pq,check_dtype=False,atol=1e-13,rtol=1e-13)
        prov=json.loads((self.path/'provenance.json').read_text())
        for name,expected in prov['outputs_sha256'].items():
            self.assertEqual(hashlib.sha256((self.path/name).read_bytes()).hexdigest(),expected,name)
        for name,expected in prov['code_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),expected,name)

    def test_coverage_partition_and_weighted_identity(self):
        national=self.rows[0];regions=[r for r in self.rows if r['scope']=='region']
        communes=[r for r in self.rows if r['scope']=='commune']
        self.assertEqual({r['territory_code'] for r in regions},{str(i) for i in range(1,17)})
        self.assertEqual(sum(r['n_households'] for r in regions),self.audit['n_households'])
        self.assertEqual(sum(r['n_households'] for r in communes),self.audit['n_households'])
        self.assertAlmostEqual(sum(r['weighted_denominator'] for r in regions),national['weighted_denominator'])
        self.assertAlmostEqual(sum(r['weighted_denominator']*r['estimate'] for r in regions)/national['weighted_denominator'],national['estimate'])
        coverage=self.audit['commune_coverage']
        self.assertEqual(len(communes),coverage['universe_n'])
        self.assertEqual(sum(r['ci_status']=='no_sample' for r in communes),coverage['no_sample_n'])
        self.assertEqual(coverage['universe_n'],coverage['sampled_n']+coverage['no_sample_n'])
        for r in communes:
            self.assertIsNone(r['se']);self.assertIsNone(r['ci_low']);self.assertIsNone(r['ci_high'])
            if not r['n_households']: self.assertIsNone(r['estimate'])

    def test_schema_privacy_and_no_fiscal_plug_in(self):
        expected={'scope','territory_code','territory_name','unit','denominator_definition','weight',
                  'n_households','n_valid','n_missing','n_flagged','weighted_denominator','estimate',
                  'se','ci_low','ci_high','ci_status','n_psu','n_strata','design_df','selection_note'}
        for r in self.rows:
            self.assertEqual(set(r),expected)
            self.assertEqual(r['unit'],'household')
            self.assertEqual(r['n_valid']+r['n_missing'],r['n_households'])
            if r['estimate'] is not None:self.assertTrue(0<=r['estimate']<=1)
        self.assertFalse(self.audit['r2']['applied_to_fiscal_gap'])
        self.assertFalse(self.audit['r2']['household_rate_used_as_parameter'])
        for name in ['estimates.json','audit.json','provenance.json']:
            text=(self.path/name).read_text()
            self.assertNotIn('/home/',text)
            validate_public_structure(json.loads(text))

    def test_identifier_values_rejected_but_class_metadata_allowed(self):
        validate_public_structure(self.audit)
        leaked=copy.deepcopy(self.audit);leaked['people']=[{'id_persona':12345}]
        with self.assertRaisesRegex(ValueError,'identifier field'):
            validate_public_structure(leaked)

    def test_class_metadata_cannot_hide_observation_values(self):
        for invalid in ({'storage_type':'double','classes':['numeric'],'values':[12345]},
                        {'storage_type':'double','classes':[12345]}):
            leaked=copy.deepcopy(self.audit)
            leaked['r_extraction']['columns']['folio']=invalid
            with self.assertRaisesRegex(ValueError,'metadata'):
                validate_public_structure(leaked)


if __name__=='__main__': unittest.main()

```