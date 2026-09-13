# QA — cápsula de audio de Nushell

Estado: **pendiente de escucha humana**. Nada de lo que sigue sustituye esa escucha.

## Comprobado por máquina (2026-09-13)

| Comprobación | Resultado | Cómo |
|---|---|---|
| El re-encode conserva la duración | 989,053968 s en máster y publicado | `ffprobe -show_entries format=duration` sobre los dos |
| El publicado es mono AAC | `codec_name=aac`, `channels=1` | `ffprobe -show_entries stream=codec_name,channels` |
| Peso declarado == peso real | 8.253.516 bytes en `audio.bytes` y en disco | `stat -c '%s'` |
| El archivo está declarado en el contrato de repo | exit 0 | `ruby scripts/verify_repo_governance.rb --strict` |
| El gate detecta su ausencia del contrato | exit 1, `unowned_large_file` | falsado retirando la entrada y restaurándola |
| La ruta del `<source>` existe en el artefacto | exit 0 | `ruby scripts/verify_site_artifact.rb public` |
| El gate detecta una ruta rota | aborta «Rendered internal asset references are broken» | falsado cambiando un carácter de `audio.archivo` |
| El bloque se renderiza en el post ES y no en el EN | 1 y 0 | `grep -c 'class="notice capsula-audio"'` en ambos artefactos |
| La cápsula no entra al feed RSS | 0 | `grep -c 'capsula-audio' public/feed.xml` |

## Pendiente de escucha humana

Ninguna de estas se puede comprobar sin oír el archivo:

1. **Los dos acentos salieron distintos.** Se pidió es-ES para el conductor y es-CL para la experta.
   NotebookLM no expone selector de acento por hablante: la petición va en la personalización y no
   está garantizada. Si las dos voces suenan igual, hay que anotarlo aquí y corregir la expectativa
   de la plantilla, no declararlo cumplido.
2. **Los roles se sostienen.** Que A conduzca y B explique, sin que ninguno se atribuya el
   experimento del artículo como experiencia propia.
3. **Las cifras del audio coinciden con las del post.** 380 ejecuciones, 200 del microbenchmark,
   100 del A/B, 50 del holdout, 30 del caso agregado.
4. **No hay cortes ni frases truncadas** al principio ni al final.
5. **No se leen en voz alta identificadores de evidencia ni instrucciones.**

## Duración fuera del criterio original

El prompt con que se generó exigía 300–480 s. El archivo dura **989 s**, más del doble del máximo.
No es un defecto del episodio: NotebookLM no obedece objetivos de duración escritos en la
personalización. La plantilla sucesora corrige la ventana a 600–1200 s con esta medición como única
observación.
