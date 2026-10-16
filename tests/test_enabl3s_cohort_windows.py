import numpy as np
import pytest

from src.features.enabl3s_windows import (
    clean_trial,
    eligible_runs,
    selected_block_indices,
    time_matched_blocks,
)


def test_only_present_blank_notes_are_primary_eligible():
    assert clean_trial("  ")
    assert not clean_trial(None)
    assert not clean_trial("Late transition from LW to SA")
    assert not clean_trial("nan")


def test_duration_matching_and_rounding():
    assert time_matched_blocks((256, 512, 1024), 1925.9239, 1000) == (133, 266, 532)
    assert time_matched_blocks((1,), 2, 1) == (1,)


def test_guard_does_not_bridge_transition_and_preserves_indices():
    mode = np.r_[np.ones(5095), 2, np.ones(5096)]
    signal = np.ones(len(mode))
    assert eligible_runs(mode, signal, signal) == [
        {"raw_start": 5096, "raw_stop": 10192, "start": 5596, "stop": 9692}
    ]


def test_nonfinite_sample_breaks_walk_and_never_gets_interpolated():
    signal = np.ones(6000)
    signal[3000] = np.nan
    assert eligible_runs(np.ones(6000), signal, np.ones(6000)) == []


def test_shared_selection_is_undefined_if_limbs_select_disjoint_times():
    right, left = np.repeat([1.0, 10.0], 256), np.repeat([10.0, 1.0], 256)
    independent = selected_block_indices(right, left, 256, 0.2)
    assert independent[0].tolist() == [1]
    assert independent[1].tolist() == [0]
    common = selected_block_indices(right, left, 256, 0.2, shared=True)
    assert len(common[0]) == len(common[1]) == 0


def test_alignment_mismatch_is_rejected():
    with pytest.raises(ValueError):
        eligible_runs([1, 1], [1], [1, 1])
