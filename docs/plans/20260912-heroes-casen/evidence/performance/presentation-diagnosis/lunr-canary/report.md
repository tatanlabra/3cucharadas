# Ensayo Lunr diferido — no demuestra mejora LCP

Una única comparación acotada del MISMO build candidato congelado: lado baseline=JavaScript original; lado candidate=respuesta interceptada exclusivamente de lunr-en.js con constructor memoizado a primer focus/input/keyup. Sin modificaciones al filesystem de producto, sin formal adicional, sin excluir muestras. Mismo Chrome151,1440×1000,DPR1,light,no-store,ventana5000ms;8/8observaciones presentes.

| Página/estado | Original LCP ms | Lunr diferido LCP ms | CPU original/diferido |
|---|---:|---:|---:|
| Avalúos cold |984|1880|43,9%/86,1%|
| Avalúos warm |252|416|60,9%/49,1%|
| CASEN cold |1056|1128|30,5%/33,4%|
| CASEN warm |224|248|38,2%/26,8%|

Hecho favorable: las tareas largas originales de indexación (Avalúos341/222ms; CASEN195/304ms) desaparecen del warm diferido y de CASEN diferido; Avalúos cold conserva una tarea61ms. El prototipo sí separó trabajo real del momento de carga.

Hecho contrario: LCP no mejoró en ninguno de los4contrastes. El original Avalúos warm empezó pintura134,6ms y luego su tarea larga135,7ms; presentación252ms. Que el callback tarde no significa que el índice haya retrasado por igual el timestamp de presentación. El compositor puede avanzar mientras el hilo principal trabaja.

Confusión: Avalúos cold diferido coincidió con86,1%CPU y los pares no están replicados; no se puede concluir daño causal de+896ms. Tampoco se puede concluir beneficio solo por reducir longtasks: el outcome contratado es LCP estándar y aquí no mejoró. CASEN warm tiene gap pintura-presentación104,5ms original/104,0ms diferido, otro contraejemplo a una explicación exclusiva por indexación.

Búsqueda: los4chequeos posventana devolvieron5artículos para casen; original ya tenía idx y diferido pasó de idx ausente a presente. Son eventos DOM sintéticos focus/input/keyup, no QA visual de teclado. El índice diferido tardó346,4ms en Avalúos y260,9ms en CASEN: deuda trasladada a primera interacción, no eliminada. No se midió INP de interacción humana y no corresponde afirmar cumplimiento de INP.

Juicio: no adoptar este prototipo como corrección demostrada de Q1. Mantener el formal en RED y evitar repetir hasta obtener PASS. Si se decide trabajar sobre búsqueda por mérito propio, la pregunta debe incluir el costo de primera interacción y quizá un worker/precalentamiento; eso amplía alcance y no se ejecutó.

Hipótesis debilitada: Lunr es el cuello dominante y suficiente para resolver LCP. Evidencia que permitiría rehabilitarla: comparación replicada y alternada en carga equiparable, con trazas que sitúen indexación antes de la presentación y reducción estable del LCP. Condición de descarte para una mejora propuesta: su LCP no mejora al cambiar solo esa ejecución, o degrada accesibilidad/resultados/primera interacción. Este ensayo ya aporta evidencia contraria; no justifica un cambio de producto.

Artefactos: runs.json estándar y raw; search-checks.json; settings.json documenta hash del JS realmente servido; row.resources_sha256 refleja el prototipo interceptado, no el original en disco. La integridad del build1248 y fuentes144se verificó antes/después, sin cambios. La respuesta interceptada es un tratamiento experimental, por lo que receipt no equivale a aceptación del build congelado. Ambos servidores propios y4sesiones cerrados;4004intacto.
