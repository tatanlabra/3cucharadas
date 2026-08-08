# Contrato de tarea

Capa delgada sobre los verificadores que el repositorio **ya tiene**. No es un
framework: es el mínimo necesario para que la palabra «hecho» tenga un
significado comprobable.

El problema que resuelve: el mismo agente que ejecuta una tarea puede
reinterpretar informalmente cuándo la considera terminada. Un Markdown es
contexto, no una barrera. Aquí el veredicto lo da un exit code.

```
El agente produce CLAIMS.
Los verificadores producen EVIDENCIA.
```

## Uso

```bash
python3 .agent/scripts/verify_contract.py              # todo el contrato
python3 .agent/scripts/verify_contract.py --phase P1   # solo una fase
python3 .agent/scripts/verify_contract.py --only AC-SEO-03
python3 .agent/scripts/verify_contract.py --list       # qué se comprueba
python3 .agent/scripts/verify_contract.py --artifact _site --keep-artifact
```

Exit codes: `0` cumplido · `1` incumplido · `2` contrato inválido.

Por defecto construye el sitio en `_site_check/` y lo borra al terminar. Con
`--artifact` se reutiliza un build existente y no se borra nada.

## Estructura

| Ruta | Qué es |
|---|---|
| `contract.yaml` | Objetivo, invariantes, deliverables y criterios de aceptación por fase |
| `scripts/verify_contract.py` | Ejecuta cada criterio, guarda evidencia, imprime el veredicto |
| `checks/_common.py` | Lectura del artefacto: páginas, canonicals, hreflang, sitemap |
| `checks/canonicals.py` | Canonicals duplicados, autorreferencia, sitemap sin URLs muertas |
| `checks/hreflang.py` | Reciprocidad ES/EN + x-default |
| `checks/markup.py` | Barra de navegación propia, accesibilidad del toggle, soft-404 |
| `checks/styles.py` | CSS compilado: escalera tipográfica, área táctil, fallback sin JS |
| `checks/security.py` | Pipeline, escapado de Liquid, pinning de acciones, dependabot |
| `evidence/` | Salida real de cada criterio. No se versiona: se regenera |

Los comprobadores leen el **artefacto construido**, no las plantillas: lo que
importa es lo que reciben el navegador y Googlebot, no lo que el Liquid pretende
emitir.

## Verificaciones manuales

`manual_acceptance` en el contrato recoge lo que necesita un navegador real y no
puede correr desatendido: comportamiento a 320/375/414 px, ausencia de errores de
consola, la barra antes de que llegue Font Awesome, y el tema oscuro. No bloquean
el exit code, pero se listan en cada ejecución para que no se olviden.

Para ejecutarlas:

```bash
bundle exec jekyll build -d _site
npm run serve:catastro:mcp     # sirve _site en 0.0.0.0:4015
```

Desde el MCP de Playwright, el navegador corre en contenedor: usar
`http://172.17.0.1:4015/`, **no** `localhost`. El puerto 4000 está ocupado por
LiteLLM.

## Política de cambios

| Nivel | Mutabilidad |
|---|---|
| Objetivo e invariantes | Requieren aprobación humana explícita |
| Criterios de aceptación | Modificables con justificación registrada en `changes:` |
| Plan e implementación | Libres |

**Freeze the goal, not the path.** Corregir una premisa equivocada con evidencia
es drift positivo y está permitido: se registra en `changes:`, se justifica y se
vuelven a ejecutar los criterios afectados. Borrar un criterio porque cuesta
cumplirlo no lo es.

## Alcance deliberado

Esto es la Fase 1 MVP del handoff de contratos operativos. **No** implementa
máquina de estados, stop hooks, evaluación de Spec Kit, ADRs ni integración con
Codex: eso requiere su propia Fase 0 de diagnóstico y merece sesión aparte.
