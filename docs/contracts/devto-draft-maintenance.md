# Mantenimiento DEV: sólo borradores existentes

La autorización de saneamiento no permite crear artículos, publicar, despublicar
ni modificar artículos publicados. El trailer `3c-maintenance: drafts-only` del
commit de entrega activa el mismo modo restringido que `--existing-drafts-only`.

Antes de escribir: inventario autenticado, canonical único, ID existente, estado
borrador y cuerpo recuperable. Un inventario vacío o de 1.000 resultados
(paginación potencialmente incompleta) impide continuar. Sin clave o con dry-run
sin API, el resultado es NO_CONCLUYENTE, nunca una validación remota.

La custodia anterior se cifra con AES-256-GCM, salt e IV aleatorios y una clave
derivada mediante PBKDF2-HMAC-SHA256 (250.000 iteraciones) de DEV_TO_API_KEY.
El workflow conserva únicamente `drafts-before.enc.json` en un artifact durante
siete días; nunca guarda cuerpos en claro ni secretos en logs. Descargar ese
artifact a almacenamiento privado al cerrar la ejecución. Conservar la clave
vigente al ejecutar hasta recuperar/exportar cualquier respaldo necesario:
rotarla invalida la recuperación si no se conserva la anterior de forma segura.
`DevtoDraftPolicy.decrypt_snapshot` permite recuperar el JSON con esa clave; no
restaura ni escribe en DEV. La prueba ejecuta round-trip y rechaza clave errónea,
tag alterado y sobrescritura de un respaldo existente.

Cada PUT relee el inventario después de la pausa de rate limit y comprueba
identidad, estado y contenido; un cambio concurrente, respuesta incoherente o
HTTP 429 detiene las escrituras restantes. El registro local conserva los éxitos
anteriores aunque falle un artículo posterior. No se reintenta automáticamente.
Un cuerpo/título ya equivalente no provoca un PUT.

La [API oficial de Forem](https://developers.forem.com/api/v1) no documenta un PUT
condicional con compare-and-swap: queda una ventana entre relectura y escritura.
Esta guarda detecta cambios observables; no ofrece exclusión atómica con un editor
humano. Durante la corrida no editar/publicar simultáneamente los mismos borradores.

Rollback: descifrar en almacenamiento privado, releer el estado actual y restaurar
sólo los IDs que sigan siendo borradores y cuyo cuerpo sea el escrito por esta
corrida; cualquier cambio ajeno exige revisión humana, no sobrescritura automática.
