# Power and Sample Size Calculator

A comprehensive web-based statistical power analysis and sample size calculator designed for pharmaceutical, medical device, and clinical research. Built with Streamlit, this tool makes power analysis accessible to researchers with varying levels of statistical expertise.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

### Statistical Tests Supported

#### Parametric Tests
- **Two-Sample Independent Groups t-test** - Compare means between two independent groups
- **One-Sample t-test** - Compare sample mean to a hypothesized value
- **Paired t-test** - Compare means for related samples (pre/post, matched pairs)
- **Z-test: Two Independent Proportions** - Compare proportions between two groups
- **Z-test: Single Proportion** - Compare observed proportion to hypothesized value
- **One-Way ANOVA (Between Subjects)** - Compare means across 3+ independent groups

#### Non-Parametric Tests (Approximations)
- **Mann-Whitney U Test** - Non-parametric alternative to two-sample t-test
- **Wilcoxon Signed-Rank Test** - Non-parametric alternative to paired/one-sample t-test
- **Kruskal-Wallis Test** - Non-parametric alternative to one-way ANOVA
- **Fisher's Exact Test** - Exact test for 2×2 contingency tables

#### Survival Analysis
- **Log-Rank Test** - Compare survival curves between two groups (time-to-event data)

### Calculation Modes

Calculate any one of:
1. **Sample Size (N)** - Determine required sample size given power and effect size
2. **Statistical Power (1-β)** - Determine power given sample size and effect size
3. **Minimum Detectable Effect Size (MDES)** - Determine smallest effect detectable given sample size and power

### Key Capabilities

- **Interactive Test Selection Guide** - Wizard-based approach to choosing the right test
- **Multiple Effect Size Input Methods** - Use standardized metrics (Cohen's d, f, h, HR) or raw values
- **Study Objectives Support** - Superiority, Non-Inferiority, and Equivalence trials
- **Dropout Adjustment** - Adjust sample sizes for anticipated participant dropout
- **Comprehensive Documentation** - Built-in explanations, assumptions, and citations
- **Expected Count Validation** - Warnings for small sample sizes in proportion tests
- **Summary Tables** - Detailed parameter summaries for reproducibility

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/tpcopeland/Power_Sample_Calc.git
cd Power_Sample_Calc
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Requirements

```
streamlit>=1.28.0
numpy>=1.24.0
scipy>=1.10.0
statsmodels>=0.14.0
pandas>=1.5.0
```

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run power_sample_calc.py
```

The application will open in your default web browser, typically at `http://localhost:8501`.

### Basic Workflow

1. **Choose Your Test**
   - Use the **Test Selection Guide** (checkbox in sidebar) for interactive help
   - Or manually select from **Test Category** and **Specific Test** dropdowns

2. **Configure Parameters**
   - Select what to calculate: Sample Size, Power, or MDES
   - Set significance level (α), typically 0.05
   - Set desired power (1-β), typically 0.80
   - Choose study objective: Superiority, Non-Inferiority, or Equivalence
   - Select alternative hypothesis: Two-sided or One-sided

3. **Specify Effect Size**
   - Use **standardized benchmarks** (Small/Medium/Large)
   - Or enter **custom standardized** values
   - Or specify **raw values** (means, SDs, proportions, etc.)

4. **View Results**
   - Calculated sample sizes (with group breakdowns)
   - Dropout-adjusted sample sizes (if applicable)
   - Summary table of all input parameters

## Examples

### Example 1: Two-Sample t-test for Sample Size

**Scenario:** Comparing mean blood pressure between treatment and control groups.

**Parameters:**
- Test: Two-Sample Independent Groups t-test
- Calculate: Sample Size
- α = 0.05 (two-sided)
- Power = 0.80
- Effect size: Cohen's d = 0.5 (medium)
- Sample size ratio: 1:1

**Result:** ~64 participants per group (128 total)

**With 20% dropout:** ~80 participants per group (160 total)

### Example 2: Single Proportion Test for Power

**Scenario:** Testing if response rate exceeds 50%.

**Parameters:**
- Test: Z-test: Single Proportion
- Calculate: Power
- α = 0.05 (one-sided, larger)
- Sample size: N = 100
- Null proportion: 0.50
- Expected proportion: 0.65

**Result:** Power ≈ 0.92 (92% chance of detecting the effect)

### Example 3: Log-Rank Test for Survival Analysis

**Scenario:** Comparing survival between new drug vs. standard treatment.

**Parameters:**
- Test: Log-Rank Test
- Calculate: Sample Size
- α = 0.05 (two-sided)
- Power = 0.80
- Hazard ratio: 0.65 (35% reduction in hazard)
- Event probability: 0.50 (50% of participants expected to have event)
- Sample size ratio: 1:1

**Result:** ~169 participants per group (338 total)

**Note:** Higher event rates reduce required sample sizes (e.g., with 70% event rate: ~121 per group)

## Effect Size Guidelines

### Cohen's d (t-tests)
- **Small:** 0.2 - Subtle difference
- **Medium:** 0.5 - Moderate difference
- **Large:** 0.8 - Substantial difference

### Cohen's f (ANOVA)
- **Small:** 0.10
- **Medium:** 0.25
- **Large:** 0.40

### Cohen's h (Proportions)
- Calculated from proportion differences
- Similar interpretation to Cohen's d

### Hazard Ratio (Survival)
- **HR = 1.0:** No difference between groups
- **HR < 1.0:** Reduced hazard (better survival) in Group 1
- **HR > 1.0:** Increased hazard (worse survival) in Group 1
- **HR = 0.80:** 20% hazard reduction (small effect)
- **HR = 0.65:** 35% hazard reduction (medium effect)
- **HR = 0.50:** 50% hazard reduction (large effect)

## Statistical Methods

### Parametric Tests
- Calculations use `statsmodels.stats.power` classes
- Based on non-central t, F, and normal distributions
- Exact calculations (not approximations)

### Non-Parametric Tests
- **Mann-Whitney, Wilcoxon, Kruskal-Wallis:** USE ARE (Asymptotic Relative Efficiency) adjustments
  - ARE ≈ 0.955 for normal data
  - Sample sizes adjusted by 1/ARE factor
- **Fisher's Exact:** Uses z-test with heuristic adjustments
  - Sample size increased by 5%
  - Power decreased by 5%

### Survival Analysis
- **Log-Rank Test:** Uses Schoenfeld's formula
  - Calculates required events: d = (z_α + z_β)² / log(HR)²
  - Converts to sample size based on event probability
  - Assumes proportional hazards

## Understanding the Results

### Sample Size Results
- **N₁, N₂:** Sample sizes for each group
- **Total N:** Combined sample size across all groups
- **Adjusted N:** Sample size accounting for dropout rate

### Power Results
- Probability (0-1) of detecting the specified effect
- Convention: 0.80 (80%) is minimum acceptable
- Higher power reduces Type II error (false negative)

### MDES Results
- Smallest standardized effect detectable
- Given fixed sample size and power
- Helps assess study sensitivity

## Tips for Researchers

### Choosing Sample Size
1. **Start with power = 0.80** - Standard in most fields
2. **Use α = 0.05** - Conventional significance level
3. **Be realistic about effect sizes** - Don't assume large effects
4. **Account for dropout** - 10-20% is common in clinical trials
5. **Round up** - Always use conservative (larger) estimates

### Choosing Effect Size
1. **Pilot studies** - Use observed effects as estimates
2. **Literature review** - Look for similar published studies
3. **Clinical significance** - What difference matters to patients?
4. **Resource constraints** - Balance desired sensitivity with feasibility

### Study Design Considerations
1. **Unequal groups** - Adjust sample size ratio if groups differ in cost/availability
2. **Multiple comparisons** - Consider Bonferroni correction for multiple tests
3. **Interim analyses** - May require adjusted α levels
4. **Non-inferiority/Equivalence** - Requires careful margin specification

## Limitations

### Non-Parametric Tests
- Approximations may be less accurate for small samples (N < 20)
- Actual power may differ from estimates
- Consider simulation studies for critical applications

### Survival Analysis
- Assumes proportional hazards throughout follow-up
- Event probability estimates can be uncertain
- Censoring patterns must be non-informative
- Does not account for competing risks

### General
- Assumes assumptions of each test are met
- Does not account for missing data patterns
- Does not handle complex designs (clustering, stratification)
- Results should be reviewed by a statistician for critical studies

## Technical Details

### Architecture
- Single-file Streamlit application (987 lines)
- Modular function-based design
- Session state management for interactivity

### Dependencies
- **statsmodels:** Statistical power calculations
- **scipy:** Distribution functions, hypothesis tests
- **numpy:** Numerical operations
- **pandas:** Data display
- **streamlit:** Web interface

### Browser Compatibility
Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Citation

If you use this calculator in your research, please cite:

```
Copeland, T.P. (2025). Power and Sample Size Calculator (Version 1.1) [Software].
Available from: https://github.com/tpcopeland/Power_Sample_Calc
```

### References

- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.
- Schoenfeld, D. (1981). The asymptotic properties of nonparametric tests for comparing survival distributions. *Biometrika, 68*(1), 316-319.
- ICH E9 (1998). Statistical Principles for Clinical Trials. International Conference on Harmonisation.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Support

For questions, issues, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/tpcopeland/Power_Sample_Calc/issues)
- Email: [contact via GitHub profile]

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and research purposes. While calculations are based on established statistical methods, results should be validated by a qualified statistician before being used for critical study design decisions. The authors assume no liability for decisions made based on this tool's output.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Statistical calculations powered by [statsmodels](https://www.statsmodels.org/)
- Inspired by the need for accessible power analysis tools in clinical research

---

**Version:** 1.3
**Author:** Timothy P. Copeland
**Location:** Geneva, Switzerland
**Year:** 2025
**Website:** https://tcope.land
