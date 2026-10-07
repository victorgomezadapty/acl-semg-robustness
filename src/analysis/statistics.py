"""Fixed exploratory tests; participant bootstrap; no normality-driven test switching."""

import numpy as np
from scipy import stats


def holm(values):
    p = np.asarray(values, float)
    order = np.argsort(p)
    adjusted = np.empty(len(p))
    adjusted[order] = np.minimum(
        1, np.maximum.accumulate(p[order] * (len(p) - np.arange(len(p))))
    )
    return adjusted


def compare(a, b, paired, rng, replicates=5000):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if not (np.isfinite(a).all() and np.isfinite(b).all()):
        raise ValueError("Nonfinite endpoint")
    if paired:
        if len(a) != len(b):
            raise ValueError("Paired lengths differ")
        d = a - b
        test = stats.ttest_rel(a, b)
        rank = stats.wilcoxon(d, method="auto") if np.any(d) else None
        ranks = stats.rankdata(np.abs(d[d != 0]))
        signs = np.sign(d[d != 0])
        rank_effect = (
            float(np.sum(ranks * signs) / np.sum(ranks)) if len(ranks) else 0.0
        )
        effect = float(d.mean() / d.std(ddof=1)) if d.std(ddof=1) > 0 else float("nan")
        sample = rng.integers(0, len(a), size=(replicates, len(a)))
        boot = np.mean(d[sample], axis=1)
        mode = "paired_t"
        effect_name = "Cohen_dz"
    else:
        test = stats.ttest_ind(a, b, equal_var=False)
        rank = stats.mannwhitneyu(a, b, alternative="two-sided", method="auto")
        rank_effect = float(2 * rank.statistic / (len(a) * len(b)) - 1)
        df = len(a) + len(b) - 2
        pooled = np.sqrt(
            ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / df
        )
        effect = (
            float((a.mean() - b.mean()) / pooled * (1 - 3 / (4 * df - 1)))
            if pooled > 0
            else float("nan")
        )
        boot = rng.choice(a, size=(replicates, len(a))).mean(axis=1) - rng.choice(
            b, size=(replicates, len(b))
        ).mean(axis=1)
        mode = "Welch_t"
        effect_name = "Hedges_g"
    low, high = np.quantile(boot, [0.025, 0.975])
    return {
        "n_a": len(a),
        "n_b": len(b),
        "mean_difference_a_minus_b": float(a.mean() - b.mean()),
        "bootstrap95_low": float(low),
        "bootstrap95_high": float(high),
        "test": mode,
        "statistic": float(test.statistic),
        "p_raw": float(test.pvalue),
        "effect_name": effect_name,
        "effect": effect,
        "rank_test": "Wilcoxon" if paired else "Mann_Whitney",
        "rank_p_raw": float(rank.pvalue) if rank else 1.0,
        "rank_biserial": rank_effect,
        "shapiro_p_a": float(stats.shapiro(a).pvalue),
        "shapiro_p_b": float(stats.shapiro(b).pvalue),
    }
