# Seguridad — índice

Este directorio **no duplica** la documentación de seguridad que ya existía. Los
dos documentos con mediciones reales siguen donde estaban, porque `_headers` los
referencia por ruta y moverlos rompería ese enlace sin ganar nada:

| Documento | Qué contiene | Estado |
|---|---|---|
| [`../cabeceras_seguridad_cloudflare.md`](../cabeceras_seguridad_cloudflare.md) | Diagnóstico de por qué GitLab Pages ignora `_headers` (verificado contra el código de `gitlab-org/gitlab-pages`, issue #50) y registro de la implementación del 19-07-2026 | Histórico + registro |
| [`../runbook_cloudflare_headers.md`](../runbook_cloudflare_headers.md) | Procedimiento operativo en el panel de Cloudflare, con `curl` medidos, rollback y "qué no tocar" | **Vigente** |
| [`threat-model.md`](threat-model.md) | Modelo de amenazas ordenado sobre la infraestructura real, no sobre la supuesta | Vigente |
| [`rollback.md`](rollback.md) | Cómo revertir cada cambio de endurecimiento, uno por uno | Vigente |
| [`../../SECURITY.md`](../../SECURITY.md) | Política pública de reporte | Vigente |
| [`../../_headers`](../../_headers) | La política de cabeceras como fuente única. **Inerte en GitLab Pages**; quien la aplica es Cloudflare | Fuente única, no ejecutable |

## La corrección de premisa que ordena todo lo demás

El plan de seguridad original (`HANDOFF_SEGURIDAD_3CUCHARADAS.md` v1.0) asumía
**GitHub Pages + Cloudflare**. Verificado contra el repositorio:

| Supuesto v1.0 | Realidad |
|---|---|
| Producción en GitHub Pages | **Falso.** GitLab Pages: `.gitlab-ci.yml`, job `pages`, artefacto `public/`. No existe la gema `github-pages` ni un archivo `CNAME` |
| Cloudflare delante | **Cierto**, con tres Response Header Transform Rules activas desde 2026-07-19 |
| GitHub como espejo | **Cierto**: `README.md` y `.github/workflows/github-pages-redirector.yml` |

La consecuencia práctica: **endurecer GitHub Actions no protege producción.** Es
trabajo que vale la pena igual —el espejo es público y un workflow con
`contents: write` puede alterar el repositorio— pero no es lo primero. Lo primero
es el pipeline de GitLab, que es lo único que escribe en el artefacto publicado.

Ver [`threat-model.md`](threat-model.md) para el orden completo.

## Controles automatizados

Cuatro comprobadores fijan las correcciones para que no se pierdan en una edición
futura. No son un escáner general: cada uno ancla un hallazgo concreto.

```bash
python3 .agent/checks/security.py --pipeline          # sin curl|bash en el pipeline
python3 .agent/checks/security.py --liquid-escaping   # datos remotos escapados en atributos
python3 .agent/checks/security.py --actions-pinned    # acciones con escritura pinneadas a SHA
python3 .agent/checks/security.py --dependabot        # dependabot cubre lo que hay
```
