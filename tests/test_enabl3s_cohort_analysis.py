import numpy as np

from scripts.analyze_enabl3s_cohort import canonical, evaluate
from src.features.specifications import specifications


def test_primary_preserves_original_algorithm_on_nonconstant_data():
    rng = np.random.default_rng(84721)
    right = rng.normal(size=6000)
    left = rng.normal(size=6000) * 0.6
    report = evaluate(right, left, (256, 512, 1024), (0.1, 0.2, 0.3), original=True)
    original_right, original_left = specifications(right), specifications(left)
    assert report["status"] == "complete"
    for row in report["specifications"]:
        assert (
            row["ratio"] == original_right[row["method"]] / original_left[row["method"]]
        )


def test_no_shared_selection_does_not_become_zero_or_complete_range():
    right = np.repeat([1.0, 10.0], 3000)
    left = np.repeat([10.0, 1.0], 3000)
    report = evaluate(right, left, (256, 512, 1024), (0.1, 0.2, 0.3), shared=True)
    assert report["status"] == "partial"
    assert report["log_ratio_range"] is None
    assert any(row["ratio"] is None for row in report["specifications"])


def test_zero_denominator_is_explicit_and_json_safe():
    report = evaluate(np.ones(6000), np.zeros(6000), (133, 266, 532), (0.1, 0.2, 0.3))
    assert report["defined_positive_ratios"] == 0
    assert report["specifications"][0]["undefined_reason"] == "nonpositive_denominator"


def test_source_metadata_paths_match_across_platforms():
    assert canonical(r"AB156\Processed\AB156_Circuit_001_post.csv") == canonical(
        "AB156_Circuit_001.csv"
    )
