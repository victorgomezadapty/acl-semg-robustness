import hashlib
import runpy
import zipfile
from pathlib import Path

import numpy as np
import pytest

from src.data.semg import recordings
from src.features.amplitude import center_signal, summarize
from src.features.specifications import specifications

ROOT = Path(__file__).resolve().parents[1]


def test_specifications_known_blocks_and_common_gain():
    signal = np.r_[np.tile([-1.0, 1.0], 512), np.tile([-2.0, 2.0], 512)]
    values = specifications(signal)
    assert len(values) == 21
    assert sum(name.endswith("RMS") for name in values) == 11
    assert np.isclose(values["whole_RMS"], np.sqrt(2.5))
    assert values["block1024_f0.2_RMS"] == 2
    assert values["block1024_f0.2_MAV"] == 2
    scaled = specifications(signal * 7)
    assert all(np.isclose(scaled[name], value * 7) for name, value in values.items())


def test_specifications_short_and_constant_selection_are_undefined():
    short = specifications(np.array([-1.0, 1.0]))
    assert short["whole_RMS"] == 1
    assert np.isnan(short["block256_f0.1_RMS"])
    constant = specifications(np.ones(2048))
    assert constant["whole_RMS"] == 1
    assert np.isnan(constant["block1024_f0.2_RMS"])


@pytest.mark.parametrize("script", ["check_amplitude.py", "check_statistics.py"])
def test_analytical_regressions(script):
    runpy.run_path(str(ROOT / "scripts" / script))


def test_centering_offset_and_energy_identity():
    x = np.array([-3.0, -1.0, 1.0, 3.0])
    shifted = x + 12
    copy = shifted.copy()
    assert np.allclose(center_signal(shifted), x)
    assert np.array_equal(shifted, copy)
    assert np.isclose(
        summarize(shifted)["rms_V"] ** 2,
        summarize(center_signal(shifted))["rms_V"] ** 2 + shifted.mean() ** 2,
    )
    assert np.isclose(
        summarize(center_signal(0.8 * x + 12))["rms_V"]
        / summarize(center_signal(x - 7))["rms_V"],
        0.8,
    )


@pytest.mark.parametrize("values", [[], [np.nan], [[1, 2]]])
def test_centering_rejects_invalid(values):
    with pytest.raises(ValueError):
        center_signal(values)


def test_verified_loader_padding_and_internal_gap(tmp_path):
    archive = tmp_path / "small.zip"

    def create(body):
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("healthy_iso90_inv.csv", body)
            z.writestr("healthy_iso90_inv_time.csv", "time\n0\n1\n2\n")
        return hashlib.sha256(archive.read_bytes()).hexdigest()

    digest = create("healthy1\n1\n-1\n\n")
    result = list(recordings(archive, expected_hash=digest))
    assert result[0]["padding_removed"] == 1
    assert np.array_equal(result[0]["semg_V"], [1, -1])
    with pytest.raises(ValueError, match="pinned"):
        list(recordings(archive))
    digest = create("healthy1\n1\n\n-1\n")
    with pytest.raises(ValueError, match="internal gap"):
        list(recordings(archive, expected_hash=digest))
