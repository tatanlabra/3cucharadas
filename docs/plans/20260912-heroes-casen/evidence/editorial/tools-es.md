<aside class="notice--info" markdown="1">
**Detrás del análisis: Python y geomática reproducible**

Python conecta los agregados catastrales, censales y territoriales; Parquet conserva las tablas en formato columnar y Matplotlib produce estas figuras en SVG y PNG, con tipografía y paletas para ambos modos de lectura. Cada gráfico parte de una tabla verificable: la imagen sirve para leer el patrón y la tabla para examinar los valores. El visor mantiene ECharts para la exploración interactiva y las capas cartográficas para revisar el territorio.

Para CASEN, R abre la base original y entrega a Python las columnas necesarias mediante una tubería en memoria. Python calcula las estimaciones y la varianza de diseño; fixtures algebraicos y una comparación acotada con Julia contrastan la implementación. Separar extracción, cálculo, representación y controles facilita llevar trabajo semejante a flujos de cómputo de mayor escala. **Esta ejecución es local: no constituye un benchmark ni una ejecución demostrada en un clúster HPC.** El [método y la procedencia](/catastro_sii_brecha/data/casen-shared-site/method.md) permiten revisar qué se hizo efectivamente.
</aside>
