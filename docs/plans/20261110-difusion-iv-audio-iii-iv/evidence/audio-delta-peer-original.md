[Posts III/IV:25,43] → **APPROVE del delta de audio** → la inversa exacta de ambas adiciones reproduce los archivos de `HEAD` (`a8f18e8b08a883f09d0d28a80faba6ab2bb95319`).

| Binding | SHA-256 previo → actual |
|---|---|
| [Post III](/home/ende/Descargas/programaciones/activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md:43) | `d43588ecfab11c28ea28fce4fe5f310362d3969137d085988dde0a219b538e22` → `bad473d666d7e60fe2ea231adddf5c78e054fe28339380a2896293c9455b9c3e` |
| [Post IV](/home/ende/Descargas/programaciones/activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md:43) | `6ac97d5ed70f963ffe04f9eb9ccd588c1c7ec7e154b5020f07db7e7485e92ab6` → `825fe015865215c6c48aeb65b40741d9110731962648313a34c93cd4b2752672` |

- **HECHO:** de los 403 bindings de [semantic-review.json](/home/ende/Descargas/programaciones/activos/3cucharadas/assets/data/tesis-scientific-reset/semantic-review.json:1), 401 coinciden, dos difieren —solo esos posts ES— y ninguno falta. En el repositorio también existen otros cambios concurrentes fuera de los bindings.
- **HECHO:** cada diff agrega exactamente 12 líneas: `audio: generated` y un bloque con 768 s, fecha `2026-11-10`, NotebookLM (Google), dos voces ES, Spotify `4VIIXt7nDk8RwrtkqEVVZ7` y Apple Podcasts `id6811713988`. Al retirarlos, ambos archivos coinciden byte a byte con `HEAD`; sus cuerpos científicos permanecen idénticos. `git diff --check` terminó con código 0.
- **Evidencia documental:** [spotify-replacement.json](/home/ende/Descargas/programaciones/activos/3cucharadas/docs/plans/20261110-difusion-iv-audio-iii-iv/evidence/spotify-replacement.json:2) registra `public_sha256 = expected_sha256 = b17fa59baaabf1642f800d329836a1e253d0aa336f2f86f7bfb564ea611f8499`, `identical: true` y `00:12:48`.
- **Límite:** leí el recibo, pero no descargué ni escuché el audio, no verifiqué Apple en vivo ni repetí la revisión científica íntegra. Corresponde reanclar el recibo conservando sus hashes originales y documentando estas dos adiciones; este dictamen solo acredita el delta.

HANDOFF-TRACE: Codex integrador → Codex revisor, collaboration, gpt-6-sol high.
