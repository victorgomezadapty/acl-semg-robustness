"""Signal-quality helpers: clock-derived sampling rate, band-pass and pair validity."""

import numpy as np
from scipy import signal as sps

EMG_BAND_HZ = (20.0, 450.0)
SHORT_RECORD_FRACTION = 0.25


def sampling_rate_from_clock(times):
    """Average rate over the whole record: (samples - 1) / elapsed seconds.

    Validates nondecreasing timestamps; duplicates are retained. Endpoint span
    estimates an average rate, not uniform acquisition or the cause of duplicates.
    """
    t = np.asarray(times, dtype=float)
    if t.ndim != 1 or len(t) < 2 or not np.isfinite(t).all():
        raise ValueError("At least two finite timestamps are required.")
    if np.any(np.diff(t) < 0):
        raise ValueError("Clock timestamps must not go backwards.")
    elapsed = t[-1] - t[0]
    if elapsed <= 0:
        raise ValueError("Clock does not advance.")
    return float((len(t) - 1) / elapsed)


def bandpass(signal, fs, band=EMG_BAND_HZ, order=4):
    """Butterworth prototype N=order, SOS band-pass, forward/backward filtering.

    N=4 gives order 8 band-pass per direction, effective order 16 after both
    passes. Input is preserved; sampling uniformity remains an explicit assumption.
    """
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or not len(x) or not np.isfinite(x).all():
        raise ValueError("A nonempty finite one-dimensional signal is required.")
    if not 0 < band[0] < band[1] < fs / 2:
        raise ValueError("Band edges must lie between 0 and Nyquist.")
    sos = sps.butter(order, band, btype="band", fs=fs, output="sos")
    return sps.sosfiltfilt(sos, x)


def rms_retention_ratio(signal, fs, band=EMG_BAND_HZ):
    """RMS of the band-passed signal divided by RMS of the mean-centered signal.

    Measures RMS retention under this filter, including transition attenuation
    and edge effects. Its square is the filtered/centered mean-square ratio;
    neither quantity directly partitions energy into inside/outside the band.
    """
    x = np.asarray(signal, dtype=float)
    centered = x - x.mean()
    total = np.sqrt(np.mean(centered * centered))
    if total == 0:
        return float("nan")
    filtered = bandpass(x, fs, band)
    return float(np.sqrt(np.mean(filtered * filtered)) / total)


def short_records(rows, fraction=SHORT_RECORD_FRACTION):
    """Keys (participant, condition, limb) shorter than a fraction of the
    cohort-condition median length. Rows need participant_id, cohort,
    condition, limb_label and samples."""
    rows = list(rows)
    medians = {}
    for r in rows:
        medians.setdefault((r["cohort"], r["condition"]), []).append(int(r["samples"]))
    medians = {k: float(np.median(v)) for k, v in medians.items()}
    return {
        (r["participant_id"], r["condition"], r["limb_label"])
        for r in rows
        if int(r["samples"]) < fraction * medians[r["cohort"], r["condition"]]
    }


def excluded_pairs(rows, fraction=SHORT_RECORD_FRACTION):
    """Participant-condition pairs left out of the primary presentation because
    one limb record is too short for a whole-record bilateral ratio."""
    return {(p, c) for p, c, _ in short_records(rows, fraction)}
