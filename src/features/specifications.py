"""Explicit amplitude specifications; undefined selections return NaN."""

import numpy as np

from src.features.amplitude import summarize


def specifications(x):
    x = np.asarray(x, dtype=float)
    s = summarize(x)
    values = {
        "whole_RMS": s["rms_V"],
        "whole_MAV": s["mav_V"],
        "cap995_RMS": s["rms_cap995_V_sensitivity"],
    }
    for size in (256, 512, 1024):
        blocks = x[: len(x) // size * size].reshape(-1, size)
        rms = np.sqrt(np.mean(blocks * blocks, axis=1))
        if len(rms):
            lo, hi = np.quantile(rms, [0.2, 0.9])
        else:
            lo = hi = np.nan
        for f in (0.1, 0.2, 0.3):
            selected = blocks[rms > lo + f * (hi - lo)].ravel()
            # Strict > is retained from the original protocol. Constant blocks
            # have no selected values and are reported as undefined.
            for metric in ("RMS", "MAV"):
                values[f"block{size}_f{f}_{metric}"] = (
                    (
                        float(np.sqrt(np.mean(selected**2)))
                        if metric == "RMS"
                        else float(np.mean(np.abs(selected)))
                    )
                    if len(selected)
                    else np.nan
                )
    return values
