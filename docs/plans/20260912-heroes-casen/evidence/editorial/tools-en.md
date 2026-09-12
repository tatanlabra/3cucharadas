<aside class="notice--info" markdown="1">
**Behind the analysis: Python and reproducible geomatics**

Python connects cadastral, census and territorial aggregates; Parquet stores columnar tables, and Matplotlib produces these figures in SVG and PNG with typography and palettes for both reading modes. Each chart comes from a verifiable table: the image helps readers see the pattern, while the table exposes the values. The viewer retains ECharts for interactive exploration and map layers for examining territory.

For CASEN, R opens the original dataset and passes the required columns to Python through an in-memory pipe. Python computes estimates and design variance; algebraic fixtures and a bounded comparison with Julia check the implementation. Separating extraction, computation, presentation and checks makes similar work easier to carry into larger computing workflows. **This execution is local: it is neither a benchmark nor a demonstrated HPC-cluster run.** The [method and provenance](/catastro_sii_brecha/data/casen-shared-site/method.md) document what was actually done.
</aside>
