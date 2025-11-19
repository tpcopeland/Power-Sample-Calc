"""
Backward Compatibility Test Suite for Original 11 Tests
Tests that all original features still work correctly after recent additions
"""
import sys
import numpy as np
from statsmodels.stats.power import TTestIndPower, TTestPower, FTestAnovaPower

# Test configurations for the original 11 tests
ORIGINAL_TESTS = {
    "Two-Sample Independent Groups t-test": {
        "key": "2samp",
        "class": TTestIndPower,
        "effect": "cohen_d_two",
        "benchmarks": {"Small": 0.2, "Medium": 0.5, "Large": 0.8},
        "raw_inputs": ["mean1", "mean2", "pooled_sd"],
        "n_ratio": True,
        "n_labels": ["Required N₁", "Required N₂", "Total N Required"]
    },
    "One-Sample t-test": {
        "key": "1samp",
        "class": TTestPower,
        "effect": "cohen_d_one",
        "nobs_total": True,
        "benchmarks": {"Small": 0.2, "Medium": 0.5, "Large": 0.8},
        "raw_inputs": ["hypothesized_mean", "sample_mean", "sd"],
        "n_labels": ["Required Sample Size (N)"]
    },
    "Paired t-test": {
        "key": "paired",
        "class": TTestPower,
        "effect": "cohen_d_paired",
        "nobs_total": True,
        "benchmarks": {"Small": 0.2, "Medium": 0.5, "Large": 0.8},
        "raw_inputs": ["mean_diff", "sd_diff"],
        "n_labels": ["Required Number of Pairs (N)"]
    },
    "Z-test: Two Independent Proportions": {
        "key": "prop",
        "func": "power_proportions_2indep",
        "effect": "cohen_h",
        "raw_inputs": ["prop1", "prop2"],
        "n_ratio": True,
        "check_counts": "two_prop",
        "n_labels": ["Required N₁", "Required N₂", "Total N Required"]
    },
    "Z-test: Single Proportion": {
        "key": "singleprop",
        "func": "calculate_single_proportion_power",
        "effect": "cohen_h",
        "raw_inputs": ["null_prop", "sample_prop"],
        "check_counts": "one_prop",
        "n_labels": ["Required Sample Size (N)"]
    },
    "One-Way ANOVA (Between Subjects)": {
        "key": "anova",
        "class": FTestAnovaPower,
        "effect": "cohen_f",
        "benchmarks": {"Small": 0.10, "Medium": 0.25, "Large": 0.40},
        "k_groups": True,
        "fixed_alt": True,
        "nobs_total": True,
        "n_labels": ["Required N per Group", "Total N Required"]
    },
    "Mann-Whitney U Test": {
        "key": "mw",
        "class": TTestIndPower,
        "effect": "cohen_d_two",
        "are": "mann_whitney",
        "raw_inputs": ["median1", "median2", "pooled_sd"],
        "n_ratio": True,
        "n_labels": ["Approx. Required N₁", "Approx. Required N₂", "Approx. Total N"]
    },
    "Wilcoxon Signed-Rank Test": {
        "key": "wilcox",
        "class": TTestPower,
        "effect": "wilcoxon_special",
        "are": "wilcoxon",
        "nobs_total": True,
        "n_labels": ["Approx. Required N"]
    },
    "Kruskal-Wallis Test": {
        "key": "kw",
        "class": FTestAnovaPower,
        "effect": "cohen_f",
        "are": "kruskal_wallis",
        "k_groups": True,
        "fixed_alt": True,
        "nobs_total": True,
        "n_labels": ["Approx. N per Group", "Approx. Total N"]
    },
    "Fisher's Exact Test": {
        "key": "fisher",
        "func": "power_proportions_2indep",
        "effect": "cohen_h",
        "raw_inputs": ["prop1", "prop2"],
        "n_ratio": True,
        "fisher": True,
        "n_labels": ["Approx. Required N₁", "Approx. Required N₂", "Approx. Total N"]
    },
    "Log-Rank Test": {
        "key": "logrank",
        "func": "calculate_logrank_power",
        "effect": "hazard_ratio",
        "raw_inputs": ["hazard_ratio", "prob_event"],
        "n_ratio": True,
        "n_labels": ["Required N₁", "Required N₂", "Total N Required"],
        "benchmarks": {"Small (HR=0.8)": 0.8, "Medium (HR=0.65)": 0.65, "Large (HR=0.5)": 0.5}
    }
}

# ARE factors must be unchanged
EXPECTED_ARE_FACTORS = {"wilcoxon": 0.955, "mann_whitney": 0.955, "kruskal_wallis": 0.955}
EXPECTED_FISHER_ADJUSTMENTS = {"power": 0.95, "n": 1.05}

def test_imports():
    """Test that all required imports are available"""
    print("Testing imports...")
    try:
        from power_sample_calc import (
            TTestIndPower, TTestPower, FTestAnovaPower,
            ARE_FACTORS, FISHER_ADJUSTMENTS,
            calculate_effect_size, get_test_config,
            power_proportions_2indep, calculate_single_proportion_power,
            calculate_logrank_power
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_constants():
    """Test that constants haven't been changed"""
    print("\nTesting constants...")
    from power_sample_calc import ARE_FACTORS, FISHER_ADJUSTMENTS

    issues = []

    # Check ARE factors
    if ARE_FACTORS != EXPECTED_ARE_FACTORS:
        issues.append(f"ARE_FACTORS changed: expected {EXPECTED_ARE_FACTORS}, got {ARE_FACTORS}")
    else:
        print("✓ ARE_FACTORS unchanged")

    # Check Fisher adjustments
    if FISHER_ADJUSTMENTS != EXPECTED_FISHER_ADJUSTMENTS:
        issues.append(f"FISHER_ADJUSTMENTS changed: expected {EXPECTED_FISHER_ADJUSTMENTS}, got {FISHER_ADJUSTMENTS}")
    else:
        print("✓ FISHER_ADJUSTMENTS unchanged")

    return len(issues) == 0, issues

def test_get_test_config():
    """Test that get_test_config returns correct configuration for all original tests"""
    print("\nTesting get_test_config...")
    from power_sample_calc import get_test_config

    issues = []

    for test_name, expected_config in ORIGINAL_TESTS.items():
        config = get_test_config(test_name)

        if not config:
            issues.append(f"{test_name}: config is empty or None")
            continue

        # Check key fields
        if config.get("key") != expected_config.get("key"):
            issues.append(f"{test_name}: key mismatch - expected {expected_config.get('key')}, got {config.get('key')}")

        if config.get("effect") != expected_config.get("effect"):
            issues.append(f"{test_name}: effect mismatch - expected {expected_config.get('effect')}, got {config.get('effect')}")

        # Check class or func
        if expected_config.get("class"):
            if config.get("class") != expected_config.get("class"):
                issues.append(f"{test_name}: class mismatch")
        elif expected_config.get("func"):
            if config.get("func") != expected_config.get("func"):
                issues.append(f"{test_name}: func mismatch - expected {expected_config.get('func')}, got {config.get('func')}")

        if not issues:
            print(f"✓ {test_name}")

    if issues:
        for issue in issues:
            print(f"✗ {issue}")

    return len(issues) == 0, issues

def test_effect_size_calculations():
    """Test that effect size calculations work correctly"""
    print("\nTesting effect size calculations...")
    from power_sample_calc import calculate_effect_size

    issues = []

    # Test cohen_d_two
    result = calculate_effect_size("cohen_d_two", mean1=10, mean2=15, pooled_sd=10)
    expected = 0.5
    if result is None or abs(result - expected) > 0.001:
        issues.append(f"cohen_d_two: expected {expected}, got {result}")
    else:
        print("✓ cohen_d_two calculation correct")

    # Test cohen_d_one
    result = calculate_effect_size("cohen_d_one", sample_mean=12, hypothesized_mean=10, sd=4)
    expected = 0.5
    if result is None or abs(result - expected) > 0.001:
        issues.append(f"cohen_d_one: expected {expected}, got {result}")
    else:
        print("✓ cohen_d_one calculation correct")

    # Test cohen_d_paired
    result = calculate_effect_size("cohen_d_paired", mean_diff=5, sd_diff=10)
    expected = 0.5
    if result is None or abs(result - expected) > 0.001:
        issues.append(f"cohen_d_paired: expected {expected}, got {result}")
    else:
        print("✓ cohen_d_paired calculation correct")

    # Test cohen_h
    result = calculate_effect_size("cohen_h", p1=0.25, p2=0.40)
    # Cohen's h = 2 * (arcsin(sqrt(p1)) - arcsin(sqrt(p2)))
    expected = abs(2 * np.arcsin(np.sqrt(0.25)) - 2 * np.arcsin(np.sqrt(0.40)))
    if result is None or abs(result - expected) > 0.001:
        issues.append(f"cohen_h: expected {expected:.3f}, got {result}")
    else:
        print("✓ cohen_h calculation correct")

    return len(issues) == 0, issues

def test_parametric_calculations():
    """Test that parametric test calculations still work"""
    print("\nTesting parametric calculations...")

    issues = []

    # Test Two-Sample t-test
    try:
        calc = TTestIndPower()
        n = calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80, ratio=1.0, alternative='two-sided')
        if n is None or n < 0:
            issues.append("Two-Sample t-test: invalid result")
        else:
            print(f"✓ Two-Sample t-test: n1={n:.1f}")
    except Exception as e:
        issues.append(f"Two-Sample t-test: {e}")

    # Test One-Sample t-test
    try:
        calc = TTestPower()
        n = calc.solve_power(effect_size=0.5, alpha=0.05, power=0.80, alternative='two-sided')
        if n is None or n < 0:
            issues.append("One-Sample t-test: invalid result")
        else:
            print(f"✓ One-Sample t-test: n={n:.1f}")
    except Exception as e:
        issues.append(f"One-Sample t-test: {e}")

    # Test ANOVA
    try:
        calc = FTestAnovaPower()
        n = calc.solve_power(effect_size=0.25, alpha=0.05, power=0.80, k_groups=3)
        if n is None or n < 0:
            issues.append("One-Way ANOVA: invalid result")
        else:
            print(f"✓ One-Way ANOVA: n_per_group={n:.1f}")
    except Exception as e:
        issues.append(f"One-Way ANOVA: {e}")

    return len(issues) == 0, issues

def test_proportion_calculations():
    """Test that proportion test calculations still work"""
    print("\nTesting proportion calculations...")
    from power_sample_calc import power_proportions_2indep, calculate_single_proportion_power

    issues = []

    # Test Two Proportions
    try:
        effect = abs(2 * np.arcsin(np.sqrt(0.25)) - 2 * np.arcsin(np.sqrt(0.40)))
        power = power_proportions_2indep(effect_size=effect, nobs1=100, alpha=0.05, ratio=1.0, alternative='two-sided')
        if power is None or power < 0 or power > 1:
            issues.append("Two Proportions: invalid power result")
        else:
            print(f"✓ Two Proportions: power={power:.3f}")
    except Exception as e:
        issues.append(f"Two Proportions: {e}")

    # Test Single Proportion
    try:
        n = calculate_single_proportion_power(
            alpha=0.05,
            alternative='two-sided',
            power=0.80,
            nobs1=None,
            sample_prop=0.60,
            null_prop=0.50
        )
        if n is None or n < 0:
            issues.append("Single Proportion: invalid sample size result")
        else:
            print(f"✓ Single Proportion: n={n:.1f}")
    except Exception as e:
        issues.append(f"Single Proportion: {e}")

    return len(issues) == 0, issues

def test_survival_calculations():
    """Test that survival analysis calculations still work"""
    print("\nTesting survival calculations...")
    from power_sample_calc import calculate_logrank_power

    issues = []

    # Test Log-Rank
    try:
        n = calculate_logrank_power(
            alpha=0.05,
            alternative='two-sided',
            power=0.80,
            nobs1=None,
            hazard_ratio=0.65,
            prob_event=0.5,
            ratio=1.0
        )
        if n is None or n < 0:
            issues.append("Log-Rank: invalid sample size result")
        else:
            print(f"✓ Log-Rank: n1={n:.1f}")
    except Exception as e:
        issues.append(f"Log-Rank: {e}")

    return len(issues) == 0, issues

def run_all_tests():
    """Run all backward compatibility tests"""
    print("="*70)
    print("BACKWARD COMPATIBILITY TEST SUITE")
    print("Testing 11 Original Features")
    print("="*70)

    all_passed = True
    all_issues = []

    # Test 1: Imports
    if not test_imports():
        print("\n✗ CRITICAL: Import test failed. Cannot continue.")
        return False

    # Test 2: Constants
    passed, issues = test_constants()
    if not passed:
        all_passed = False
        all_issues.extend(issues)

    # Test 3: Test configurations
    passed, issues = test_get_test_config()
    if not passed:
        all_passed = False
        all_issues.extend(issues)

    # Test 4: Effect size calculations
    passed, issues = test_effect_size_calculations()
    if not passed:
        all_passed = False
        all_issues.extend(issues)

    # Test 5: Parametric calculations
    passed, issues = test_parametric_calculations()
    if not passed:
        all_passed = False
        all_issues.extend(issues)

    # Test 6: Proportion calculations
    passed, issues = test_proportion_calculations()
    if not passed:
        all_passed = False
        all_issues.extend(issues)

    # Test 7: Survival calculations
    passed, issues = test_survival_calculations()
    if not passed:
        all_passed = False
        all_issues.extend(issues)

    # Summary
    print("\n" + "="*70)
    if all_passed:
        print("✓ ALL TESTS PASSED - BACKWARD COMPATIBILITY CONFIRMED")
        print("All 11 original features are working correctly.")
    else:
        print("✗ SOME TESTS FAILED - BACKWARD COMPATIBILITY ISSUES DETECTED")
        print(f"\nTotal issues found: {len(all_issues)}")
        print("\nIssues:")
        for issue in all_issues:
            print(f"  - {issue}")
    print("="*70)

    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
