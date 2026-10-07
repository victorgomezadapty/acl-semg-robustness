"""Analytical checks for amplitude definitions and block remainder handling."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np

from src.features.amplitude import ratio, summarize

x = np.array([-3.0, 4.0])
r = summarize(x, block_sizes=(2,))
assert np.isclose(r["rms_V"], np.sqrt(12.5))
assert r["mav_V"] == 3.5 and r["peak_abs_V"] == 4.0
assert summarize(-x, block_sizes=(2,)) == r
constant = summarize(np.full(513, 2.0))
assert constant["block512_count"] == 1 and constant["block512_remainder_samples"] == 1
assert constant["rms_V"] == 2 and constant["block512_median_rms_V"] == 2
assert np.isnan(ratio(1, 0))
for invalid in [[], [np.nan], [[1, 2]]]:
    try:
        summarize(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid signal accepted")
print(
    "Amplitude definitions, sign invariance, remainder and zero-denominator checks passed."
)
