<!--
INSTRUCCIONES DE PUBLICACIÓN — NO PEGAR EN MEDIUM
1. Preferencia: Import a story con la URL canónica inglesa y luego reemplazar el cuerpo por esta adaptación.
2. Si se pega manualmente: More settings → Advanced settings → This story was originally published elsewhere.
3. Canónico obligatorio: https://3cucharadas.cl/en/ia/productividad/desarrollo/nushell-coprocesador-estructurado/
4. Imagen: https://3cucharadas.cl/assets/images/structured-shell/og-1200-en.webp
5. Texto alternativo: A data stream enters a processing core and splits into three structured routes shown in blue, magenta, and grey.
6. Verificar el canónico en el código fuente del borrador antes de publicar.
-->

# I Gave a Coding Agent a Structured Shell. The Benchmark Was Not the Answer.

## Nushell improved some answers, slowed every timed pipeline, and changed nothing in the case that looked most realistic.

I started with a familiar intuition: if a coding agent receives structured values instead of columns of text, it should make fewer parsing mistakes. Dates remain dates, sizes remain sizes, and selecting a field does not depend on counting spaces.

That intuition is plausible. It is not a result.

So I kept zsh as my shell, added Nushell as a selective route, and tried to make the decision falsifiable. The policy was deliberately conservative. Native commands came first, specialised utilities such as `jq` or `rg` came second, Nushell came third for multi-step structured transformations, and analytical engines came fourth for larger problems.

The route was not supposed to activate often. It was supposed to activate for a reason.

### The first answer was simply “slower”

I began with four small pipeline tasks and repeated each implementation 25 times. Across 200 runs, Nushell was slower in every timed comparison.

Finding recently modified large files took a median 389 milliseconds with the traditional route and 1,315 milliseconds with Nushell. Selecting the five processes using the most memory took 22 milliseconds versus 233. Grouping containers by image took 19 versus 40.

Structure did not automatically reduce output either. It helped when the task contained real aggregation: reducing `docker ps -a` context produced 566 bytes instead of 3,353, at the cost of 39 milliseconds instead of 17. On the other tasks, the structured representation was larger.

If I had published only this benchmark, the conclusion would have been easy: do not add the route. But those were pipelines I had written. The real question was whether an agent would avoid errors when it had to choose and compose the command.

### The agent was more accurate, and more expensive

I built a tuned corpus with three task families where the policy favoured Nushell and two where it should stay out. Ten repetitions per family and arm produced 100 agent runs.

On the positive tasks, observed accuracy rose from 23/30 without the skill to 30/30 with it. Negative tasks remained 20/20 in both arms, and the treatment correctly avoided Nushell in all 20 negative runs.

The improvement was not free. Median time on positive tasks rose from 6,239 to 9,537 milliseconds. Median output rose from 152 to 368 tokens.

A Fisher exact test on the 60 positive runs yields a small p-value, but treating repetitions as independent problem types is not a defensible basis for generalisation. There were only three positive families, and they had been used while tuning the integration. The number describes that corpus; it does not certify a universal gain.

The failures explained more than the aggregate score. One recurring command used `fd -I`, assuming it included hidden files. It does not. Ignoring exclusion rules and including hidden paths are separate choices. Another run piped Bash into `nu -c`, received `null` with exit code 0, and spent 77 seconds searching for an answer. Adding the documented `--stdin` route reduced that case to under eight seconds.

These were not abstract warnings about shell syntax. They were silent failures that looked successful from the outside.

### The holdout made the story smaller

The tuned result was too neat. I froze the skill description and added five held-out tasks, then ran both arms five times: another 50 runs.

On the positive holdout, accuracy was 14/15 with the skill and 10/15 without it. But the policy activated Nushell in only 4/15 treatment runs, all within one family. Two other positive families reached 5/5 without activating the route.

That does not erase the observed improvement. It changes what the improvement can mean. The 28/30 activation rate belonged to the tuned corpus, not to the integration in general.

### The realistic case produced no accuracy difference

For a second counter-test, I reused a governed temporal audit from a reconstruction of my master's thesis. The public fixture contains aggregates only: a source with 306,768 rows and 263 columns reduced to 21 annual rows. One task requested a valid ranking, one supplied a corrupted fixture that had to be rejected, and one asked for an institutional conclusion the data could not support.

Across three tasks, two arms, and five repetitions, both arms were correct every time. The treatment used Nu in 10/10 structured observations and 0/5 conceptual observations. The policy behaved as intended and produced no accuracy advantage.

That is not a failed experiment. It is a useful case of indifference. Once both routes already satisfied the contract, changing the shell changed implementation details rather than the outcome.

### The conditional rule survived

After 380 runs, I kept a smaller rule than the one I expected to defend:

Use Nushell when the task combines structured input, multiple transformations, and a concrete risk of silent text-parsing failure. Prefer a native command or specialised utility for simpler work. Move to an analytical engine when the problem outgrows shell-scale manipulation.

This is evidence from one EndeavourOS/Arch machine using zsh, Nushell 0.115.1, Claude Code, and Codex. The task families are few, some were used during tuning, and the project that implemented the policy also produced the measurements. Those limits travel with the result.

The [canonical article](https://3cucharadas.cl/en/ia/productividad/desarrollo/nushell-coprocesador-estructurado/) includes the interactive R viewer, full tables, references, and the reproducible aggregate case.

What I would like to compare next is not a list of favourite tools. It is evidence: what task made a structured shell, `jq`, DuckDB, Python, or a dedicated tool measurably better than the simplest baseline that already worked?
