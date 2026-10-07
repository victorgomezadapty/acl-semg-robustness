"""Checks for multiplicity, direction and pairing of exploratory statistics."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np

from src.analysis.statistics import compare, holm

assert np.allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
a = np.array([3.0, 5.0, 7.0, 9.0, 11.0])
b = np.array([1.0, 2.0, 4.0, 5.0, 8.0])
r = compare(a, b, True, np.random.default_rng(1), 1000)
assert np.isclose(r["mean_difference_a_minus_b"], 3.0)
assert r["rank_biserial"] == 1 and r["bootstrap95_low"] <= 3 <= r["bootstrap95_high"]
forward = compare(a, b, False, np.random.default_rng(2), 1000)
reverse = compare(b, a, False, np.random.default_rng(2), 1000)
assert np.isclose(forward["effect"], -reverse["effect"])
assert np.isclose(forward["rank_biserial"], -reverse["rank_biserial"])
try:
    compare(a, b[:-1], True, np.random.default_rng(0), 10)
except ValueError:
    pass
else:
    raise AssertionError("Unmatched pair accepted")
print("Holm, paired direction, bootstrap difference and effect sign checks passed.")
