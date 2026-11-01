# Reddit: hilos clave del Post III (en inglés)

No se publicó nada. Decisión del autor: la difusión en Reddit va en inglés, a subs de
datos, política pública y cambio demográfico; los subs chilenos no son pertinentes por temática.
Las reglas oficiales de los subreddits no se pudieron leer de forma automática; lo verificado, los
tamaños y los riesgos están en `QA.md` (sección Reddit). Antes de enviar, revisar en la barra
lateral de cada sub la autopromoción, los enlaces a blogs propios y el flair obligatorio.

Orden sugerido, un sub por día y respondiendo comentarios: r/dataisbeautiful (imagen [OC] y
comentario de fuente), luego r/demography y después r/PublicPolicy. En reserva: r/econometrics,
si se busca crítica del diseño.

## r/dataisbeautiful

**Título:** [OC] 78,972 Chilean students lost their school in 1,141 closures (2005–2024): in all 19 cohorts, progression failure or grade lag rose more than for 734,472 comparable peers

**Primer comentario (fuente y herramientas):** Data: Chilean Ministry of Education administrative records. Tools: DuckDB and Python (matplotlib). Method: staggered difference-in-differences (Callaway and Sant'Anna), exact matching and Manski bounds for missing records. Pooled random-effects gap: +6.29 percentage points (95% CI +4.49 to +8.09). I do not claim this is the causal effect of closure yet: exposed students came from more fragile schools and 47.04% had already switched schools. Article and open CSV: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en

## r/demography

**Título:** If falling birth rates bring more school closures, what happens to the students? Evidence from 78,972 Chilean students who lost their school in 1,141 closures (2005–2024)

**Texto:** I followed Chilean Ministry of Education records for students whose school closed and compared them with 734,472 peers from schools that stayed open. In all 19 cohorts, progression failure or grade lag rose more among those who lost their school; the pooled gap is +6.29 percentage points (95% CI +4.49 to +8.09). I cannot yet call it causal: their schools were already more fragile and 47.04% had switched schools before. My takeaway for planning the demographic transition: assess where the next closures will happen and plan support before, not after. Article and open data: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en

## r/PublicPolicy

**Título:** School closures in Chile, 2005–2024: in all 19 cohorts, students who lost their school fell behind more than their peers. What should a closure protocol require?

**Texto:** Using Chilean Ministry of Education records, I compared 78,972 students who lost their school (1,141 closures) with 734,472 comparable peers. Pooled gap in progression failure or grade lag: +6.29 percentage points (95% CI +4.49 to +8.09). It is not yet a causal estimate, because the closed schools were already more fragile. Still, a list of nearby schools is not continuity: I argue for verified vacancies, safe transport, support at receiving schools and tracking every student for at least two years, plus assessing in advance where the next closures will happen. Article and open data: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en

## r/econometrics (reserva)

**Título:** Feedback welcome: staggered DiD (Callaway–Sant'Anna) with exact matching and Manski bounds on 1,141 school closures in Chile, where pre-closure gaps limit causal claims

**Texto:** Design: 78,972 exposed students (1,141 closures, 2005–2024) against 734,472 matched peers; Callaway–Sant'Anna DiD, exact matching and Manski bounds. Pooled gap: +6.29 pp (95% CI +4.49 to +8.09), positive in all 19 cohorts. Exposed students came from more fragile schools and 47.04% had already switched schools, so I make no causal claim yet. Which robustness checks would you add? Write-up and CSV: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en
