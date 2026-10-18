# QA — cápsula de audio de la serie de la tesis (Post I y Post II)

Estado: **publicado en Spotify** (`https://open.spotify.com/episode/7ho9naqSgAotsTfcsBmOwc`, HTTP 200); **pendiente de escucha humana**.

## Comprobado por máquina (2026-10-17)

| Comprobación | Resultado | Cómo |
|---|---|---|
| Máster custodiado sin re-encode | sha256 `eae58af0…` en origen y custodia | `sha256sum` |
| Ensamblado con las cortinas vigentes | intro y outro con correlación 0,9999; control negativo 0,01-0,02 | `/tmp/cmp-cortinas-scripts/cmp.py` sobre `intro.wav`/`outro.wav` |
| Sonoridad del ensamblado | −16,02 LUFS, −1,41 dBTP (igual que los tres episodios publicados) | `ffmpeg -af loudnorm=print_format=json -f null -` |
| Duración | 1.187,5 s (19:48) | `ffprobe` |
| La cápsula sale en los posts ES y no en los EN | ES I = 1, ES II = 1, EN I = 0, EN II = 0 | `rg -c 'class="notice capsula-audio"'` en los cuatro artefactos |
| La cápsula no entra al feed RSS | 0 apariciones en `feed.xml` | `rg -c capsula-audio public/feed.xml` |

## Pendiente de escucha humana

1. Las cifras del audio coinciden con los posts: Post I (50 hipótesis, 34 juicios) y Post II (900 cierres oficiales, 330 estrictos, 665 con trayectoria, `28 → 23 → 1`).
2. El audio conserva las salvedades del Post II: no identifica efectos causales y no es una regla para decidir qué escuelas cerrar. El título del episodio pregunta «¿cuáles cerrar?»: comprobar que el audio lo trata como pregunta y no como recomendación.
3. No menciona casos retirados por el redline (Lo Prado, Lo Barnechea, «parte III»).
4. Sin cortes ni instrucciones leídas en voz alta.
