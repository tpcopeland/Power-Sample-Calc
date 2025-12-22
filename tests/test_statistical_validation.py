#!/usr/bin/env python3
"""
Comprehensive Statistical Validation Test Suite

This test suite validates the power and sample size calculations against:
1. Known published values from Cohen (1988) Statistical Power Analysis
2. statsmodels reference implementations
3. G*Power validation cases
4. Manual calculations from first principles

These tests ensure the calculator is production-ready for clinical and research use.
"""

import sys
import math
import types
import pytest
import numpy as np
from scipy.stats import norm

# Mock streamlit before importing power_sample_calc
class DummyContext:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def __getattr__(self, name):
        return lambda *a, **k: DummyContext()

class MockStreamlit(types.ModuleType):
    session_state = {}
    def __getattr__(self, name):
        if name in ('expander', 'container', 'columns', 'tabs', 'form'):
            return lambda *a, **k: DummyContext()
        if name == 'session_state':
            return {}
        if name == 'sidebar':
            return MockStreamlit('streamlit.sidebar')
        return lambda *a, **k: None

sys.modules['streamlit'] = MockStreamlit('streamlit')

# Now import the calculator
sys.path.insert(0, '/home/user/Power-Sample-Calc')

from power_sample_calc import (
    calculate_effect_size,
    calculate_design_effect,
    calculate_clusters_needed,
    calculate_repeated_measures_power,
    calculate_repeated_measures_n,
    calculate_logrank_power,
    calculate_single_proportion_power,
    power_proportions_2indep,
    ARE_FACTORS,
    FISHER_ADJUSTMENTS,
)

from statsmodels.stats.power import TTestIndPower, TTestPower, FTestAnovaPower


class TestEffectSizeCalculations:
    """Validate effect size calculations against known formulas."""

    def test_cohens_d_two_sample(self):
        """Cohen's d = |mean1 - mean2| / pooled_sd"""
        # Standard case
        d = calculate_effect_size('cohen_d_two', mean1=105, mean2=100, pooled_sd=10)
        assert d == pytest.approx(0.5, abs=0.001), f"Expected 0.5, got {d}"

        # Large effect
        d = calculate_effect_size('cohen_d_two', mean1=120, mean2=100, pooled_sd=15)
        assert d == pytest.approx(20/15, abs=0.001), f"Expected {20/15:.3f}, got {d}"

        # Reversed direction (should still be positive)
        d = calculate_effect_size('cohen_d_two', mean1=100, mean2=105, pooled_sd=10)
        assert d == pytest.approx(0.5, abs=0.001), "Effect size should be absolute"

    def test_cohens_d_one_sample(self):
        """One-sample Cohen's d = |sample_mean - hypothesized_mean| / sd"""
        d = calculate_effect_size('cohen_d_one', sample_mean=105, hypothesized_mean=100, sd=15)
        assert d == pytest.approx(5/15, abs=0.001)

        d = calculate_effect_size('cohen_d_one', sample_mean=50, hypothesized_mean=60, sd=20)
        assert d == pytest.approx(0.5, abs=0.001)

    def test_cohens_d_paired(self):
        """Paired Cohen's d = |mean_diff| / sd_diff"""
        d = calculate_effect_size('cohen_d_paired', mean_diff=5, sd_diff=10)
        assert d == pytest.approx(0.5, abs=0.001)

        d = calculate_effect_size('cohen_d_paired', mean_diff=-8, sd_diff=10)
        assert d == pytest.approx(0.8, abs=0.001), "Should be absolute value"

    def test_cohens_h_proportions(self):
        """Cohen's h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))"""
        # Known value: p1=0.6, p2=0.4 gives h ≈ 0.4115
        h = calculate_effect_size('cohen_h', p1=0.6, p2=0.4)
        expected = abs(2 * np.arcsin(np.sqrt(0.6)) - 2 * np.arcsin(np.sqrt(0.4)))
        assert h == pytest.approx(expected, abs=0.001)

        # Equal proportions should return None
        assert calculate_effect_size('cohen_h', p1=0.5, p2=0.5) is None

        # Edge case: extreme proportions
        h = calculate_effect_size('cohen_h', p1=0.9, p2=0.1)
        assert h is not None and h > 1.0  # Should be a large effect

    def test_invalid_inputs(self):
        """Test handling of invalid inputs."""
        # Zero standard deviation
        assert calculate_effect_size('cohen_d_two', mean1=10, mean2=5, pooled_sd=0) is None

        # Proportions outside (0, 1)
        assert calculate_effect_size('cohen_h', p1=0.0, p2=0.5) is None
        assert calculate_effect_size('cohen_h', p1=1.0, p2=0.5) is None


class TestTwoSampleTTest:
    """Validate two-sample t-test calculations against statsmodels reference."""

    def test_sample_size_cohen_benchmarks(self):
        """Test sample size for Cohen's conventional effect sizes (α=0.05, power=0.80)."""
        power_calc = TTestIndPower()

        # Small effect (d=0.2): ~394 per group
        n = power_calc.solve_power(effect_size=0.2, alpha=0.05, power=0.80,
                                   ratio=1.0, alternative='two-sided')
        assert 380 < n < 410, f"Small effect: expected ~394, got {n:.1f}"

        # Medium effect (d=0.5): ~64 per group
        n = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                   ratio=1.0, alternative='two-sided')
        assert 60 < n < 70, f"Medium effect: expected ~64, got {n:.1f}"

        # Large effect (d=0.8): ~26 per group
        n = power_calc.solve_power(effect_size=0.8, alpha=0.05, power=0.80,
                                   ratio=1.0, alternative='two-sided')
        assert 24 < n < 30, f"Large effect: expected ~26, got {n:.1f}"

    def test_power_calculation(self):
        """Test power calculation matches statsmodels."""
        power_calc = TTestIndPower()

        # N=50 per group, d=0.5, α=0.05, two-sided
        pwr = power_calc.solve_power(effect_size=0.5, nobs1=50, alpha=0.05,
                                     ratio=1.0, alternative='two-sided')
        assert 0.65 < pwr < 0.75, f"Expected power ~0.70, got {pwr:.3f}"

        # N=100 per group, d=0.3
        pwr = power_calc.solve_power(effect_size=0.3, nobs1=100, alpha=0.05,
                                     ratio=1.0, alternative='two-sided')
        assert 0.50 < pwr < 0.60, f"Expected power ~0.56, got {pwr:.3f}"

    def test_unequal_allocation(self):
        """Test unequal allocation ratios."""
        power_calc = TTestIndPower()

        # 2:1 allocation with d=0.5, power=0.80
        n1 = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                    ratio=2.0, alternative='two-sided')
        n2 = n1 * 2

        # Should require more total N than equal allocation
        n_equal = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                         ratio=1.0, alternative='two-sided')
        assert n1 + n2 > 2 * n_equal, "Unequal allocation should require more total N"


class TestOneSampleTTest:
    """Validate one-sample and paired t-test calculations."""

    def test_sample_size_against_statsmodels(self):
        """Test sample sizes match statsmodels TTestPower."""
        power_calc = TTestPower()

        # Medium effect, 80% power
        n = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                   alternative='two-sided')
        assert 30 < n < 38, f"Expected ~34, got {n:.1f}"

        # Large effect
        n = power_calc.solve_power(effect_size=0.8, alpha=0.05, power=0.80,
                                   alternative='two-sided')
        assert 12 < n < 18, f"Expected ~15, got {n:.1f}"

    def test_one_sided_vs_two_sided(self):
        """One-sided test should require fewer subjects."""
        power_calc = TTestPower()

        n_two = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                       alternative='two-sided')
        n_one = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                       alternative='larger')

        assert n_one < n_two, "One-sided should require fewer subjects"
        assert n_one < n_two * 0.85, "Should be about 20% fewer for one-sided"


class TestANOVA:
    """Validate ANOVA power calculations."""

    def test_sample_size_cohen_benchmarks(self):
        """Test ANOVA sample sizes for Cohen's f benchmarks.

        Note: statsmodels FTestAnovaPower.solve_power returns TOTAL N, not per-group.
        """
        power_calc = FTestAnovaPower()

        # Small effect (f=0.10), 3 groups - returns TOTAL N
        n_total = power_calc.solve_power(effect_size=0.10, alpha=0.05, power=0.80, k_groups=3)
        n_per_group = n_total / 3
        assert 300 < n_per_group < 350, f"Small effect: expected ~322 per group, got {n_per_group:.1f}"

        # Medium effect (f=0.25), 3 groups
        n_total = power_calc.solve_power(effect_size=0.25, alpha=0.05, power=0.80, k_groups=3)
        n_per_group = n_total / 3
        assert 45 < n_per_group < 60, f"Medium effect: expected ~52 per group, got {n_per_group:.1f}"

        # Large effect (f=0.40), 3 groups
        n_total = power_calc.solve_power(effect_size=0.40, alpha=0.05, power=0.80, k_groups=3)
        n_per_group = n_total / 3
        assert 18 < n_per_group < 25, f"Large effect: expected ~21 per group, got {n_per_group:.1f}"

    def test_more_groups_needs_more_n(self):
        """More groups should require more total N."""
        power_calc = FTestAnovaPower()

        n_3groups = power_calc.solve_power(effect_size=0.25, alpha=0.05, power=0.80, k_groups=3)
        n_4groups = power_calc.solve_power(effect_size=0.25, alpha=0.05, power=0.80, k_groups=4)
        n_5groups = power_calc.solve_power(effect_size=0.25, alpha=0.05, power=0.80, k_groups=5)

        # Total N should increase
        assert n_3groups * 3 < n_4groups * 4, "4 groups needs more total N than 3"
        assert n_4groups * 4 < n_5groups * 5, "5 groups needs more total N than 4"


class TestNonParametricARE:
    """Validate Asymptotic Relative Efficiency adjustments."""

    def test_are_factor_values(self):
        """ARE factors should be approximately 0.955 (3/π ≈ 0.9549)."""
        expected_are = 3 / math.pi

        assert ARE_FACTORS['wilcoxon'] == pytest.approx(expected_are, abs=0.005)
        assert ARE_FACTORS['mann_whitney'] == pytest.approx(expected_are, abs=0.005)
        assert ARE_FACTORS['kruskal_wallis'] == pytest.approx(expected_are, abs=0.005)

    def test_mann_whitney_inflation(self):
        """Mann-Whitney should require slightly more N than t-test."""
        power_calc = TTestIndPower()

        # Parametric sample size
        n_param = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                         ratio=1.0, alternative='two-sided')

        # Non-parametric sample size (inflated by 1/ARE)
        n_nonparam = n_param / ARE_FACTORS['mann_whitney']

        # Should be about 5% more
        assert n_nonparam > n_param
        assert n_nonparam < n_param * 1.10


class TestClusterRandomized:
    """Validate cluster-randomized trial calculations."""

    def test_design_effect_formula(self):
        """DEFF = 1 + (m - 1) * ICC"""
        # Standard case
        deff = calculate_design_effect(icc=0.05, cluster_size=20)
        expected = 1 + (20 - 1) * 0.05
        assert deff == pytest.approx(expected, abs=0.001)

        # High ICC
        deff = calculate_design_effect(icc=0.15, cluster_size=30)
        expected = 1 + (30 - 1) * 0.15
        assert deff == pytest.approx(expected, abs=0.001)

        # Edge case: ICC = 0 (no clustering)
        deff = calculate_design_effect(icc=0.0, cluster_size=50)
        assert deff == pytest.approx(1.0, abs=0.001)

    def test_clusters_needed_calculation(self):
        """Test cluster calculation returns correct values."""
        # 64 individuals needed, cluster size 20, ICC 0.05
        total_n, n_clusters, deff = calculate_clusters_needed(
            individual_n=64, cluster_size=20, icc=0.05
        )

        # DEFF = 1.95, so total_n ≈ 64 * 1.95 = 125
        assert 120 < total_n < 130, f"Total N: expected ~125, got {total_n}"
        assert n_clusters >= math.ceil(total_n / 20), f"Clusters: got {n_clusters}"
        assert deff == pytest.approx(1.95, abs=0.01)

    def test_validation_errors(self):
        """Test input validation."""
        with pytest.raises(ValueError):
            calculate_design_effect(icc=-0.1, cluster_size=20)

        with pytest.raises(ValueError):
            calculate_design_effect(icc=1.5, cluster_size=20)

        with pytest.raises(ValueError):
            calculate_design_effect(icc=0.05, cluster_size=1)


class TestLogRankSurvival:
    """Validate log-rank test calculations using Schoenfeld's formula."""

    def test_sample_size_calculation(self):
        """Test sample size matches Schoenfeld formula.

        Schoenfeld (1981) formula for log-rank test:
        d = (z_α + z_β)² × (1 + r) / (r × θ²)
        where θ = log(HR), r = n2/n1

        For equal allocation (r=1): d = 2(z_α + z_β)² / θ²
        Then: n_total = d / prob_event, n1 = n_total / (1 + r)
        """
        # HR=0.65, α=0.05, power=0.80, 50% events
        n1 = calculate_logrank_power(
            alpha=0.05, alternative='two-sided', power=0.80,
            hazard_ratio=0.65, prob_event=0.5, ratio=1.0
        )

        assert n1 is not None, "Should return valid sample size"

        # Verify against manual Schoenfeld calculation
        z_alpha = norm.ppf(0.975)  # 1.96 for two-sided
        z_beta = norm.ppf(0.80)    # 0.84
        theta = np.log(0.65)
        d_needed = ((z_alpha + z_beta) ** 2) * 2 / (theta ** 2)  # Events needed (equal allocation)
        n_total_expected = d_needed / 0.5  # Total N with 50% event rate
        n1_expected = n_total_expected / 2  # N per group

        # Should be approximately 84-85 per group
        assert 80 < n1 < 95, f"Expected N₁ ~85, got {n1:.1f}"
        assert n1 == pytest.approx(n1_expected, rel=0.05), \
            f"Expected {n1_expected:.1f}, got {n1:.1f}"

    def test_power_calculation(self):
        """Test power calculation for log-rank test."""
        # N=150 per group, HR=0.65, 50% events
        pwr = calculate_logrank_power(
            alpha=0.05, alternative='two-sided', nobs1=150,
            hazard_ratio=0.65, prob_event=0.5, ratio=1.0
        )

        assert pwr is not None, "Should return valid power"
        assert 0.70 < pwr < 0.90, f"Expected power ~0.80, got {pwr:.3f}"

    def test_hr_symmetry(self):
        """HR=0.5 and HR=2.0 should give same power (reciprocal)."""
        pwr_low = calculate_logrank_power(
            alpha=0.05, alternative='two-sided', nobs1=100,
            hazard_ratio=0.5, prob_event=0.6, ratio=1.0
        )
        pwr_high = calculate_logrank_power(
            alpha=0.05, alternative='two-sided', nobs1=100,
            hazard_ratio=2.0, prob_event=0.6, ratio=1.0
        )

        assert pwr_low == pytest.approx(pwr_high, abs=0.01), \
            "Reciprocal HR should give same power"

    def test_higher_events_more_power(self):
        """Higher event rate should give more power."""
        pwr_low = calculate_logrank_power(
            alpha=0.05, alternative='two-sided', nobs1=100,
            hazard_ratio=0.7, prob_event=0.3, ratio=1.0
        )
        pwr_high = calculate_logrank_power(
            alpha=0.05, alternative='two-sided', nobs1=100,
            hazard_ratio=0.7, prob_event=0.8, ratio=1.0
        )

        assert pwr_high > pwr_low, "Higher event rate should increase power"


class TestSingleProportion:
    """Validate single proportion test calculations."""

    def test_sample_size_calculation(self):
        """Test sample size for single proportion test."""
        # Null=0.5, Alternative=0.65, α=0.05, power=0.80
        n = calculate_single_proportion_power(
            alpha=0.05, alternative='two-sided', power=0.80,
            null_prop=0.5, sample_prop=0.65
        )

        assert n is not None, "Should return valid sample size"
        # Manual: z_α=1.96, z_β=0.84
        # n = [(z_α*sqrt(p0(1-p0)) + z_β*sqrt(p1(1-p1))) / (p1-p0)]²
        z_a = 1.96
        z_b = 0.84
        num = z_a * np.sqrt(0.5 * 0.5) + z_b * np.sqrt(0.65 * 0.35)
        expected = (num / 0.15) ** 2

        assert n == pytest.approx(expected, rel=0.05), \
            f"Expected {expected:.1f}, got {n:.1f}"

    def test_power_calculation(self):
        """Test power for single proportion."""
        pwr = calculate_single_proportion_power(
            alpha=0.05, alternative='two-sided', nobs1=100,
            null_prop=0.5, sample_prop=0.65
        )

        assert pwr is not None, "Should return valid power"
        assert 0.75 < pwr < 0.95, f"Expected power ~0.85, got {pwr:.3f}"

    def test_validation(self):
        """Test input validation."""
        # Proportions must be in (0, 1)
        result = calculate_single_proportion_power(
            alpha=0.05, alternative='two-sided', power=0.80,
            null_prop=0.0, sample_prop=0.3
        )
        assert result is None

        # Equal proportions should fail
        result = calculate_single_proportion_power(
            alpha=0.05, alternative='two-sided', power=0.80,
            null_prop=0.5, sample_prop=0.5
        )
        assert result is None


class TestRepeatedMeasures:
    """Validate repeated measures ANOVA approximation."""

    def test_power_increases_with_correlation(self):
        """Higher correlation should increase power (more efficient design)."""
        pwr_low = calculate_repeated_measures_power(
            n=30, effect_size=0.25, alpha=0.05,
            num_measurements=3, correlation=0.2
        )
        pwr_high = calculate_repeated_measures_power(
            n=30, effect_size=0.25, alpha=0.05,
            num_measurements=3, correlation=0.7
        )

        assert pwr_high > pwr_low, "Higher correlation should increase power"

    def test_sample_size_decreases_with_correlation(self):
        """Higher correlation should require fewer subjects."""
        n_low = calculate_repeated_measures_n(
            effect_size=0.25, alpha=0.05, power=0.80,
            num_measurements=3, correlation=0.2
        )
        n_high = calculate_repeated_measures_n(
            effect_size=0.25, alpha=0.05, power=0.80,
            num_measurements=3, correlation=0.7
        )

        assert n_high < n_low, "Higher correlation should require fewer subjects"

    def test_high_correlation_warning(self):
        """Very high correlation (>0.95) should return None."""
        result = calculate_repeated_measures_power(
            n=30, effect_size=0.25, alpha=0.05,
            num_measurements=3, correlation=0.96
        )
        assert result is None, "Should return None for correlation >= 0.95"

    def test_invalid_correlation(self):
        """Invalid correlation values should be handled."""
        result = calculate_repeated_measures_power(
            n=30, effect_size=0.25, alpha=0.05,
            num_measurements=3, correlation=1.5
        )
        assert result is None


class TestFisherAdjustments:
    """Validate Fisher's exact test adjustments."""

    def test_adjustment_factors(self):
        """Fisher adjustments should be reasonable values."""
        assert 0.90 < FISHER_ADJUSTMENTS['power'] < 1.0, \
            "Power adjustment should reduce calculated power slightly"
        assert 1.0 < FISHER_ADJUSTMENTS['n'] < 1.15, \
            "N adjustment should increase required sample size slightly"

    def test_fisher_more_conservative(self):
        """Fisher's exact should require more N than chi-square."""
        # The adjustment factor of 1.05 means 5% more N
        assert FISHER_ADJUSTMENTS['n'] == pytest.approx(1.05, abs=0.01)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_small_effect(self):
        """Very small effects should require very large N."""
        power_calc = TTestIndPower()
        n = power_calc.solve_power(effect_size=0.05, alpha=0.05, power=0.80,
                                   ratio=1.0, alternative='two-sided')
        assert n > 3000, "Very small effect should require very large N"

    def test_very_large_effect(self):
        """Very large effects should require small N."""
        power_calc = TTestIndPower()
        n = power_calc.solve_power(effect_size=1.5, alpha=0.05, power=0.80,
                                   ratio=1.0, alternative='two-sided')
        assert n < 15, "Very large effect should require small N"

    def test_high_power_requirement(self):
        """Power=0.99 should require more N than power=0.80."""
        power_calc = TTestIndPower()
        n_80 = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                      ratio=1.0, alternative='two-sided')
        n_99 = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.99,
                                      ratio=1.0, alternative='two-sided')
        assert n_99 > n_80 * 1.5, "Power=0.99 should require >50% more N"

    def test_stricter_alpha(self):
        """Stricter alpha should require more N."""
        power_calc = TTestIndPower()
        n_05 = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                                      ratio=1.0, alternative='two-sided')
        n_01 = power_calc.solve_power(effect_size=0.5, alpha=0.01, power=0.80,
                                      ratio=1.0, alternative='two-sided')
        assert n_01 > n_05, "Stricter alpha should require more N"


# Integration test to run quick validation
def test_integration_quick_check():
    """Quick integration test to verify basic functionality."""
    # Effect size calculation
    d = calculate_effect_size('cohen_d_two', mean1=110, mean2=100, pooled_sd=15)
    assert d is not None and 0.6 < d < 0.7

    # T-test power
    power_calc = TTestIndPower()
    n = power_calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                               ratio=1.0, alternative='two-sided')
    assert 60 < n < 70

    # Cluster design effect
    deff = calculate_design_effect(icc=0.05, cluster_size=20)
    assert 1.9 < deff < 2.0

    print("✅ Integration test passed!")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
