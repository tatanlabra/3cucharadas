### Several dwellings on one site: another explanation worth testing

Two dwellings can share a plot and be covered by one property-tax record. The Census would then count two dwellings without a property necessarily being absent from the tax register. This mechanism may contribute to the difference; measuring its contribution requires linking **dwellings, sites and property records**. The public dictionary examined and the [Census microdata manual, pp. 17–20][ine-manual], link dwellings, households and people, but do not provide a shared site or property-record identifier for this reconciliation. Several households within one dwelling are not the same as several dwellings on one site.

CASEN 2024 provides a narrower signal. Categories 3 and 4 of its tenure question identify households reporting **an owned site shared with other dwellings**, either fully paid or being paid for. They do not ask how many dwellings occupy the site. I calculate their share among **all households with valid answers**, including renters and other tenure arrangements, using one household head per household. The principal-household question is conditional; applying it as a filter to the entire dataset would incorrectly remove households in single-household dwellings. See the [official questionnaire, pp. 79 and 83][casen-cuestionario].

The national result is **1.09% of households**, with an approximate 95% interval of **0.97% to 1.21%**. It comes from 78,654 sampled households, with no missing answers to this question. National and regional estimates use `expr` and Taylor linearization with strata and clusters; the interval expresses sampling uncertainty, rather than every possible measurement error. The [official CASEN data-use note][casen-nota] distinguishes these domains from descriptive use at commune level.

<!-- CASEN_FIGURE_AND_TABLE -->

Valparaíso and Viña del Mar show **9.27% and 8.60%**, respectively, in the commune calculation weighted by `expc`. These are exploratory signals: I selected the two communes after observing their discrepancy, and these results **are not representative estimates for each commune**. A commune weight does not confer that property. The table retains sample sizes and missingness; the eleven communes outside the sample are recorded as missing data, never zero.

The deduction is limited but useful: dwelling and property-record counts may differ even with an accurate register. The observed pattern in these two communes makes shared sites worth investigating. The hypothesis is that they explain part of the discrepancy, alongside informal settlements, agricultural land uses, timing and possible omissions. A representative sample linking dwellings to sites and property records would discriminate between these explanations; the hypothesis would weaken as a material explanation if this linkage showed a small contribution against a criterion set before measurement.

**I do not subtract this percentage from the bars or monetary scenarios.** It describes household tenure, not the share of excess dwellings in a count. It also misses other ways of sharing sites and may overlap with informal settlements. Subtracting it now would introduce apparent precision and could count the same explanation twice.
{: .notice--info}

<details markdown="1">
<summary>Why the CASEN percentage cannot directly become dwellings per site</summary>

In a purely hypothetical example, if a share $$p_v$$ of **dwellings** belonged to sites with exactly two dwellings and all remaining dwellings occupied individual sites, there would be $$V(1-p_v/2)$$ sites. The property-records/sites ratio would be $$R_2=R_1/(1-p_v/2)$$, where $$R_1=\text{property records}/V$$. For example, an assumed $$p_v=0.20$$ would mean 90 sites for every 100 dwellings. The CASEN **household** share is not that parameter: the formula illustrates the mechanism but does not estimate a fiscal adjustment.

</details>
