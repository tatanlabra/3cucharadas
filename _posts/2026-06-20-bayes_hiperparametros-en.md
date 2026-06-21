---
layout: single
title: "Bayesian hyperparameters in 3 spoonfuls: less grid, more statistical memory"
subtitle: "Bayesian optimization in Python for vulnerability and expected-purchase-value models"
date: 2026-06-20
categories: [mlops, hpo, python, h2o]
tags: [bayesian-optimization, hyperparameter-optimization, h2o, xgboost, ebm, rsh, ecommerce, aucpr, reproducibility]
description: "A direct guide to using Bayesian optimization as a hyperparameter search strategy for predictive models: a public RSH-style case with EBM and a private ecommerce-style case with H2O XGBoost."
author: clabra
lang: en
ref: bayes-hiperparametros
permalink: /mlops/bayes-hiperparametros/
toc: true
toc_sticky: true
comments: true
author_profile: true
math: true
---

Imagine a tabular model with 10 values of <span class="text-nowrap">learn_rate</span>, 8 of <span class="text-nowrap">max_depth</span>, 5 of <span class="text-nowrap">sample_rate</span> and 5 of <span class="text-nowrap">col_sample_rate</span>. A Cartesian grid would train **2,000 models**. With 5-fold cross-validation, the operational count rises to **10,000 internal fits**. On a machine with limited RAM, VRAM or CPU, that is not necessarily more rigor: it can be just an expensive way of ignoring what was learned in previous evaluations.
{: .text-justify}

This post proposes using Bayesian optimization (BO) as an external decision layer in Python. It does not always win. It wins when the problem looks like this: an expensive objective function, a bounded search space, a reasonably stable metric and a limited budget.
{: .text-justify}


**Three ideas to start with:**

- **BO does not assume that the hyperparameter follows a particular distribution.** In the classic case with Gaussian processes, what is modeled probabilistically is the objective function evaluated at different points of the hyperparameter space.
- **Random search is still a serious baseline.** Bergstra and Bengio showed that it can be far more efficient than a grid when not all hyperparameters matter equally. BO starts from there and adds statistical memory.
- **Optimizing hyperparameters does not fix a bad objective function.** In RSH, for example, one could model a circularity (what is now called "information leakage" 🌊). In ecommerce — not my field (comments welcome) — it would be confusing propensity with causality. In both cases, BO can find a solution faster if the predictive design is well posed.

---

## Tolerance to contrast, or checking against evidence

This post does not yet compare empirical results (the second leg), but I have tested its behavior in production on a couple of cases, so it comes from the empirical side with real data and full traceability (SAT: Early Warning System for School Dropout, and a vulnerability sub-bracket model in RSH, brackets within the most vulnerable 40% using EBM).
{: .text-justify}

{: .table-caption}
**Table 1** — Minimum evidence to support the approach

| Point                                                                                               | Evidence                                                                                                                                                                                                                                                                                                                                                                                                 | Practical implication                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| H2O handles training well, but does not ship BO as a standard native search                         | [H2O Grid Search](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/grid-search.html) documents Cartesian and random grids.                                                                                                                                                                                                                                                                                 | If we want an informed sequential search, H2O can remain the training engine and Python the external optimization layer. The separation is clean: H2O trains; Optuna, SMAC, BoTorch or `skopt` decide the next point.                  |
| For this post, Optuna is a more practical option than `gp_minimize`                                 | [Optuna](https://optuna.org/) is designed as an HPO framework, with studies, trials, persistence, samplers and pruners. Its [`GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html) also fits a Gaussian process over the objective function.                                                                                                   | In an H2O + Python flow, Optuna lets you log every run, resume experiments and compare samplers. `gp_minimize` serves to explain BO in a few lines, but Optuna is more defensible as a working tool.                                   |
| Normality is not in the hyperparameter, but in the probabilistic model of the objective function    | In BO with Gaussian processes, what is modeled is the function $f(\theta)$ — for example, the AUC obtained when training with a given hyperparameter set. See [`skopt.gp_minimize`](https://scikit-optimize.github.io/stable/modules/generated/skopt.gp_minimize.html) and [`Optuna GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html). | It is incorrect to say that "the hyperparameter follows a normal distribution." The right statement is that, given the evaluations already observed, BO builds a predictive distribution over the expected performance of new configurations. |
| Random search is not naive: it is a strong baseline when only a few hyperparameters truly matter    | [Bergstra and Bengio (2012)](https://jmlr.org/papers/v13/bergstra12a.html) show that random search can be more efficient than a grid when only a few dimensions concentrate the relevant variation.                                                                                                                                                                                                       | The fair comparison is not BO versus a huge grid, but BO versus random search with the same evaluation budget. If BO does not beat that baseline, the search space or the surrogate are probably not contributing.                     |
| HPO demands experimental design, not just a library                                                 | [Bischl et al. (2023)](https://arxiv.org/abs/2107.05847) frame the HPO problem as an experimental decision: search space, budget, resampling, metric, overfitting risk and external validation.                                                                                                                                                                                                          | Optimization must first fix the trial budget, the objective metric and the train/validation/test split. In RSH and ecommerce, repeating tuning against the same validation can overfit as much as fitting the model poorly.           |
| BO can save evaluations, but it depends on the surrogate and the acquisition function               | [SMAC3, Lindauer et al. (2022)](https://www.jmlr.org/papers/v23/21-0888.html) shows a robust Bayesian optimization approach for algorithm configuration; [BoTorch, Balandat et al. (2020)](https://arxiv.org/abs/1910.06403) offers a more flexible framework for acquisition, constraints and advanced optimization.                                                                                     | "Using Bayes" is not enough. In mixed, conditional or many-category spaces, TPE/SMAC can be more practical than a plain GP; in advanced problems, BoTorch is more powerful but also more demanding.                                    |
| Expected Improvement is useful, but should not be treated as a closed recipe                         | [Ament et al. (2023)](https://arxiv.org/abs/2310.20708) review numerical issues with EI and propose logEI; other recent work shows that acquisition can misbehave with noise, poor initialization or difficult surfaces.                                                                                                                                                                                  | In noisy validations — CV, temporal validation or small samples — it pays to fix seeds, repeat folds or use less unstable metrics. Acquisition decides where to look next; it does not guarantee statistical truth.                   |
| LLM + BO is an interesting line, not a replacement for validation                                   | [LLAMBO, Liu et al. (2024)](https://arxiv.org/abs/2402.03921), and work on priors or pretrained models for BO such as [HyperBO, Wang et al. (2021)](https://arxiv.org/abs/2109.08215), aim to use prior knowledge to propose better spaces or initial points.                                                                                                                                             | A reasoning model can help define ranges, discard absurd configurations or propose warm starts. But it does not replace holdout, temporal validation, leakage auditing or substantive analysis of the target.                          |


---

## Spoonful 1: two ranking problems, not two predictive toys

I want to use two examples with equal weight. One comes from the public world: ranking households by relative vulnerability using a public RSH sample. The other comes from the private world: ranking customers, sessions or contacts by the expected value of a commercial action in ecommerce.
{: .text-justify}

They are not equivalent in substance. The first has consequences for public legitimacy; the second, for commercial efficiency. But both share the same statistical question: if what matters is ordering cases well, how do we search for hyperparameters that improve that order without spending compute on uninformative combinations?
{: .text-justify}

{: .table-caption}
**Table 2**: Two equivalent exercises to think of HPO as a ranking problem

| Dimension                  | RSH, public sample                                                                                                                                                                                                                                                                                                       | Ecommerce, Shopify style                                                                                                                                                                                                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unit of analysis           | Household                                                                                                                                                                                                                                                                                                                 | Customer, session, customer-campaign or customer-product                                                                                                                                                                                                                                                 |
| Substantive question       | Which households show the highest relative probability of vulnerability, using indirect signals and not income as a predictor?                                                                                                                                                                                            | Which customers or sessions should be prioritized because they concentrate the highest probability of purchase, expected margin or incremental response to a commercial action?                                                                                                                          |
| Source                     | A public, random, anonymized RSH sample available in [BIDAT](https://bidat.gob.cl/details/ficha/dataset/registro-social-de-hogares-muestra-diciembre-2025)                                                                                                                                                                | A proprietary table of browsing, transactions and campaigns: sessions, carts, purchases, margin, discounts, recurrence, stock, channels and devices                                                                                                                                                     |
| Reasonable target          | A vulnerability signal built outside the predictor set. It can be binary, ordinal or continuous: membership in a high-vulnerability group, a later transition to greater vulnerability, an external deprivation index, or a reference bracket used only as a label, not as a predictor.                                    | Two distinct options: propensity to buy or expected value, if there is no experiment; causal uplift, if there is random assignment, a control group or a defensible quasi-experimental design.                                                                                                            |
| What is excluded           | Direct income and variables that are operational copies of income or of the target. The idea is not to mechanically reconstruct the CSE, but to assess how much ordering can be recovered from indirect vulnerability signals.                                                                                            | Post-intervention variables: campaign open if predicting before sending it, the discount actually used if deciding to whom to offer it, the purchase observed within the target window, or any variable contaminated by the outcome.                                                                      |
| Proposed model             | **EBM** with `interpretML`, because it allows reviewing partial functions, plausible monotonicities, odd jumps and interaction effects without entirely losing interpretive control.                                                                                                                                     | **H2O XGBoost**, because it is strong on tabular data, handles non-linearities and interactions, scales well and lets us treat ecommerce as an operational ranking or expected-value problem.                                                                                                            |
| Plausible predictors       | Household size, age composition, presence of children, elderly or dependents, schooling, occupation, employment status, housing tenure, materials, overcrowding, doubling-up, rurality, municipality or aggregated territory, access to services, disability and other indirect socioeconomic signals.                    | Recency, frequency, amount, margin, recent sessions, time since last purchase, categories visited, cart abandonment, browsing depth, historical discount sensitivity, channel, device, acquisition source, stock, seasonality, returns and prior campaign response.                                       |
| What ordering well means    | That, comparing two households, the more vulnerable one according to the reference signal tends to receive a higher score. At the top of the ranking it should concentrate households with greater observed vulnerability, without relying on direct income.                                                              | That the selected top-k concentrates more purchase, margin or incremental effect than random prioritization or a simple business rule. If there is an experiment, the incremental effect matters; if not, one can only speak of propensity or expected value.                                             |
| Main metrics               | AUC if the target is binary and global ranking matters; AUCPR if high vulnerability is a minority; NDCG@k or lift@k if the top segment matters; Kendall or Spearman if the target is ordinal; Brier and calibration curves if the score is interpreted as a probability.                                                  | For propensity: AUCPR, lift@k, gain@k and profit@k. For expected value: RMSE, MAE, pinball loss or margin-weighted error. For causal uplift: uplift@k, Qini and estimated incremental gain on an experimental holdout.                                                                                    |
| Main risk                  | Circularity, information leakage and false legitimacy. A model can order very well because it learned variables nearly equivalent to income or to the target itself. That would be apparently good performance, but bad evidence.                                                                                          | Confusing propensity with causality. The best buyers are not necessarily the most persuadable. A coupon sent to someone who would have bought anyway can raise observed conversions while destroying incremental margin.                                                                                  |

### RSH case: vulnerability ranking without using direct income

The RSH exercise should not be framed as "predicting poverty" or "replicating the CSE." That would close the discussion too quickly and increase the risk of circularity. The cleanest framing is as a problem of **supervised ranking of relative vulnerability**.
{: .text-justify}

The objective function does not only seek to get classes right, but to improve the probability that the order between households is correct. If household $i$ is more vulnerable than household $j$, the model should assign $s_i > s_j$. That score can be calibrated as a probability, but its first analytical use is ordinal: ordering households with the greatest possible stability.
{: .text-justify}

A simple way to write it is:
{: .text-justify}

$$
s_i = f_\theta(X_i), \quad X_i \not\ni income
$$

where $s_i$ is the household's vulnerability score, $X_i$ contains indirect signals and $\theta$ represents the model's hyperparameters. Direct income stays out of $X_i$. Variables that are an administrative copy too close to the target should also be left out.
{: .text-justify}

In an EBM, the score has an important advantage: it can be decomposed into per-variable effects and bounded interactions.
{: .text-justify}

$$
g(E[y_i]) = \beta_0 + \sum_k f_k(x_{ik}) + \sum_{k<l} f_{kl}(x_{ik}, x_{il})
$$

That form does not make the model "fair" by itself, but it makes it easier to audit. If the score rises abruptly at an absurd point of schooling, materials or household composition, the functional form is exposed. Here interpretability is not cosmetic: it is part of the methodological defense of the ranking.
{: .text-justify}

For HPO, an illustrative hyperparameter is <span class="text-nowrap">max_bins</span>. It controls how finely continuous variables are discretized before learning effects. With few bins, the model can smooth too much and lose real differences. With too many bins, it can capture noise, produce artificial jumps and worsen the stability of the order.
{: .text-justify}

The right comparison is not "grid versus Bayes" in the abstract. The relevant comparison is this:
{: .text-justify}

| Strategy      | What it would do with <span class="text-nowrap">max_bins</span>                                                | Problem                                                                                                            |
| ------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Grid          | Would try fixed values, e.g. 32, 64, 128, 256, 512 and 1024.                    | Orderly, but rigid. If the good range is between two values or depends on another hyperparameter, it can look in the wrong place. |
| Random search | Would try random values within a range.                                         | A strong baseline, but it does not explicitly learn from previous results.                                        |
| BO            | Uses the results already observed to decide the next value of <span class="text-nowrap">max_bins</span>. | It does not guarantee the optimum, but it can save evaluations if the surface has exploitable structure.           |

A more realistic bivariate move would be to optimize <span class="text-nowrap">max_bins</span> together with <span class="text-nowrap">interactions</span>. The intuition is clear: more granularity in main variables may demand more caution with interactions. If both are increased without control, the ranking may improve on internal validation and worsen out of sample.
{: .text-justify}

$$
\theta = (\mathrm{max\_bins},\ \mathrm{interactions})
$$

The main objective metric would be **Kendall's tau-b**, because the model's purpose is not only to classify vulnerable households, but to correctly preserve their ordering: that households with greater reference vulnerability systematically receive higher scores than less vulnerable ones. AUCPR can be reported as a complementary metric if high vulnerability is defined as a minority event; NDCG@k, if it is especially of interest to audit the top segment of the ranking; and Brier/calibration, only if the score will be interpreted as a probability. In a more demanding version, beyond global performance, I would require stability by subgroup and territory: a ranking that orders well only in the dominant region or household type is not, in my opinion, ready for public discussion.
{: .text-justify}


### Ecommerce case: operational lift without confusing it with causality

In ecommerce one must separate three models that are often mixed:
{: .text-justify}

1. **Propensity**: probability of future purchase.
2. **Expected value**: expected purchase weighted by amount, margin or conversion probability.
3. **Causal uplift**: increment attributable to an action, e.g. sending a coupon, showing a banner or triggering a recommendation.

If there is no experiment — and here I enter unfamiliar territory for my knowledge — I would not promise causality. I would build a propensity or expected-value model and evaluate it as a commercial ranking. If there is an A/B experiment or a valid control group, then one can speak of more genuine uplift: the question becomes who buys more because they were treated, not simply who was going to buy anyway.
{: .text-justify}

I would use H2O XGBoost with two variants:
{: .text-justify}

| Scenario        | Target                                                              | Metric                                                                       |
| --------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| No experiment   | Future purchase, future margin or expected value at 7, 14 or 30 days | AUCPR, lift@k, gain@k, profit@k, RMSE or MAE if the target is an amount        |
| With experiment | Incremental difference attributable to the treatment               | uplift@k, Qini, incremental gain and validation against an experimental holdout |

In the observational case, a useful score could be:
{: .text-justify}

$$
score_i = \hat{p}_i(\text{purchase}) \times \widehat{margin}_i
$$

That does not measure causality, but it can help prioritize actions if the goal is commercial efficiency. If the cost of contact or discount is known, it is worth optimizing expected profit:
{: .text-justify}

$$
profit_i = \hat{p}_i(\text{purchase}) \times \widehat{margin}_i - cost_i
$$

In H2O XGBoost, an illustrative hyperparameter is <span class="text-nowrap">max_depth</span>. It controls the maximum depth of each tree. With very shallow trees, the model can miss relevant interactions: for example, recurring customers with recent cart abandonment, high discount sensitivity and available stock. With overly deep trees, it can memorize noise from campaigns, seasonality or one-off events.
{: .text-justify}

| Strategy      | What it would do with <span class="text-nowrap">max_depth</span>                                                                                 | Problem                                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Grid          | Would try fixed depths, e.g. 2, 4, 6, 8, 10 and 12.                                                                | Simple, but becomes costly when combined with <span class="text-nowrap">learn_rate</span>, <span class="text-nowrap">min_rows</span>, <span class="text-nowrap">sample_rate</span> and <span class="text-nowrap">col_sample_rate</span>. |
| Random search | Would try random depths and random combinations of other hyperparameters.                                         | A good baseline, especially when only a few dimensions truly matter.                                          |
| BO            | Learns from prior trials which zones produce better lift@k, profit@k or AUCPR, and decides where to try next.      | Depends on the metric being stable and on the validation representing real use of the model.                  |

The natural bivariate move is <span class="text-nowrap">max_depth</span> with <span class="text-nowrap">min_rows</span> or <span class="text-nowrap">learn_rate</span>.
{: .text-justify}

$$
\theta = (\mathrm{max\_depth},\; \mathrm{min\_rows})
$$

The intuition: if deeper trees are allowed, it may be necessary to demand more minimum observations per leaf to avoid overly specific rules. Another frequent pair is <span class="text-nowrap">max_depth</span> with <span class="text-nowrap">learn_rate</span>: more complex trees with high learning rates can overfit quickly; lower rates may need more trees and more time.
{: .text-justify}

That is where BO makes practical sense. Not because "Bayes is better" by definition, but because a Cartesian grid grows fast. If you try 8 depth values, 8 of <span class="text-nowrap">min_rows</span>, 6 of <span class="text-nowrap">learn_rate</span>, 5 of <span class="text-nowrap">sample_rate</span> and 5 of <span class="text-nowrap">col_sample_rate</span>, that is already 9,600 combinations before thinking about cross-validation or temporal windows. Random search reduces the cost; BO tries to reduce it by learning from each evaluation.
{: .text-justify}

The underlying idea for both examples is the same:
{: .text-justify}

$$
\theta^* = \arg\max_{\theta \in \Theta} M(f_\theta, D_{valid})
$$

where $M$ can be AUCPR, NDCG@k, lift@k, profit@k, Qini or a combination penalized by instability. BO does not assume that the hyperparameters follow a normal distribution. In its Gaussian-process version, it models the objective function probabilistically: what performance to expect for a configuration not yet evaluated, given what has already been observed.
{: .text-justify}

The methodological decision is then: random search is the minimum baseline; BO enters when each training run is costly, when the search space is reasonable and when the validation metric represents real use of the model. If those three conditions are not met, BO can produce an elegant optimization over a badly posed question.
{: .text-justify}

## Spoonful 2: the experiment before the algorithm

Hyperparameter optimization, I think, starts by fixing how we will evaluate success. In these two examples, the success contract would have six pieces:
{: .text-justify}

{: .table-caption}
**Table 3**: Minimum contract before doing HPO

| Decision          | What must be fixed                                                          | Why it matters                                                                            |
| ----------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Unit              | Household, customer, session or customer-campaign                            | If the unit changes, the target, the validation and the interpretation of the score change. |
| Target            | Vulnerability signal, future purchase, expected margin or incremental effect | You do not optimize the same thing whether the target is ordinal, binary, monetary or causal. |
| Main metric       | A metric aligned with the decision                                          | The metric must represent real use of the ranking, not just look good on a leaderboard.    |
| Split             | Out-of-sample validation, ideally temporal when appropriate                  | Tuning against a weak validation produces artificial confidence.                           |
| Budget            | Maximum number of training runs                                             | HPO is a decision under a compute constraint, not an infinite search.                      |
| Baseline          | Simple rule and random search                                              | BO must justify its complexity against reasonable alternatives.                            |

The key statistical part is that the observed metric is not the true metric. Each trial delivers a noisy estimate of performance:
{: .text-justify}

$$
\widehat{M}(\theta) = M(\theta) + \varepsilon
$$

That noise appears from splits, folds, event prevalence, sample size, temporal changes, small subgroups and the training's own variation. In RSH it can show up as instability by territory or household type. In ecommerce it can show up as seasonality, simultaneous campaigns, stock changes, discounts or poorly representative validation windows.
{: .text-justify}

That is why, instead of optimizing only a clean metric, it is worth optimizing a penalized metric:
{: .text-justify}

$$
J(\theta) = M(\theta) - \lambda_1 \cdot \text{instability} - \lambda_2 \cdot \text{complexity}
$$

The intuition is simple. A configuration should not win just because it marginally raises the main metric. It should win because it improves the ranking (particularly in RSH/SIVUST, where order is critical), holds out of sample and does not introduce complexity that is hard to defend.
{: .text-justify}

In the RSH case, that function could reward Kendall's tau-b and penalize instability by territory, household composition or relevant subgroups. In ecommerce, it could reward profit@k or lift@k and penalize temporal volatility, excess depth or dependence on a single campaign.
{: .text-justify}

The search space must also be thought through, not just declared. A wide grid may seem neutral, but it actually contains assumptions. Deciding that <span class="text-nowrap">max_depth</span> ranges from 2 to 20, or that <span class="text-nowrap">max_bins</span> can reach 4096, is not innocent. It widens the space, makes the search more expensive and allows configurations that perhaps should never compete.
{: .text-justify}

A practical rule:
{: .text-justify}

{: .table-caption}
**Table 4**: How I would think about the search space

| Hyperparameter type       | Reasonable treatment                          | Example                                                         |
| ------------------------- | --------------------------------------------- | --------------------------------------------------------------- |
| Complexity integers       | Bounded, substantively defensible ranges      | <span class="text-nowrap">max_depth</span>, <span class="text-nowrap">max_bins</span>, <span class="text-nowrap">interactions</span>                         |
| Rates or regularization   | Logarithmic scale                             | <span class="text-nowrap">learn_rate</span>, penalties, regularization                    |
| Sampling                  | Conservative ranges                           | <span class="text-nowrap">sample_rate</span>, <span class="text-nowrap">col_sample_rate</span>                                |
| Conditional parameters    | Activate them only when appropriate           | Interactions only if the base model is already stable           |
| Computational cost        | Log time per trial                            | A slightly better point may not justify tripling the cost       |

Here BO enters, but with a bounded role. It does not define the target, does not fix leakage/circularity ("leakage" 🕶️) and does not decide which error is acceptable. The practical sequence would be:
{: .text-justify}

1. run a simple rule;
2. run random search with a fixed budget;
3. run BO with the same budget;
4. compare not only the best metric, but the learning curve;
5. check stability on test;
6. publish the failed trials too.

The learning curve matters a lot. If BO beats random search only after 300 trials, but the real budget was 30, it did not contribute. If random search reaches a similar result with less complexity, that is also evidence. The question is not which method has the better reputation, but which one delivers the better decision within the available budget.
{: .text-justify}

For this post, I would use **Optuna** as the main orchestrator. Not because it is "more Bayesian" in the abstract, but because it lets you log studies, resume trials, compare samplers and save results (I originally tried other libraries in SAT without success, and kept resorting to artifacts like pickle to fill gaps the library did not cover). The training engine can be H2O XGBoost, EBM or another tabular model; Optuna only needs an objective function that returns a metric.
{: .text-justify}

I would also distinguish three levels of search:
{: .text-justify}

{: .table-caption}
**Table 5**: Three possible levels of search

| Level        | Strategy                      | Reasonable use                                                                    |
| ------------ | ----------------------------- | ---------------------------------------------------------------------------------- |
| Base         | Random search                 | Minimum technical baseline. If BO does not beat it, there is not much to defend.   |
| Intermediate | TPE or GP via Optuna          | A good balance between practicality, traceability and sequential search.           |
| Advanced     | SMAC, BoTorch or multiobjective | Apparently useful when there are constraints, multiple objectives or complex conditional spaces (I HAVE NOT TESTED IT). |

I would not over-defend the Gaussian process. To explain BO it is useful, but in mixed, discrete or conditional spaces, TPE or SMAC seem more practical. In small and relatively smooth problems, GP makes sense. In large problems with categories, conditionality or noise, it is worth comparing. In short, you have to measure how much each evaluation costs and what instability we are unwilling to accept.
{: .text-justify}

---

## Spoonful 3: Alternatives and closing

Instead of BO, or as a complement to it, LLMs can enter as a layer. First, before tuning, to propose reasonable search spaces, detect poorly scaled hyperparameters and suggest constraints. Second, during tuning, to read failed trials and propose adjustments to the space. Third, after tuning, to review consistency: information loss, suspicious variables, metrics that do not match the decision or overly fragile explanations (THIS NEEDS EXPERIMENTATION).
{: .text-justify}

The most interesting flow would be hybrid:
{: .text-justify}

$$
\text{domain knowledge}
\rightarrow
\text{search space}
\rightarrow
\text{random search}
\rightarrow
\text{BO}
\rightarrow
\text{audit}
\rightarrow
\text{redesign}
$$

And, in parallel:
{: .text-justify}

$$
\text{LLM}
\rightarrow
\text{better search hypotheses}
\rightarrow
\text{fewer absurd trials}
$$

The point is not to replace Bayes with LLMs or LLMs with Bayes. The point is for each part to do what it does best. The LLM can help to think, summarize, criticize and propose. BO can better allocate the evaluation budget. Validation, in turn, remains the court.
{: .text-justify}

---

## Closing: an invitation to try with real data

The question I want to leave open is not whether BO is "better" than random search. Framed that way, the question is too broad. The useful question is more concrete:
{: .text-justify}

**with 30 available training runs, which strategy delivers the most stable, defensible and useful ranking?**

In RSH, that means testing whether a transparent model can order relative vulnerability without using direct income (due to the absence or fragility of the direct datum), with auditing by territory and household type. In ecommerce, it means testing whether an optimized tabular model beats a simple business rule on profit@k, lift@k or incremental gain, respecting temporal windows.
{: .text-justify}

Consider a set of strategies:
{: .text-justify}

| Strategy      | Question it answers                                            |
| ------------- | -------------------------------------------------------------- |
| Simple rule   | How much does the model really contribute?                     |
| Random search | How much do you gain with a cheap, honest search?              |
| BO            | How much do you gain by learning from the trial history?       |
| LLM + BO      | How much do you gain if the search space starts better designed? |

If someone works in public policy, I would like to know which indirect signals they use to order their models without falling into circularity. If someone works in ecommerce or another industry, how they define metrics when there is no experiment and how they separate propensity from incremental effect. And if someone already uses LLMs to design hyperparameter searches, I would be happy to read about it 🤩.
{: .text-justify}

Hyperparameter optimization is not the center of the problem. The center is the decision that comes after the ranking. In public policy, a bad ordering can damage legitimacy. In industry, it can destroy margin. In both cases, ordering well matters more than declaring an algorithm the winner.
{: .text-justify}

## References

* Ament, Sebastian; Daulton, Samuel; Eriksson, David; Balandat, Maximilian; Bakshy, Eytan. [Unexpected Improvements to Expected Improvement for Bayesian Optimization](https://arxiv.org/abs/2310.20708), NeurIPS 2023.
* Balandat, Maximilian et al. [BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization](https://arxiv.org/abs/1910.06403), NeurIPS 2020.
* Bergstra, James; Bengio, Yoshua. [Random Search for Hyper-Parameter Optimization](https://jmlr.org/papers/v13/bergstra12a.html), JMLR 2012.
* Bischl, Bernd et al. [Hyperparameter Optimization: Foundations, Algorithms, Best Practices and Open Challenges](https://doi.org/10.1002/widm.1484), WIREs Data Mining and Knowledge Discovery, 2023. Open version on [arXiv](https://arxiv.org/abs/2107.05847).
* Caruana, Rich et al. [Intelligible Models for HealthCare: Predicting Pneumonia Risk and Hospital 30-day Readmission](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/KDD2015FinalDraftIntelligibleModels4HealthCare_igt143e-caruanaA.pdf), KDD 2015.
* H2O.ai. [Grid (Hyperparameter) Search](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/grid-search.html), official documentation.
* H2O.ai. [XGBoost](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/xgboost.html), official documentation.
* InterpretML. [Explainable Boosting Machine](https://interpret.ml/docs/ebm.html) and [Hyperparameters](https://interpret.ml/docs/hyperparameters.html), official documentation.
* Lindauer, Marius; Eggensperger, Katharina; Feurer, Matthias; Biedenkapp, André; Deng, Difan; Benjamins, Carolin; Ruhkopf, Tim; Sass, René; Hutter, Frank. [SMAC3: A Versatile Bayesian Optimization Package for Hyperparameter Optimization](https://www.jmlr.org/papers/v23/21-0888.html), JMLR 2022.
* Liu, Tennison; Astorga, Nicolás; Seedat, Nabeel; van der Schaar, Mihaela. [Large Language Models to Enhance Bayesian Optimization](https://arxiv.org/abs/2402.03921), 2024.
* Ministry of Social Development and Family, BIDAT. [Social Household Registry, December 2025 sample](https://bidat.gob.cl/details/ficha/dataset/registro-social-de-hogares-muestra-diciembre-2025), published on January 30, 2026.
* Optuna. [Optuna: A Hyperparameter Optimization Framework](https://optuna.org/) and [`GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html), official documentation.
* Scikit-Optimize. [`gp_minimize`](https://scikit-optimize.github.io/stable/modules/generated/skopt.gp_minimize.html), official documentation.
* Villagrán Prieto, Nicolás; Garrido-Merchán, Eduardo C. [Default Machine Learning Hyperparameters Do Not Provide Informative Initialization for Bayesian Optimization](https://arxiv.org/abs/2602.08774), 2026, preprint.
* Zhou, Han; Ma, Xingchen; Blaschko, Matthew B. [A Corrected Expected Improvement Acquisition Function Under Noisy Observations](https://arxiv.org/abs/2310.05166), 2023.
