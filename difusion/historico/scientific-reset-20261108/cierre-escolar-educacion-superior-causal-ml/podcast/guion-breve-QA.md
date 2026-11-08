# QA del guion breve para NotebookLM: Post IV (`cierre-escolar-educacion-superior-causal-ml`)

- **Guion:** `guion-breve.md` (mismo directorio).
- **Fuente que manda:** post canónico `cierre-escolar-educacion-superior-causal-ml` (<https://3cucharadas.cl/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/>).
- **Fecha:** 7 de noviembre de 2026 (revisión editorial adversarial del mismo día). Etapa: preparado; pendiente generación manual de audio y escucha humana.
- **Extensión:** `wc -w` sobre `guion-breve.md` queda dentro del rango objetivo de seiscientas cincuenta a ochocientas cincuenta palabras, tanto el archivo completo como el texto hablado (unas cinco minutos de locución a ritmo conversacional).
- **Texto hablado:** sin dígitos en los diálogos (`rg '^\*\*[AB]:\*\*.*[0-9]'` no devuelve líneas), sin anglicismos no explicados, sin enlaces leídos en voz alta y sin cifras ajenas al post.

## 1. Verificación de cifras y afirmaciones cuantitativas del guion breve

| Tal como se pronuncia en `guion-breve.md` | Valor en el post | Sección del post ES | Cita o respaldo en el post |
|---|---|---|---|
| "entre trece y quince puntos porcentuales menos" | 13 a 15 pp (−13,24 a −14,64 pp) | Subtítulo y Apertura | "parece restar entre 13 y 15 puntos porcentuales de acceso a la educación superior" |
| "veinte años de matrícula escolar —más de setenta y nueve millones de registros—" | 20 años; 79.709.054 | Apertura | "**79.709.054 registros alumno-año de matrícula escolar** y **73.873.835 de rendimiento** entre 2004 y 2025" |
| "veinte nóminas de Matrícula del SIES entre dos mil siete y dos mil veintiséis, diecinueve de Titulados y seis procesos de admisión PAES y PDT" | 20 (2007–2026); 19 (2007–2025); 6 (2021–2026) | Apertura y Cucharada 1 | "**20 nóminas anuales de Matrícula de Educación Superior del SIES (2007–2026)**, las **19 nóminas de Titulados del SIES (2007–2025)** y los **6 procesos de admisión centralizada PAES/PDT ... (2021–2026)**" |
| "sin tocar los archivos restringidos del DEMRE de dos mil catorce a dos mil veinte" | DEMRE 2014–2020 | Cucharada 1 | "**no utilicé ningún archivo DEMRE 2014–2020**" |
| "menos catorce coma sesenta y cuatro puntos en celdas exactas, o menos trece coma veinticuatro con controles demográficos" | −14,64 pp y −13,24 pp | Apertura y Tabla 2 | "una diferencia de **−14,64 puntos porcentuales** en celdas exactas, o **−13,24 puntos porcentuales** al ajustarla por demografía" |
| "sesenta y dos mil ciento cincuenta y tres estudiantes —treinta y ocho mil quinientos veinticinco en enseñanza media y veintitrés mil seiscientos veintiocho en básica superior—" | 62.153; 38.525; 23.628 | Cucharada 2, Tabla 2 | "modelo DML con *N* = 62.153 estudiantes con historia G−5 completa: 38.525 en Media y 23.628 en Básica Superior" |
| "pasa de menos trece coma veinticuatro a menos cinco coma sesenta y tres puntos" | −13,24 a −5,63 pp | Apertura y Tabla 2 | "la brecha ajustada baja de −13,24 pp a menos de la mitad (**−5,63 pp**, intervalo de −9,78 a −1,47 pp)" |
| "Cuatro años antes que la generación expuesta —en G menos cinco—, las generaciones anteriores de esos mismos liceos ya entraban doce puntos porcentuales menos" | G−5; −12,00 pp (82,0 %) | Apertura y Tabla 2 | "cuatro años antes que la generación expuesta (G−5), las generaciones anteriores de esos mismos liceos secundarios ya ingresaban **12,00 puntos porcentuales menos**" |
| "Más de cuatro quintos de la brecha bruta ya existían antes del cierre" | 82,0 % de −14,64 pp | Apertura | "**Más de cuatro quintos de la brecha aparente ya existían antes del cierre**" |
| "la brecha baja a menos dos coma sesenta y cuatro puntos" | −2,64 pp [−7,54; +2,25] | Apertura y Tabla 2 | "Al comparar con la generación G−5 del mismo liceo, la brecha baja a **−2,64 pp** en diferencias en diferencias" |
| "el efecto promedio general llega a menos cero coma veintinueve puntos porcentuales, indistinguible de cero" | −0,29 pp [−2,64; +2,06] | Apertura y Tabla 2 | "llega a **−0,29 pp** en *Double Machine Learning* completo (de −2,64 a +2,06 pp), estadísticamente indistinguible de cero" |
| "En séptimo y octavo básico tampoco se detecta pérdida promedio: da más uno coma veintiún puntos en diferencias en diferencias y más uno coma cero dos en el modelo completo" | +1,21 pp y +1,02 pp | Apertura, Tabla 2 y Apéndice §2 | "**+1,21 pp** en diferencias en diferencias ... **+1,02 pp** en *Double ML* completo"; "leo su +1,21 pp como ausencia de daño detectable y no como beneficio" |
| "contracción neta y significativa de menos dos coma cero nueve puntos porcentuales incluso tras descontar la historia G menos cinco del liceo" | −2,09 pp (EE 0,72, p = 0,0037, [−3,50; −0,68]) | Apertura y Tabla 2 | "en **institutos profesionales y centros de formación técnica (IP/CFT)**, que retrocede **−2,09 puntos porcentuales** incluso en el modelo *Double ML* más exigente" |
| "el acceso universitario sube más uno coma noventa y ocho puntos sin distinguirse de cero" | +1,98 pp [−0,22; +4,19] | Tabla 2 y Cucharada 3 | "el acceso universitario sube +1,98 pp (de −0,22 a +4,19)" |
| "el artículo la lee como contracción del canal técnico-profesional, no como pérdida demostrada de acceso" | lectura del autor | Cucharada 3 | "leo el −2,09 pp como una contracción del canal IP/CFT, no como una pérdida demostrada de acceso" |
| "el veinte por ciento más vulnerable, G uno ... cae menos doce coma veintiséis puntos en acceso total, menos ocho coma cero dos en IP y CFT y menos once coma cuarenta y ocho puntos en persistencia al segundo año" | G1: −12,26 pp; −8,02 pp; −11,48 pp | Apertura y Tabla 4 | "registra una caída de **−12,26 pp en acceso total**, **−8,02 pp en IP/CFT** y **−11,48 pp en persistencia de segundo año**" |
| "al añadir la historia del liceo, la caída general de G uno baja a menos cero coma veintiséis puntos, pero la heterogeneidad en IP y CFT persiste" | −0,26 pp; β₂ = +0,425 (p = 0,0177) | Apertura y Cucharada 3 | "al añadir la historia G−5 del liceo, la caída de G1 en acceso total baja a −0,26 pp"; "en el canal técnico-profesional IP/CFT ... la pendiente de heterogeneidad se mantienen vivas y estadísticamente significativas" |
| "cuatro medidas" (síntesis del cierre) | — | Cierre | Diferenciar por nivel; protocolo nominal hacia IP/CFT; convalidación de especialidades y FUAS; seguimiento los primeros dos años. El post no numera cuatro reglas: el guion las presenta como resumen del cierre, no como enumeración literal |
| "Son resguardos prudenciales, no efectos estimados" | — | Cierre | "Estos resguardos prudenciales no son efectos estimados de esas decisiones" |

## 2. Verificación de tono, registro y reglas editoriales

- [x] Conversación en español de Chile natural entre dos voces (`A` y `B`), sin tono comercial ni exageraciones causales; la hipótesis rival de sustitución hacia universidades aparece como límite explícito.
- [x] Ninguna cifra ajena al post aparece en el guion ni en este archivo de verificación (comprobación numérica equivalente al gate, corrida el 7 de noviembre de 2026; ver `QA.md` §2).
- [x] Cierra con la síntesis de política del artículo y la declaración de voces sintéticas.
