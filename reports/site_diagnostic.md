# Diagnóstico del sitio: Catastro SII Brecha

Fecha: 2026-07-18
Rama de integración: `feature/catastro-sii-mapas`

## Resultado

El visor existente es una aplicación estática incluida dentro del repositorio Jekyll.
Su ruta real es `/catastro_sii_brecha/` (singular), no
`/catastro_sii_brechas/` como usa el handoff. La integración debe conservar primero
esa URL canónica y entregar una redirección compatible desde la ruta plural.

## Estado comprobado antes de editar

| Aspecto | Evidencia | Decisión de integración |
| --- | --- | --- |
| Árbol y rama | Repositorio limpio, rama inicial `main` | Se creó `feature/catastro-sii-mapas`; no había cambios que fotografiar en un commit de snapshot. |
| Página | `catastro_sii_brecha/index.html` | Se preservará como shell y sus textos/IDs. No se moverá a un layout global. |
| Tema | Jekyll 4.4.1, `minimal-mistakes-jekyll` como gem | El visor no depende del layout del tema; por ello no se modificará `_config.yml`, layouts globales ni `main.min.js`. |
| Estilos e interfaz | `style.css`, `assets/site-ui.js`, controles de tema locales | Se conservan sin rediseño. El CSS del mapa se encapsulará bajo `.catastro-maplibre`. |
| Mapa actual | `app.js` pinta celdas agregadas en canvas; MapLibre sólo se intenta si se inyecta una clave MapTiler, hoy vacía | Se reemplaza sólo el motor de mapa por un bundle Vite aislado. Las celdas y fichas siguen disponibles si los tiles no responden. |
| Datos actuales | `data/comunas.json` (346 comunas), Parquet de métricas y JSON de celdas por comuna | Las métricas, textos y selectores actuales siguen siendo el contrato de la UI. |
| Frontend | No existían `package.json`, TypeScript, Vite ni lockfile | Se añadirá un proyecto npm privado y un build Vite dedicado. |
| Despliegue | GitLab Pages construye Jekyll; CI actual inyecta una clave MapTiler en un archivo local | Se añadirá el build de Vite antes de Jekyll. No se dependerá de MapTiler ni de `tile.openstreetmap.org`. |
| Toolchain local | Node 26.4.0, npm 12.0.1, Ruby 3.4.10 | CI fijará Node 24 según el contrato; el lockfile fijará las dependencias del visor. |

## Desviaciones justificadas del handoff

1. El nombre de la página preexistente es singular. Renombrarla rompería enlaces,
   canonical y activos actuales; se conserva y la URL plural será un alias.
2. La página no usa front matter ni un layout Jekyll específico. Vite se conecta
   mediante un cargador local y un `manifest` de build, no mediante una mutación del
   tema ni de layouts globales.
3. La capa predial no puede publicarse aún: `LEGAL_PUBLICATION_STATUS` empieza en
   `PENDING`, por lo que el pipeline aborta cualquier upload vectorial.

## Riesgos que bloquean promoción, no implementación

- `stata01` respondió, pero no contiene el árbol de trabajo propuesto ni los binarios
  `tippecanoe`, `pmtiles`, `ogr2ogr` o `rclone`.
- No existe configuración versionada de Cloudflare R2, CORS ni credenciales en este
  repositorio. Se dejará un comando validado que exige variables de entorno, sin
  registrar secretos.
- Falta aprobación expresa de redistribución vectorial predial. El piloto se puede
  construir y auditar local/remotamente, pero no alojar públicamente mientras el gate
  siga en `PENDING`.
