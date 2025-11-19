# Statistical Test Selection Guide

A comprehensive guide to help researchers choose the appropriate statistical test for their study design.

## Table of Contents

1. [Overview](#overview)
2. [Decision Trees](#decision-trees)
3. [Test-by-Test Guide](#test-by-test-guide)
4. [Common Study Designs](#common-study-designs)
5. [Assumptions Checking](#assumptions-checking)
6. [Frequently Asked Questions](#frequently-asked-questions)

## Overview

Choosing the right statistical test is critical for valid study conclusions. The choice depends on:

1. **Type of outcome variable** - Continuous, binary/categorical, or time-to-event
2. **Number of groups** - One, two, or three or more
3. **Independence of observations** - Independent samples or paired/matched data
4. **Distribution assumptions** - Normal distribution or non-parametric
5. **Study objective** - Superiority, non-inferiority, or equivalence

## Decision Trees

### Continuous Outcomes

```
Continuous Outcome
│
├─ One Group
│  ├─ Normally distributed → One-Sample t-test
│  └─ Non-normal → Wilcoxon Signed-Rank Test
│
├─ Two Groups
│  ├─ Paired/Matched
│  │  ├─ Differences normally distributed → Paired t-test
│  │  └─ Non-normal differences → Wilcoxon Signed-Rank Test
│  │
│  └─ Independent
│     ├─ Normal & equal variance → Two-Sample t-test
│     └─ Non-normal or unequal variance → Mann-Whitney U Test
│
└─ Three or More Groups
   ├─ Normal & equal variance → One-Way ANOVA
   └─ Non-normal or unequal variance → Kruskal-Wallis Test
```

### Binary/Categorical Outcomes

```
Binary/Categorical Outcome
│
├─ One Group
│  └─ Compare to fixed proportion → Z-test: Single Proportion
│
└─ Two Groups
   ├─ Large samples (expected counts > 5) → Z-test: Two Proportions
   └─ Small samples (expected counts < 5) → Fisher's Exact Test
```

### Time-to-Event Outcomes

```
Time-to-Event (Survival) Outcome
│
└─ Two Groups
   └─ Compare survival curves → Log-Rank Test
```

## Test-by-Test Guide

### Parametric Tests

#### Two-Sample Independent Groups t-test

**When to use:**
- Comparing means between two independent groups
- Outcome is continuous
- Data approximately normally distributed within each group
- Variances approximately equal between groups

**Example scenarios:**
- Compare blood pressure between treatment and control groups
- Compare test scores between males and females
- Compare weight loss between two diet programs

**Key assumptions:**
1. Independence of observations
2. Normal distribution within each group
3. Homogeneity of variance (equal variances)

**Effect size:** Cohen's d
- Small: 0.2
- Medium: 0.5
- Large: 0.8

**Violations:**
- If normality violated → Use Mann-Whitney U Test
- If equal variance violated → Use Welch's t-test (not yet implemented)

---

#### One-Sample t-test

**When to use:**
- Comparing sample mean to a known/hypothesized value
- Outcome is continuous
- Data approximately normally distributed

**Example scenarios:**
- Is average IQ different from 100?
- Does mean blood glucose differ from normal (100 mg/dL)?
- Is average height different from national average?

**Key assumptions:**
1. Independence of observations
2. Normal distribution of data

**Effect size:** Cohen's d (one-sample)
- Formula: d = |μ - μ₀| / σ

**Violations:**
- If normality violated → Use Wilcoxon Signed-Rank Test

---

#### Paired t-test

**When to use:**
- Comparing means for related/paired samples
- Outcome is continuous
- Differences approximately normally distributed

**Example scenarios:**
- Pre-test vs. post-test measurements
- Before vs. after treatment
- Matched case-control studies
- Measurements on left vs. right (e.g., arms, eyes)

**Key assumptions:**
1. Paired observations
2. Independence of pairs
3. Normal distribution of differences

**Effect size:** Cohen's d_z (paired)
- Formula: d_z = |μ_diff| / σ_diff

**Violations:**
- If normality of differences violated → Use Wilcoxon Signed-Rank Test

---

#### Z-test: Two Independent Proportions

**When to use:**
- Comparing proportions between two independent groups
- Outcome is binary (yes/no, success/failure)
- Large samples with expected cell counts > 5

**Example scenarios:**
- Compare response rates between two treatments
- Compare infection rates between vaccinated vs. unvaccinated
- Compare purchase rates between marketing campaigns

**Key assumptions:**
1. Independence of observations
2. Binary outcome
3. Large sample size (np > 5 and n(1-p) > 5 for each group)

**Effect size:** Cohen's h
- Calculated from arcsine transformation of proportions
- Similar interpretation to Cohen's d

**Violations:**
- If small sample size → Use Fisher's Exact Test

---

#### Z-test: Single Proportion

**When to use:**
- Comparing observed proportion to a hypothesized value
- Outcome is binary
- Large sample size

**Example scenarios:**
- Is response rate different from 50%?
- Does cure rate exceed historical rate of 70%?
- Is defect rate below 5%?

**Key assumptions:**
1. Independence of observations
2. Binary outcome
3. Large sample size (np₀ > 5 and n(1-p₀) > 5)

**Effect size:** Cohen's h
- Based on difference between observed and null proportions

**Violations:**
- If small sample size → Use exact binomial test (not implemented)

---

#### One-Way ANOVA (Between Subjects)

**When to use:**
- Comparing means across 3 or more independent groups
- Outcome is continuous
- Data approximately normally distributed within each group
- Variances approximately equal across groups

**Example scenarios:**
- Compare pain scores across 3 pain medications
- Compare crop yield across 4 fertilizer types
- Compare satisfaction scores across multiple service locations

**Key assumptions:**
1. Independence of observations
2. Normal distribution within each group
3. Homogeneity of variance across groups

**Effect size:** Cohen's f
- Small: 0.10
- Medium: 0.25
- Large: 0.40

**Violations:**
- If normality violated → Use Kruskal-Wallis Test
- If unequal variances → Use Welch's ANOVA (not implemented)

### Non-Parametric Tests

#### Mann-Whitney U Test

**When to use:**
- Non-parametric alternative to two-sample t-test
- Comparing distributions between two independent groups
- Outcome is ordinal or continuous
- Does not assume normal distribution

**Example scenarios:**
- Compare pain scores (1-10 scale) between groups
- Compare Likert scale responses
- Compare continuous data with outliers or skewed distribution

**Key assumptions:**
1. Independence of observations
2. Ordinal or continuous data
3. Similar distribution shapes for median comparison

**Power calculation:**
- Uses ARE (Asymptotic Relative Efficiency) approximation
- ARE ≈ 0.955 relative to t-test for normal data
- Less powerful than t-test when normality holds
- More powerful than t-test when normality violated

---

#### Wilcoxon Signed-Rank Test

**When to use:**
- Non-parametric alternative to paired t-test or one-sample t-test
- Paired/matched samples or single sample
- Does not assume normal distribution
- Symmetric distribution around median

**Example scenarios:**
- Pre-post measurements with skewed data
- Matched case-control with ordinal outcomes
- Testing if median differs from hypothesized value

**Key assumptions:**
1. Paired data (or single sample)
2. Independence of pairs
3. Symmetric distribution of differences around median

**Power calculation:**
- Uses ARE approximation (≈ 0.955)

---

#### Kruskal-Wallis Test

**When to use:**
- Non-parametric alternative to one-way ANOVA
- Comparing distributions across 3+ independent groups
- Ordinal or continuous data
- Does not assume normal distribution

**Example scenarios:**
- Compare Likert scale responses across multiple groups
- Compare outcomes with skewed distributions
- Ordinal data across multiple categories

**Key assumptions:**
1. Independence of observations
2. Ordinal or continuous data
3. Similar distribution shapes across groups

**Power calculation:**
- Uses ARE approximation (≈ 0.955)

---

#### Fisher's Exact Test

**When to use:**
- Exact test for 2×2 contingency tables
- Small sample sizes where normal approximation unreliable
- Binary outcome, two groups
- Expected cell counts < 5

**Example scenarios:**
- Compare outcomes in small clinical trials
- Rare events
- Small pilot studies

**Key assumptions:**
1. Independence of observations
2. Binary outcome
3. Fixed row and column margins (in exact test)

**Power calculation:**
- Uses z-test approximation with heuristic adjustments
- Less accurate than simulation-based approaches

### Survival Analysis

#### Log-Rank Test

**When to use:**
- Comparing survival curves between two groups
- Time-to-event outcomes with censoring
- Proportional hazards assumption reasonable

**Example scenarios:**
- Compare time to death between treatments
- Compare time to disease progression
- Compare time to device failure
- Compare time to cure/remission

**Key assumptions:**
1. Independence of observations
2. Non-informative censoring
3. Proportional hazards (hazard ratio constant over time)
4. Similar censoring patterns between groups

**Effect size:** Hazard Ratio (HR)
- HR = 1: No difference
- HR < 1: Reduced hazard (better survival) in Group 1
- HR > 1: Increased hazard (worse survival) in Group 1
- Small effect: HR = 0.80 (20% reduction)
- Medium effect: HR = 0.65 (35% reduction)
- Large effect: HR = 0.50 (50% reduction)

**Power calculation:**
- Based on Schoenfeld's formula
- Requires estimate of event probability
- Sample size depends on number of events needed

**When proportional hazards violated:**
- Consider stratified log-rank test
- Use weighted log-rank tests
- Consider time-varying covariates approach

## Common Study Designs

### Parallel Group Randomized Trial

**Design:** Participants randomized to treatment or control, measured once

**Test choices:**
- Continuous outcome, normal: Two-sample t-test
- Continuous outcome, non-normal: Mann-Whitney U
- Binary outcome, large N: Z-test for proportions
- Binary outcome, small N: Fisher's exact
- Time-to-event: Log-rank test

### Crossover Trial

**Design:** Each participant receives both treatments in random order

**Test choice:** Paired t-test (or Wilcoxon if non-normal)
- Analyzes difference between treatments within each person
- More powerful than parallel design
- Requires washout period

### Pre-Post Design

**Design:** Measure outcome before and after intervention

**Test choice:** Paired t-test (or Wilcoxon if non-normal)
- No control group (weaker design)
- Cannot rule out time effects
- Consider adding control group if possible

### Dose-Response Study

**Design:** Multiple dose levels compared

**Test choice:** One-way ANOVA (or Kruskal-Wallis)
- Can also use trend tests
- Consider linear regression for continuous dose

## Assumptions Checking

### Normality

**Why it matters:**
- Required for t-tests and ANOVA
- Violations can inflate Type I error or reduce power

**How to check:**
1. **Visual inspection:**
   - Histogram - should be bell-shaped
   - Q-Q plot - points should fall on line
   - Box plot - symmetric, few outliers

2. **Statistical tests:**
   - Shapiro-Wilk test (N < 50)
   - Kolmogorov-Smirnov test (N > 50)
   - Anderson-Darling test

3. **Sample size considerations:**
   - With N > 30, t-tests robust to moderate violations (Central Limit Theorem)
   - With N < 15, need stricter normality
   - ANOVA more robust with equal group sizes

**If violated:**
- Transform data (log, sqrt)
- Use non-parametric alternative
- Use bootstrap methods

### Equal Variance (Homoscedasticity)

**Why it matters:**
- Required for standard t-test and ANOVA
- Violations can affect Type I error rate

**How to check:**
1. **Visual inspection:**
   - Side-by-side box plots - similar spread
   - Residual plots - constant spread

2. **Statistical tests:**
   - Levene's test
   - Bartlett's test (sensitive to non-normality)
   - F-test for two groups

3. **Rule of thumb:**
   - If largest SD < 2 × smallest SD, usually acceptable

**If violated:**
- Use Welch's t-test (not in current tool)
- Use non-parametric alternative
- Transform data

### Independence

**Why it matters:**
- Fundamental assumption for all tests
- Violations severely compromise validity

**Common violations:**
- Cluster/hierarchical data (patients within clinics)
- Repeated measures on same subject
- Time series/autocorrelation
- Matched/paired data analyzed as independent

**How to address:**
- Use appropriate design (paired vs. independent)
- Use mixed models for hierarchical data
- Use repeated measures ANOVA
- Account for clustering in design

## Frequently Asked Questions

### When should I use parametric vs. non-parametric tests?

**Use parametric when:**
- Data meet assumptions (normality, equal variance)
- Sample size moderate to large (N > 30)
- Want most powerful test
- Need to estimate parameters (means, differences)

**Use non-parametric when:**
- Data clearly non-normal (skewed, heavy-tailed)
- Small sample size with uncertain distribution
- Ordinal data (Likert scales)
- Outliers present that shouldn't be removed
- Robust analysis preferred

### How do I determine effect size for my study?

**Sources:**
1. **Pilot data** - Most reliable if available
2. **Literature** - Similar published studies
3. **Minimum clinically important difference** - Smallest effect that matters
4. **Benchmarks** - Cohen's small/medium/large as last resort

**Be realistic:**
- Large effects (d = 0.8) are rare
- Most interventions show small to medium effects
- Overestimating effect size → underpowered study

### What power should I aim for?

**Standard:** 80% (β = 0.20)
- Balances Type I and Type II error
- Conventional in most fields

**Higher power (90%):**
- Expensive or difficult-to-recruit populations
- High consequences of false negative
- Regulatory requirements

**Lower power (70%):**
- Exploratory/pilot studies only
- Not recommended for confirmatory studies

### Should I adjust for multiple comparisons?

**When necessary:**
- Multiple primary outcomes
- Multiple treatment groups
- Interim analyses

**Methods:**
- Bonferroni: α/m (conservative)
- Holm-Bonferroni: Sequential Bonferroni
- False Discovery Rate (FDR)

**In power analysis:**
- Use adjusted α level
- Or power for individual tests, then adjust

### What if my data violate assumptions after collection?

**Options:**
1. **Transform data** - Log, sqrt, Box-Cox
2. **Use robust methods** - Welch's t-test, robust regression
3. **Use non-parametric tests** - May lose power
4. **Bootstrap/permutation tests**
5. **Report both** - Parametric and non-parametric if similar

### How do I handle unequal group sizes?

**In design:**
- Can be intentional (cost, availability)
- Use sample size ratio in calculator
- Optimal ratio: √(c₁/c₂) where c = cost per subject

**In analysis:**
- Most tests handle unequal N
- ANOVA more robust with equal N
- Mann-Whitney not affected

### What about dropout/missing data?

**In planning:**
- Add expected dropout to sample size
- Common rates: 10-20% for trials
- Higher for longer studies

**Types:**
- MCAR (Missing Completely at Random) - least problematic
- MAR (Missing at Random) - requires assumptions
- MNAR (Missing Not at Random) - most problematic

**Mitigation:**
- Minimize dropout through design
- Intention-to-treat analysis
- Multiple imputation if needed

### How precise should my effect size estimate be?

**Reality:**
- Exact effect size unknown before study
- Power analysis requires "best guess"
- Sensitivity analyses recommended

**Approach:**
- Calculate sample size for range of effect sizes
- Report power curve
- Consider adaptive designs for confirmatory trials

### Should I use one-sided or two-sided tests?

**Two-sided (recommended):**
- Default choice
- Tests for difference in either direction
- More conservative
- Required by most regulatory agencies

**One-sided:**
- Only when direction pre-specified
- Non-inferiority/equivalence trials
- Stronger theoretical justification needed
- Requires pre-specification in protocol

### What about equivalence and non-inferiority?

**Non-inferiority:**
- Show new treatment "not worse" than standard
- Requires pre-specified margin
- One-sided test typically used
- Larger sample size than superiority

**Equivalence:**
- Show treatments "not different" within margin
- Two one-sided tests (TOST)
- Requires two pre-specified margins
- Even larger sample size

**Key:**
- Margin must be clinically justified
- Cannot be determined from power calculator alone

## Additional Resources

### Recommended Reading

1. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.)
2. Hulley, S.B., et al. (2013). *Designing Clinical Research* (4th ed.)
3. Friedman, L.M., et al. (2015). *Fundamentals of Clinical Trials* (5th ed.)

### Online Resources

- FDA Guidance on Statistical Principles for Clinical Trials
- ICH E9 Guidelines
- CONSORT Statement (reporting guidelines)

### When to Consult a Statistician

**Required:**
- Regulatory submissions
- Confirmatory clinical trials
- Complex designs (adaptive, cluster, crossover)
- Novel methods

**Recommended:**
- Grant applications
- Study protocol development
- Sample size justification
- Data analysis plan

---

**Remember:** This guide provides general recommendations. Your specific study may have unique considerations requiring statistical consultation.
