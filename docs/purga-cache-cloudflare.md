# Purgar la caché de Cloudflare por API

## Por qué hace falta

Cloudflare está delante del sitio y guarda su propia copia de cada fichero durante
`max-age`, que aquí son 14 400 s (4 h). Mientras esa copia viva, todo visitante recibe
esos bytes aunque GitLab Pages ya sirva otros. Medido el 2026-09-08: tras actualizar
`bar.png` y `popup-hidpi.png`, el borde seguía entregando los de julio (14 664 B y
133 272 B) mientras el origen ya daba los nuevos (38 354 B y 251 052 B).

Un fichero con **nombre nuevo** no sufre esto: Cloudflare no tenía copia. El problema
es solo sobrescribir conservando el nombre, que es lo que hacen las piezas marcadas
`nombre_legacy` en `_data/visuales/`. Esa marca compra estabilidad de URL —tarjetas
sociales y enlaces ya servidos— al precio de una purga en cada actualización.

**`Ctrl+Shift+R` no sirve.** Manda `Cache-Control: no-cache` en la petición y Cloudflare
lo ignora: comprobado, responde `cf-cache-status: HIT` con los bytes viejos. Ese atajo
solo salta la caché del navegador, no la del borde.

## Paso 1 — crear el token (una vez)

En `dash.cloudflare.com` → **My Profile** → **API Tokens** → **Create Token** →
**Create Custom Token**:

| Campo | Valor |
|---|---|
| Nombre | `purga-cache-3cucharadas` |
| Permissions | **Zone** → **Cache Purge** → **Purge** |
| Zone Resources | Include → Specific zone → `3cucharadas.cl` |
| TTL | opcional; ponerle caducidad es buena práctica |

Ese es el permiso **mínimo**: no puede leer DNS, ni contenido, ni tocar configuración.
Si se filtra, lo peor que consigue quien lo tenga es vaciar la caché.

## Paso 2 — el Zone ID

Está en el panel del dominio, columna derecha de **Overview**, como *Zone ID*. No es un
secreto, pero se guarda junto al token por comodidad.

## Paso 3 — guardarlos

```bash
install -d -m 700 ~/.config/3cucharadas
umask 077
cat > ~/.config/3cucharadas/secrets.env   # se pega el contenido y Ctrl-D
CLOUDFLARE_PURGE_TOKEN=...
CLOUDFLARE_ZONE_ID=...
chmod 600 ~/.config/3cucharadas/secrets.env
```

Mismo patrón que `~/.config/ai-quota-monitor/secrets.env`. **El token nunca se escribe
como literal en un comando**: los hooks de memoria y el transcript registran los
comandos, así que se referencia por fichero o variable, nunca por su valor.

## Paso 4 — purgar

```bash
scripts/purge_cloudflare_cache.sh --changed          # lo que modificó el último commit
scripts/purge_cloudflare_cache.sh --changed --dry-run
scripts/purge_cloudflare_cache.sh assets/images/ai-quota-hud/bar.png
```

`--changed` toma los activos con estado **M** del último commit. Los **A** (añadidos) y
los renombrados se omiten a propósito: su URL es nueva y no hay copia vieja que purgar.

## La trampa que el script evita

Purgar **antes** de que el despliegue termine hace que Cloudflare vuelva al origen,
encuentre el fichero viejo y lo cachee otras 4 h. La purga se gasta y el problema
empeora. Por eso el script comprueba primero, con un parámetro aleatorio que evita la
clave de caché, que el origen ya sirve exactamente los bytes del árbol; si no coinciden
se niega y sale 1.

Orden correcto: `git push` → esperar que el pipeline quede en `success` → purgar.

## Qué verifica

Que la API responda `success: true` **no** prueba que el borde esté al día. El script
vuelve a pedir cada URL y compara `content-length` con el tamaño del fichero local, que
es lo que ve un visitante. Sale 1 si alguna sigue vieja.

Casos observados en rojo el 2026-09-08:

| Caso | Resultado |
|---|---|
| Origen desfasado (fichero no desplegado) | `exit=1`, se niega a purgar |
| Origen al día | `exit=0`, lista las URL |
| `--changed` sin activos modificados | `exit=0`, no hace nada |
| `--dry-run` sin credencial | funciona: la credencial se pide solo al purgar de verdad |

## Alternativa sin token

Panel de Cloudflare → dominio → **Caching** → **Configuration** → *Purge Cached Files*,
pegando las URL completas. Surte efecto en segundos. *Development Mode*, en la misma
página, desactiva la caché 3 h para todo el sitio: sirve, pero es más bruto.
