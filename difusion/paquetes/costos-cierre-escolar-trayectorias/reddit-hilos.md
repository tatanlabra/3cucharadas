# Reddit: hilos clave del Post III (ES y EN)

No se publicó nada. Las reglas oficiales de los subreddits no se pudieron leer de forma automática;
el registro de lo verificado, los tamaños y los riesgos está en `QA.md` (sección Reddit). Antes de
enviar, revisar en la barra lateral de cada sub la autopromoción, los enlaces a blogs propios y el
flair obligatorio.

Orden sugerido, un sub por día y respondiendo comentarios: en español, r/chile y luego
r/RepublicadeChile; en inglés, r/dataisbeautiful (imagen [OC] y comentario de fuente), luego
r/econometrics y al final r/education.

## r/chile

**Título:** Seguí a 78.972 estudiantes que perdieron su escuela en 1.141 cierres (2005–2024): en 19 de 19 cohortes, su falla de progresión o rezago creció más que la de sus pares

**Texto:** Extendí mi tesis con registros del Mineduc y comparé a esos estudiantes con 734.472 pares de escuelas que siguieron abiertas (diferencias en diferencias escalonadas). Efecto global: +6,29 puntos porcentuales (IC 95 %: +4,49 a +8,09). Todavía no puedo atribuirlo al cierre: venían de escuelas más frágiles y el 47,04 % ya se había cambiado de colegio antes. La pregunta de política es dónde ocurrirán los próximos cierres, para planificar el acompañamiento. Infografía y CSV abiertos: https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3

## r/RepublicadeChile

**Título:** Cierres de escuelas en Chile, 2005–2024: en 19 de 19 cohortes, a quienes perdieron su escuela les fue peor que a sus pares (+6,29 puntos), pero todavía no es un efecto causal probado

**Texto:** Usé registros del Mineduc y comparé a 78.972 estudiantes con 734.472 pares comparables. La brecha global es de +6,29 puntos porcentuales (IC 95 %: +4,49 a +8,09). No la atribuyo todavía al cierre: los expuestos venían de escuelas más frágiles y el 47,04 % ya se había cambiado de colegio. Creo que la discusión útil es dónde ocurrirán los próximos cierres con la transición demográfica y cómo acompañar a esos estudiantes. ¿Qué opinan? Artículo y CSV: https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3

## r/dataisbeautiful

**Título:** [OC] 78,972 Chilean students lost their school in 1,141 closures (2005–2024): in all 19 cohorts, progression failure or grade lag rose more than for 734,472 comparable peers

**Primer comentario (fuente y herramientas):** Data: Chilean Ministry of Education administrative records. Tools: DuckDB and Python (matplotlib). Method: staggered difference-in-differences (Callaway and Sant'Anna), exact matching and Manski bounds for missing records. Pooled random-effects gap: +6.29 percentage points (95% CI +4.49 to +8.09). I do not claim this is the causal effect of closure yet: exposed students came from more fragile schools and 47.04% had already switched schools. Article and open CSV: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en

## r/econometrics

**Título:** Feedback welcome: staggered DiD (Callaway–Sant'Anna) with exact matching and Manski bounds on 1,141 school closures in Chile, where pre-closure gaps limit causal claims

**Texto:** Design: 78,972 exposed students (1,141 closures, 2005–2024) against 734,472 matched peers; Callaway–Sant'Anna DiD, exact matching and Manski bounds. Pooled gap: +6.29 pp (95% CI +4.49 to +8.09), positive in all 19 cohorts. Exposed students came from more fragile schools and 47.04% had already switched schools, so I make no causal claim yet. Which robustness checks would you add? Write-up and CSV: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en

## r/education

**Título:** School closures in Chile, 2005–2024: progression failure or grade lag rose more among 78,972 students who lost their school than among 734,472 comparable peers, in all 19 cohorts

**Texto:** I extended my thesis with Chilean Ministry of Education records. Pooled gap: +6.29 percentage points (95% CI +4.49 to +8.09). I cannot yet attribute it to the closure: exposed students came from more fragile schools and 47.04% had already changed schools. The policy question is where the next closures will happen as enrolment shifts with the demographic transition, so that support can be planned in time. Article and CSV: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=reddit&utm_medium=social&utm_campaign=tesis_post3_en
