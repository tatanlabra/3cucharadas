# QA — cápsula de audio de Avalúos II

Estado: **escuchado y aprobado por la persona usuaria** antes de incorporarlo al post (13-09-2026).

## Comprobado por máquina (2026-09-13)

| Comprobación | Resultado | Cómo |
|---|---|---|
| El re-encode conserva la duración | 1616,294603 s en máster y publicado | `ffprobe -show_entries format=duration` sobre los dos |
| El publicado es mono AAC | `codec_name=aac`, `channels=1` | `ffprobe -show_entries stream=codec_name,channels` |
| Peso declarado == peso real | 13.503.679 bytes en `audio.bytes` y en disco | `stat -c '%s'` |
| Reducción frente al máster | 74 % (52.019.422 → 13.503.679) | aritmética sobre los dos `stat` |
| Declarado en el contrato de repo | exit 0 | `ruby scripts/verify_repo_governance.rb --strict` |
| La ruta del `<source>` existe en el artefacto | exit 0 | `ruby scripts/verify_site_artifact.rb public` |
| El bloque se renderiza en el post ES y no en el EN | 1 y 0 | `grep -c 'class="notice capsula-audio"'` en ambos |

## Lo que la máquina no puede decir, y aquí se anota

**La coherencia con la revisión del mismo día no está verificada por máquina.** El commit
`a71c0d9c` (12:00) añadió al post la sección sobre líneas de construcción H dentro de roles de otro
destino y precisó el tratamiento de la pregunta CASEN de sitio compartido. El audio se descargó a
las 14:03. La marca de tiempo permite que el episodio se generara sobre el texto ya revisado, pero
no lo demuestra: si la fuente cargada en NotebookLM fue la versión previa, la cápsula no menciona
esa sección. No es un error que invalide el episodio —el post sigue siendo el registro— pero
conviene saberlo si alguien pregunta por qué el audio no habla de las líneas H.

**Escenarios tributarios.** El post lleva `editorial_status: escenario-tributario-hipotetico`. Si
el audio presenta esas cifras en pesos sin la salvedad de que son escenarios bajo supuestos
explícitos, habría que anotarlo aquí; la escucha de aprobación no reportó ese problema.

## Duración

1616 s (26:56), fuera de la ventana 600–1200 s que fijó el primer episodio. Ver `README.md`: la
ventana se revisó a 600–1800 s con esta medición, no se recortó el audio.
