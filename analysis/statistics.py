#!/usr/bin/env python3
"""Statistical primitives for the frozen Void Matrix analysis.

This module has no provider or network dependencies.  Every function accepts
already-recorded observations and returns explicit numerators, denominators,
effect sizes, and uncertainty estimates.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from decimal import Decimal, localcontext
from typing import Any

import numpy as np
from scipy.special import logsumexp
from scipy.stats import beta, fisher_exact, hypergeom


def clopper_pearson(successes: int, total: int, alpha: float = 0.05) -> tuple[float, float]:
    """Two-sided exact binomial confidence interval."""
    if total <= 0:
        return math.nan, math.nan
    lower = 0.0 if successes == 0 else float(beta.ppf(alpha / 2, successes, total - successes + 1))
    upper = 1.0 if successes == total else float(beta.ppf(1 - alpha / 2, successes + 1, total - successes))
    return lower, upper


def rate_record(successes: int, total: int, label: str = "") -> dict[str, Any]:
    lower, upper = clopper_pearson(successes, total)
    return {
        "label": label,
        "numerator": int(successes),
        "denominator": int(total),
        "rate": successes / total if total else math.nan,
        "ci95_low": lower,
        "ci95_high": upper,
        "ci_method": "Clopper-Pearson exact",
    }


def two_by_two(a: int, b: int, c: int, d: int) -> dict[str, Any]:
    """Effect estimates for [[a,b],[c,d]] with exact Fisher p-value.

    a = exposed outcome, b = exposed non-outcome,
    c = control outcome, d = control non-outcome.
    Haldane-Anscombe correction is used only when a zero cell prevents finite
    ratio estimates; the uncorrected counts remain in the output.
    """
    table = [[int(a), int(b)], [int(c), int(d)]]
    exposed_total, control_total = a + b, c + d
    risk_exposed = a / exposed_total if exposed_total else math.nan
    risk_control = c / control_total if control_total else math.nan
    corrected = any(x == 0 for x in (a, b, c, d))
    aa, bb, cc, dd = (x + 0.5 for x in (a, b, c, d)) if corrected else (a, b, c, d)
    rr = (aa / (aa + bb)) / (cc / (cc + dd))
    odds_ratio = (aa * dd) / (bb * cc)
    rd_se = math.sqrt(
        risk_exposed * (1 - risk_exposed) / exposed_total
        + risk_control * (1 - risk_control) / control_total
    )
    rd_low = max(-1.0, risk_exposed - risk_control - 1.959963984540054 * rd_se)
    rd_high = min(1.0, risk_exposed - risk_control + 1.959963984540054 * rd_se)
    log_rr_se = math.sqrt(
        (1 / aa) - (1 / (aa + bb)) + (1 / cc) - (1 / (cc + dd))
    )
    rr_low = math.exp(math.log(rr) - 1.959963984540054 * log_rr_se)
    rr_high = math.exp(math.log(rr) + 1.959963984540054 * log_rr_se)
    log_or_se = math.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    or_low = math.exp(math.log(odds_ratio) - 1.959963984540054 * log_or_se)
    or_high = math.exp(math.log(odds_ratio) + 1.959963984540054 * log_or_se)
    fisher_or, fisher_p = fisher_exact(table, alternative="two-sided")
    # Recompute the two-sided Fisher tail in log space. This preserves a finite
    # log10 probability even when the public float value underflows to zero.
    # The test remains the exact fixed-margin Fisher test; only its numerical
    # summation is performed in the log domain.
    row_one = a + b
    column_one = a + c
    total = a + b + c + d
    lower = max(0, row_one - (total - column_one))
    upper = min(row_one, column_one)
    support = np.arange(lower, upper + 1)
    support_log_probabilities = hypergeom.logpmf(
        support, total, column_one, row_one
    )
    observed_log_probability = float(
        hypergeom.logpmf(a, total, column_one, row_one)
    )
    included = support_log_probabilities <= (
        observed_log_probability + 1e-12
    )
    fisher_log10 = float(
        logsumexp(support_log_probabilities[included]) / math.log(10)
    )
    fisher_display = (
        f"p < 10^{math.floor(fisher_log10) + 1}; "
        f"log10(p)={fisher_log10:.6f}"
        if fisher_p == 0.0
        else f"{float(fisher_p):.12g}; log10(p)={fisher_log10:.6f}"
    )
    return {
        "a": int(a),
        "b": int(b),
        "c": int(c),
        "d": int(d),
        "risk_exposed": risk_exposed,
        "risk_control": risk_control,
        "risk_difference": risk_exposed - risk_control,
        "risk_difference_ci95_low": rd_low,
        "risk_difference_ci95_high": rd_high,
        "risk_difference_ci_method": "Wald difference of independent proportions",
        "risk_ratio": float(rr),
        "risk_ratio_ci95_low": float(rr_low),
        "risk_ratio_ci95_high": float(rr_high),
        "risk_ratio_ci_method": (
            "log-Wald after Haldane-Anscombe 0.5 correction"
            if corrected
            else "log-Wald"
        ),
        "odds_ratio": float(odds_ratio),
        "odds_ratio_ci95_low": float(or_low),
        "odds_ratio_ci95_high": float(or_high),
        "odds_ratio_ci_method": (
            "log-Wald after Haldane-Anscombe 0.5 correction"
            if corrected
            else "log-Wald"
        ),
        "zero_cell_correction": "Haldane-Anscombe 0.5" if corrected else "none",
        "fisher_exact_odds_ratio": float(fisher_or),
        "fisher_exact_p": float(fisher_p),
        "fisher_exact_log10_p": fisher_log10,
        "fisher_exact_p_display": fisher_display,
    }


def exact_mcnemar(exposed: Iterable[bool], control: Iterable[bool]) -> dict[str, Any]:
    pairs = list(zip(exposed, control))
    both = sum(a and b for a, b in pairs)
    exposed_only = sum(a and not b for a, b in pairs)
    control_only = sum(not a and b for a, b in pairs)
    neither = sum(not a and not b for a, b in pairs)
    discordant = exposed_only + control_only
    if discordant == 0:
        exact_numerator, exact_denominator = 1, 1
    else:
        tail_numerator = sum(
            math.comb(discordant, k)
            for k in range(min(exposed_only, control_only) + 1)
        )
        exact_numerator = min(2**discordant, 2 * tail_numerator)
        exact_denominator = 2**discordant
    with localcontext() as context:
        context.prec = 100
        exact_decimal = Decimal(exact_numerator) / Decimal(exact_denominator)
        log10_p = float(exact_decimal.log10()) if exact_decimal else -math.inf
        p = float(exact_decimal)
    direction_low, direction_high = clopper_pearson(exposed_only, discordant)
    pair_count = len(pairs)
    paired_rd = (exposed_only - control_only) / pair_count if pair_count else math.nan
    paired_rd_se = (
        math.sqrt(
            (
                exposed_only
                + control_only
                - ((exposed_only - control_only) ** 2 / pair_count)
            )
            / (pair_count**2)
        )
        if pair_count
        else math.nan
    )
    return {
        "pair_count": pair_count,
        "both_outcome": both,
        "exposed_only": exposed_only,
        "control_only": control_only,
        "neither": neither,
        "discordant_pairs": discordant,
        "exact_mcnemar_p": p,
        "exact_mcnemar_log10_p": log10_p,
        "exact_mcnemar_p_display": (
            f"p < 10^{math.floor(log10_p) + 1}; log10(p)={log10_p:.6f}"
            if p == 0.0
            else f"{p:.12g}; log10(p)={log10_p:.6f}"
        ),
        "discordant_direction_rate": exposed_only / discordant if discordant else math.nan,
        "discordant_direction_ci95_low": direction_low,
        "discordant_direction_ci95_high": direction_high,
        "discordant_direction_ci_method": "Clopper-Pearson exact",
        "paired_risk_difference": paired_rd,
        "paired_risk_difference_ci95_low": max(
            -1.0, paired_rd - 1.959963984540054 * paired_rd_se
        ) if pair_count else math.nan,
        "paired_risk_difference_ci95_high": min(
            1.0, paired_rd + 1.959963984540054 * paired_rd_se
        ) if pair_count else math.nan,
        "paired_risk_difference_ci_method": "paired binary Wald interval",
    }


def cluster_bootstrap_rate(
    outcomes: Iterable[bool],
    clusters: Iterable[str],
    *,
    seed: int = 20260728,
    replicates: int = 20_000,
) -> dict[str, Any]:
    """Percentile cluster bootstrap, resampling whole clusters."""
    y = np.asarray(list(outcomes), dtype=float)
    g = np.asarray(list(clusters), dtype=object)
    unique = np.unique(g)
    if len(y) == 0 or len(unique) < 2:
        return {
            "cluster_count": int(len(unique)),
            "rate": float(y.mean()) if len(y) else math.nan,
            "bootstrap_ci95_low": math.nan,
            "bootstrap_ci95_high": math.nan,
            "bootstrap_replicates": 0,
        }
    by_cluster = {key: y[g == key] for key in unique}
    rng = np.random.default_rng(seed)
    estimates = np.empty(replicates, dtype=float)
    for i in range(replicates):
        selected = rng.choice(unique, size=len(unique), replace=True)
        sampled = np.concatenate([by_cluster[key] for key in selected])
        estimates[i] = sampled.mean()
    return {
        "cluster_count": int(len(unique)),
        "rate": float(y.mean()),
        "bootstrap_ci95_low": float(np.quantile(estimates, 0.025)),
        "bootstrap_ci95_high": float(np.quantile(estimates, 0.975)),
        "bootstrap_replicates": int(replicates),
        "bootstrap_seed": int(seed),
    }


def cluster_bootstrap_contrast(
    outcomes: Iterable[bool],
    conditions: Iterable[bool],
    clusters: Iterable[str],
    *,
    seed: int = 20260728,
    replicates: int = 20_000,
) -> dict[str, Any]:
    """Cluster bootstrap for null/control risk difference and risk ratio."""
    y = np.asarray(list(outcomes), dtype=float)
    condition = np.asarray(list(conditions), dtype=bool)
    group = np.asarray(list(clusters), dtype=object)
    unique = np.unique(group)
    if len(y) == 0 or len(unique) < 2:
        return {
            "cluster_count": int(len(unique)),
            "bootstrap_replicates": 0,
        }
    by_cluster = {
        key: (y[group == key], condition[group == key])
        for key in unique
    }
    rng = np.random.default_rng(seed)
    risk_differences: list[float] = []
    risk_ratios: list[float] = []
    for _ in range(replicates):
        selected = rng.choice(unique, size=len(unique), replace=True)
        sampled_y = np.concatenate([by_cluster[key][0] for key in selected])
        sampled_c = np.concatenate([by_cluster[key][1] for key in selected])
        if not sampled_c.any() or sampled_c.all():
            continue
        exposed = sampled_y[sampled_c].mean()
        control = sampled_y[~sampled_c].mean()
        risk_differences.append(float(exposed - control))
        if control > 0:
            risk_ratios.append(float(exposed / control))
    return {
        "cluster_count": int(len(unique)),
        "bootstrap_replicates": int(len(risk_differences)),
        "bootstrap_seed": int(seed),
        "risk_difference": float(y[condition].mean() - y[~condition].mean()),
        "risk_difference_bootstrap_ci95_low": float(np.quantile(risk_differences, 0.025)),
        "risk_difference_bootstrap_ci95_high": float(np.quantile(risk_differences, 0.975)),
        "risk_ratio": float(y[condition].mean() / y[~condition].mean())
        if y[~condition].mean() > 0
        else math.inf,
        "risk_ratio_bootstrap_ci95_low": float(np.quantile(risk_ratios, 0.025))
        if risk_ratios
        else math.nan,
        "risk_ratio_bootstrap_ci95_high": float(np.quantile(risk_ratios, 0.975))
        if risk_ratios
        else math.nan,
    }
