# QA de atribución en primera persona

- Matriz80/80:20posts ES/EN×390/1440×temaslight/academic-night, mediante control real del sitio; todos los casos pasaron.
- Verificados: un h1, héroe responsive800/1600 cargado, preload idéntico, caption breve en primera persona, párrafo p#ai-disclosure breve (≤25palabras), sin badge adicional y con origen de texto/portada coherente con metadatos.
- Enlaces: nota→política del idioma; caption→política#ref. Navegación por teclado, foco visible, toggle real del detalle y procedencia exacta por artículo; ninguna herramienta atribuida sin registro en catálogo.
- Axe4.12.1:0violaciones y0incomplete en héroe/párrafo de80casos más8extras; también0/0 en80detalles de política abiertos. Alcance acotado; no certifica WCAG global.
- Extras8/8: títulos largos ES/EN×ambos temas,320CSS y reflujo equivalente200% (720CSS×450,DPR2). No se afirma zoom nativo de interfaz del navegador.
- Revisión visual:88capturas y4hojas de contacto; títulos completos y atribución visible/legible en ambos temas. Captura individual CASEN móvil revisada además.
- Intento inicial conservado en initial-navigation-race/: diez casos antes de estabilizar la navegación a política, con fallos intermitentes de foco/toggle. El DOM ya cargado sí respondió al teclado. El arnés incorpora networkidle/fonts y comprueba transición real del estado; la nueva matriz completa sustituye ese intento como evidencia de aceptación. No hubo cambio de producto para recuperar verde.
- freeze.json liga nueve componentes fuente y1248archivos del build copiado. Se verificaron también las144entradas del source manifest antes de cerrar. Figuras del cuerpo, archivo/tarjetas y rendimiento tienen evidencia separada; esta revisión no amplía esos alcances.
- Sesión propia heroes-first-person y servidor4038 cerrados. Puerto4004 ajeno intacto. No se editaron archivos de producto.
