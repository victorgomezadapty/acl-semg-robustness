"""Deterministic cohort window rules; separate from the preserved pilot."""

import math

import numpy as np


def clean_trial(notes):
    """Only a present, empty source note qualifies; no absence-of-artifact claim."""
    return isinstance(notes, str) and not notes.strip()


def time_matched_blocks(reference_sizes, reference_rate, target_rate):
    """Round to nearest sample, with exact half rounded up."""
    if reference_rate <= 0 or target_rate <= 0:
        raise ValueError("Sampling rates must be positive.")
    return tuple(
        math.floor(size * target_rate / reference_rate + 0.5)
        for size in reference_sizes
    )


def eligible_runs(mode, right, left, guard=500, minimum=4096):
    """Return original and trimmed bounds; trim every finite walking-run edge."""
    mode, right, left = (np.asarray(v, dtype=float) for v in (mode, right, left))
    if mode.ndim != 1 or mode.shape != right.shape or mode.shape != left.shape:
        raise ValueError("Aligned one-dimensional channels are required.")
    if guard < 0 or minimum <= 0:
        raise ValueError("Guard must be nonnegative and minimum positive.")
    mask = (mode == 1) & np.isfinite(right) & np.isfinite(left)
    edges = np.diff(np.r_[False, mask, False].astype(int))
    runs = []
    for start, stop in zip(
        np.flatnonzero(edges == 1), np.flatnonzero(edges == -1), strict=True
    ):
        trimmed_start, trimmed_stop = int(start + guard), int(stop - guard)
        if trimmed_stop - trimmed_start >= minimum:
            runs.append(
                {
                    "raw_start": int(start),
                    "raw_stop": int(stop),
                    "start": trimmed_start,
                    "stop": trimmed_stop,
                }
            )
    return runs


def selected_block_indices(right, left, block_size, factor, shared=False):
    """Expose paired-selection sensitivity without changing the primary rule."""
    right, left = np.asarray(right, dtype=float), np.asarray(left, dtype=float)
    if (
        right.ndim != 1
        or right.shape != left.shape
        or not np.isfinite([right, left]).all()
    ):
        raise ValueError("Aligned finite channels are required.")
    if block_size <= 0 or not 0 <= factor <= 1:
        raise ValueError("Invalid block size or threshold factor.")
    count = len(right) // block_size
    if not count:
        return np.array([], dtype=int), np.array([], dtype=int)
    selections = []
    for signal in (right, left):
        blocks = signal[: count * block_size].reshape(count, block_size)
        amplitudes = np.sqrt(np.mean(blocks**2, axis=1))
        low, high = np.quantile(amplitudes, [0.2, 0.9])
        selections.append(np.flatnonzero(amplitudes > low + factor * (high - low)))
    if shared:
        common = np.intersect1d(*selections)
        return common, common.copy()
    return tuple(selections)
