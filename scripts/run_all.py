"""Offline analysis pipeline; delivery generation is an explicit optional step."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delivery", action="store_true")
    parser.add_argument("--verify-delivery", action="store_true")
    args = parser.parse_args()
    for folder in ("reports/figures/profiles", "data/processed"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    scripts = [
        "inspect_dataset.py",
        "check_amplitude.py",
        "check_statistics.py",
        "review_signals.py",
        "exploratory_amplitude.py",
        "comprehensive_semg.py",
        "evaluate_robustness.py",
        "evaluate_centering.py",
        "evaluate_bandpass.py",
        "simulate_measurement_scenarios.py",
        "build_analysis_report.py",
    ]
    if args.delivery or args.verify_delivery:
        scripts.append("prepare_kaggle.py")
    if args.verify_delivery:
        scripts.append("verify_kaggle_delivery.py")
    for script in scripts:
        print("Running", script, flush=True)
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script)],
            cwd=ROOT,
            check=True,
            env={**os.environ, "MPLCONFIGDIR": str(ROOT / ".mpl-cache")},
        )


if __name__ == "__main__":
    main()
