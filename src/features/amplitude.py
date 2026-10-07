"""Time-independent amplitude summaries; no physiological normalization."""

import numpy as np


def center_signal(signal):
    """Remove the record mean without modifying input; not a band-pass filter."""
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError("A nonempty finite one-dimensional signal is required.")
    return x - x.mean()


def summarize(signal, block_sizes=(256, 512, 1024)):
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError("A nonempty finite one-dimensional signal is required.")
    magnitude = np.abs(x)
    cap = np.quantile(magnitude, 0.995)
    result = {
        "rms_V": float(np.sqrt(np.mean(x * x))),
        "mav_V": float(magnitude.mean()),
        "median_abs_V": float(np.median(magnitude)),
        "p95_abs_V": float(np.quantile(magnitude, 0.95)),
        "peak_abs_V": float(magnitude.max()),
        "rms_cap995_V_sensitivity": float(
            np.sqrt(np.mean(np.minimum(magnitude, cap) ** 2))
        ),
    }
    for size in block_sizes:
        count = len(x) // size
        if count:
            blocks = x[: count * size].reshape(count, size)
            rms = np.sqrt(np.mean(blocks**2, axis=1))
            result.update(
                {
                    f"block{size}_count": count,
                    f"block{size}_remainder_samples": len(x) % size,
                    f"block{size}_median_rms_V": float(np.median(rms)),
                    f"block{size}_p90_rms_V": float(np.quantile(rms, 0.9)),
                }
            )
    return result


def ratio(numerator, denominator):
    return float(numerator / denominator) if denominator > 0 else float("nan")
