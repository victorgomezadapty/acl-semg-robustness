"""Protect against combining different tasks or bridging invalid samples."""

from scripts.analyze_enabl3s_pilot import first_segment


def rows(count, mode=1, right="2", left="1"):
    return [
        {"Mode": str(mode), "Right_VL": right, "Left_VL": left} for _ in range(count)
    ]


def test_short_segments_are_not_concatenated_across_other_tasks():
    assert first_segment(iter(rows(1500) + rows(1, mode=2) + rows(1500))) is None


def test_nonfinite_channel_breaks_segment_and_indices_remain_original():
    selected = first_segment(iter(rows(1500) + rows(1, left="nan") + rows(2048)))
    assert selected[0:2] == (1501, 3549)
    assert len(selected[2]) == len(selected[3]) == 2048


def test_first_eligible_segment_is_retained_instead_of_longest():
    selected = first_segment(iter(rows(2048) + rows(1, mode=0) + rows(3000)))
    assert selected[0:2] == (0, 2048)
