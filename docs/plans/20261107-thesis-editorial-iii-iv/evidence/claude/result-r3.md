REVIEW_VERDICT: REQUEST_CHANGES

**Dictamen:** M1–M4 y los seis menores de r2 quedaron resueltos o refutados con fuente. Aparecen 2 defectos materiales nuevos y 4 menores. Ninguno es de cifras: son de interpretación y de bibliografía. No edité nada. Esta ronda es dirigida, no un segundo Goldfish.

## Resolución de r2

| Hallazgo | Estado | Evidencia |
|---|---|---|
| M1 brecha sin definir (III) | Resuelto | Subtítulo `:5` dice «aumento estimado»; el aviso `:58` define la brecha como diferencia entre el cambio de expuestos y el de controles. |
| M2 −0,26 sin soporte local | Refutación válida | El JSON trae G1 `−0,26` con IC `[−2,73; 2,21]` y BLP `het_p_value 0,6583`. IP/CFT completo también cuadra: `−2,09`, G1 `−2,57`, G3 `−3,92`, β₂ `0,425`, p `0,0177`. El anexo `:185` da la ruta. |
| M3 «sólido» | Resuelto | Post IV `:108` enfrenta el DiD `−2,59`, EE 2,29, p 0,28 y 12 liceos; el JSON da `p_value 0.281`. El alt de la figura 1 dice «bajo ese modelo». |
| M4 sesgo de G−5 en básica | Resuelto | Principal `:96` y anexo `:241`. La condición es correcta solo para 7.º Básico, y el anexo `:235` lo explica. |
| Menores 1–6 | Resueltos | Los p y el IC del `−3,79` son coherentes con t de 6 g.l. y siete conglomerados. Acepto la refutación del 77,5 %: eran denominadores distintos. |

## Hallazgos materiales

**[MAT] `_posts/2026-11-04-…md:11,110,123`, alt y caption de fig. A2, anexo `:165,168,187` → «G1 baja de −12,26 a −0,26» compara dos grupos distintos → reformular.**
- Hecho: el JSON trae `clan_g1_vs_g5` para cada especificación. G1 solo con controles estudiantiles es 99,5 % media, 77,2 % técnico-profesional (TP), nota 5,33 y asistencia 87,1 %. G1 con historia G−5 es 91,2 % media, 51,8 % TP, nota 5,79 y asistencia 85,0 %.
- Consecuencia: los quintiles se reordenan en cada especificación. El texto dice «la estimación de G1 baja», que se lee como el mismo grupo antes y después. Eso no está identificado.
- Ajuste: «el quintil de mayor daño predicho con controles individuales muestra −12,26; con historia escolar, el quintil equivalente —otros estudiantes, 91 % de media— muestra −0,26 y el BLP no detecta heterogeneidad (p = 0,66)».
- Ajuste: añadir al anexo la fila CLAN de la especificación completa, que hoy solo documenta la estudiantil (`:189`).

**[MAT] `_posts/2026-11-04-…md:155` (Referencias) → la nota `[^chernozhukov2018]` de `:94` no tiene definición.**
- Hecho: `rg '^\[\^chernozhukov'` no encuentra nada en el principal. Mi primer script lo dejó pasar porque la referencia va seguida de `:`; el `rg` posterior lo confirma.
- Efecto: Jekyll no puede resolver la nota y deja el marcador sin enlace.
- Ajuste: copiar la entrada Chernozhukov et al. 2018 desde `_pages/tesis-post4-anexo-metodologico.md:310`.

## Hallazgos menores

- **[MEN] Post IV `:5,47`:** el subtítulo dice «persiste una contracción estimada» y el aviso da `−2,09` sin estimador. El límite del aviso no menciona que el análogo de cohortes repetidas (`−2,59`, p 0,28) no se distingue de cero. Ese dato solo está en `:108`. Añadir una cláusula al «Límite».
- **[MEN] Post IV `:47`:** `−0,29` aparece sin intervalo. Añadir `[−2,64; +2,06]` para que «cercana a cero» quede acotado.
- **[MEN] Anexo III `:172,208`:** dicen «tabla A1 / A4 del cuerpo principal», pero esas tablas están en el anexo. Cambiar a «de este anexo».
- **[MEN] Anexo III `:226` y anexo IV `:292`:** hay un `</details>` huérfano; ningún archivo abre `<details>`. Eliminarlo.

## Opcionales

- «G1» choca con «G−1» y «G−5» para un lector no especialista, y el excerpt `:11` usa la jerga sin definirla. Usar «el quintil de mayor daño predicho».
- Anexo III `:94`: a la tabla A4 le falta `{: .table-caption}`.
- Los p `0,0037` y `0,0177` (anexo IV `:182`) salen de varios desenlaces y especificaciones sin corrección por multiplicidad. Basta una frase.

## Criterios

| Criterio | Veredicto |
|---|---|
| 1. Preámbulo | Cumple. Distingue tasa de diferencia de tasas; falta el límite IP/CFT (MEN). |
| 2. Hilo y extensión | Cumple. Mi conteo, sin referencias ni HTML: III ≈ 2.572 palabras, IV ≈ 2.926. Sin ELI5. |
| 3. Anexos y límites | Cumple. Los límites decisivos están en el principal; el CLAN completo falta en el anexo (MAT 1). |
| 4. Mismo hecho y límite | Falla solo en MAT 1. No hay causalidad promovida desde no significación. |
| 5. Cierre, citas y referencias | Cierres con tres desafíos verificables. Falla en MAT 2 y en las referencias cruzadas del anexo III. |
| 6. Preámbulo, alt y cierre vs. tablas | Cifras coinciden. Falla en la lectura de G1 (alt, caption, cierre) y en los límites del preámbulo. |

## Fortalezas y contraejemplos

- III separa sin ambigüedad las cotas de Manski de la inferencia por intervalos. El `−3,35` queda como descriptivo, sin intervalo propio.
- IV declara la sustitución IP/CFT→universidad como hipótesis rival, con prueba discriminante y condición de descarte.
- Contraejemplo a MAT 1: el cambio de composición no invalida el resultado. Un quintil más heterogéneo pero con BLP nulo apoya que la heterogeneidad se absorbe. Lo que falla es la redacción «G1 baja», no la conclusión.

## Límites y riesgo residual

- Verifiqué contra el JSON los valores de M2/M3, el CLAN de ambas especificaciones, las t de los DiD por régimen y los denominadores 70,58 % y 3.556.
- No verifiqué la banda de recorte `[+3,79; +6,80]` (anexo IV `:49`), el multiplicador `14,24` (`:241`) ni los manifiestos de figuras. No ejecuté builds ni los verificadores. Las versiones EN quedan fuera de alcance.
- Riesgo residual tras corregir MAT 1–2: bajo. El texto se toca en seis lugares y no hace falta tocar CSV ni JSON.

EDITORIAL_REVIEW_COMPLETE

HANDOFF-TRACE: Claude → Codex vía claude-bridge; revisión dirigida completada.

MODEL-REPORT: Claude Sonnet 5.5 (`claude-sonnet-5-5`), Anthropic.

PLAN_STATE v2 (plan no cerrado; solo cambia F2):
```yaml
- id: "F2"
  glyph: "[~]"
  status: "active"
  step: "F2 · Claude · revisión dirigida realizada; dictamen REQUEST_CHANGES (2 materiales nuevos: G1 no es el mismo grupo, nota chernozhukov2018 sin definir; 4 menores); correcciones pendientes del editor ES"
  deps: ["ES"]
# Resto del estado recibido sin cambios. F3, EN, PDF, F4 y F5 siguen pendientes y dependen de F2.
```
