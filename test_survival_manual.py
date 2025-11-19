"""
Manual test for survival analysis (log-rank) power calculations.
Tests the calculate_logrank_power function without requiring full environment.
"""

import math
import numpy as np
from scipy.stats import norm


def calculate_logrank_power(alpha, alternative, power=None, nobs1=None,
                            hazard_ratio=None, prob_event=0.5, ratio=1.0):
    """
    Simplified version for testing (without streamlit error handling).
    """
    if hazard_ratio is None or hazard_ratio <= 0:
        raise ValueError("Hazard ratio must be positive")

    if hazard_ratio == 1:
        raise ValueError("Hazard ratio must be different from 1")

    if not (0 < prob_event <= 1):
        raise ValueError("Probability of event must be between 0 and 1")

    # Critical values
    alpha_crit = alpha / 2 if alternative == "two-sided" else alpha
    z_alpha = norm.ppf(1 - alpha_crit)

    # Log hazard ratio
    theta = np.log(hazard_ratio)

    if power is None and nobs1 is not None:  # Calculate power
        if nobs1 <= 0:
            raise ValueError("Sample size must be positive")

        # Total sample size
        n2 = nobs1 * ratio
        n_total = nobs1 + n2

        # Expected number of events
        d = n_total * prob_event

        # Proportion in each group
        p1 = nobs1 / n_total
        p2 = n2 / n_total

        # Variance of log(HR) estimator
        var_theta = 1 / (d * p1 * p2)

        # Calculate power
        # Test statistic under alternative: z_obs ~ N(theta/sqrt(var), 1)
        z_obs = abs(theta) / np.sqrt(var_theta)

        if alternative == "two-sided":
            # Power = P(|Z| > z_alpha | theta != 0)
            # = Φ(z_obs - z_alpha) + Φ(-z_obs - z_alpha)
            result = 1 - norm.cdf(z_alpha - z_obs) + norm.cdf(-z_alpha - z_obs)
        else:
            # One-sided test
            if alternative == "larger":
                # HR < 1, theta < 0
                z_obs = theta / np.sqrt(var_theta)  # Keep negative sign
                result = norm.cdf(z_obs - z_alpha)
            else:
                # HR > 1, theta > 0
                z_obs = theta / np.sqrt(var_theta)
                result = 1 - norm.cdf(z_alpha - z_obs)

        return max(0.0, min(1.0, result))

    elif nobs1 is None and power is not None:  # Calculate N
        if not 0 < power < 1:
            raise ValueError(f"Power must be between 0 and 1, got {power}")

        z_beta = norm.ppf(power)

        # Number of events needed (Schoenfeld's formula)
        # For two groups with allocation ratio r = n2/n1:
        # d = (z_alpha + z_beta)² × (1 + r)² / (r × theta²)
        # For equal allocation (r=1): d = 4 × (z_alpha + z_beta)² / theta²
        d_needed = ((z_alpha + z_beta) ** 2) * ((1 + ratio) ** 2) / (ratio * (theta ** 2))

        # Convert events to total sample size
        n_total = d_needed / prob_event

        # Calculate N1 from total N and ratio
        n1 = n_total / (1 + ratio)

        return max(1, n1)

    raise ValueError("Must provide either power or nobs1")


def test_sample_size_calculation():
    """Test sample size calculation for log-rank test."""
    print("Test 1: Sample size calculation")
    print("-" * 50)

    # Parameters: HR=0.65, 80% power, 5% alpha, 50% event rate, equal groups
    n1 = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        power=0.80,
        hazard_ratio=0.65,
        prob_event=0.5,
        ratio=1.0
    )

    print(f"Hazard Ratio: 0.65")
    print(f"Power: 0.80")
    print(f"Alpha: 0.05 (two-sided)")
    print(f"Event Probability: 0.50")
    print(f"Calculated N1: {n1:.1f}")
    print(f"Calculated N2: {n1:.1f}")
    print(f"Total N: {2*n1:.1f}")
    print()

    # Expected: approximately 169 per group for HR=0.65, 50% event rate
    # d = 4 × (1.96 + 0.84)² / 0.431² = 168.6 events
    # n_total = 168.6 / 0.5 = 337.2, n1 = 168.6
    assert 160 < n1 < 180, f"N1 out of expected range: {n1}"
    print("✓ Test passed - sample size in expected range")
    print()


def test_power_calculation():
    """Test power calculation for log-rank test."""
    print("Test 2: Power calculation")
    print("-" * 50)

    # Parameters: HR=0.65, N=169 per group, 5% alpha, 50% event rate
    power = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        nobs1=169,
        hazard_ratio=0.65,
        prob_event=0.5,
        ratio=1.0
    )

    print(f"Hazard Ratio: 0.65")
    print(f"N per group: 169")
    print(f"Alpha: 0.05 (two-sided)")
    print(f"Event Probability: 0.50")
    print(f"Calculated Power: {power:.3f}")
    print()

    # Expected: approximately 0.80
    assert 0.75 < power < 0.85, f"Power out of expected range: {power}"
    print("✓ Test passed - power in expected range")
    print()


def test_high_event_rate():
    """Test with high event rate (should require fewer participants)."""
    print("Test 3: High event rate")
    print("-" * 50)

    # Same HR, but 90% event rate
    n1 = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        power=0.80,
        hazard_ratio=0.65,
        prob_event=0.9,
        ratio=1.0
    )

    print(f"Hazard Ratio: 0.65")
    print(f"Power: 0.80")
    print(f"Event Probability: 0.90")
    print(f"Calculated N1: {n1:.1f}")
    print()

    # Should be about 169 * 0.5 / 0.9 ≈ 94
    assert 85 < n1 < 105, f"N1 out of expected range: {n1}"
    print("✓ Test passed - higher event rate reduces required N")
    print()


def test_large_effect():
    """Test with large effect (HR=0.5)."""
    print("Test 4: Large effect size")
    print("-" * 50)

    n1 = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        power=0.80,
        hazard_ratio=0.5,
        prob_event=0.5,
        ratio=1.0
    )

    print(f"Hazard Ratio: 0.50 (50% reduction)")
    print(f"Power: 0.80")
    print(f"Event Probability: 0.50")
    print(f"Calculated N1: {n1:.1f}")
    print()

    # Larger effect should require smaller N
    assert 30 < n1 < 70, f"N1 out of expected range: {n1}"
    print("✓ Test passed - larger effect requires smaller N")
    print()


def test_unequal_groups():
    """Test with unequal group allocation (2:1 ratio)."""
    print("Test 5: Unequal group allocation")
    print("-" * 50)

    n1 = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        power=0.80,
        hazard_ratio=0.65,
        prob_event=0.5,
        ratio=2.0  # N2 = 2*N1
    )

    n2 = n1 * 2.0

    print(f"Hazard Ratio: 0.65")
    print(f"Power: 0.80")
    print(f"Allocation Ratio: 2:1")
    print(f"Calculated N1: {n1:.1f}")
    print(f"Calculated N2: {n2:.1f}")
    print(f"Total N: {n1 + n2:.1f}")
    print()

    # Unequal allocation is less efficient, so total N should be larger than 338
    assert 365 < (n1 + n2) < 415, f"Total N out of expected range: {n1 + n2}"
    print("✓ Test passed - unequal allocation requires larger total N")
    print()


def test_reciprocal_hazard_ratios():
    """Test that HR=0.5 and HR=2.0 give similar sample sizes."""
    print("Test 6: Reciprocal hazard ratios")
    print("-" * 50)

    n1_reduced = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        power=0.80,
        hazard_ratio=0.5,
        prob_event=0.5,
        ratio=1.0
    )

    n1_increased = calculate_logrank_power(
        alpha=0.05,
        alternative="two-sided",
        power=0.80,
        hazard_ratio=2.0,
        prob_event=0.5,
        ratio=1.0
    )

    print(f"HR=0.5 (50% reduction) requires N1: {n1_reduced:.1f}")
    print(f"HR=2.0 (100% increase) requires N1: {n1_increased:.1f}")
    print(f"Difference: {abs(n1_reduced - n1_increased):.1f}")
    print()

    # Should be approximately equal (symmetric on log scale)
    assert abs(n1_reduced - n1_increased) < 5, "Reciprocal HRs should give similar N"
    print("✓ Test passed - reciprocal HRs give similar sample sizes")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("SURVIVAL ANALYSIS (LOG-RANK) POWER CALCULATION TESTS")
    print("=" * 50)
    print()

    try:
        test_sample_size_calculation()
        test_power_calculation()
        test_high_event_rate()
        test_large_effect()
        test_unequal_groups()
        test_reciprocal_hazard_ratios()

        print("=" * 50)
        print("ALL TESTS PASSED! ✓")
        print("=" * 50)

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
