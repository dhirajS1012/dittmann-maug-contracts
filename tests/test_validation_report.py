from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src/py"))

from reporting import build_table1_diff_table, build_validation_report_markdown
from schemas import RunConfig


def test_validation_report_contains_status_sections():
    paper = pd.DataFrame(
        [
            {
                "panel": "A",
                "variable": "Base salary ($'000)",
                "symbol": "phi",
                "mean": 2000.0,
                "median": 1000.0,
                "std_dev": 100.0,
                "min": 10.0,
                "max": 9000.0,
                "t_test": None,
            }
        ]
    )
    replicated = pd.DataFrame(
        [
            {
                "panel": "A",
                "variable": "Base salary ($'000)",
                "symbol": "phi",
                "mean": 1900.0,
                "median": 950.0,
                "std_dev": 120.0,
                "min": 5.0,
                "max": 8800.0,
                "t_test": None,
            }
        ]
    )

    diff = build_table1_diff_table(paper=paper, replicated=replicated)
    report = build_validation_report_markdown(
        diff_table=diff,
        panel_a_n=10,
        panel_b_n=12,
        config=RunConfig(reference_year=1999, history_years=5),
    )

    assert "# Validation Report" in report
    assert "## Status" in report
    assert "Sample-size check" in report
    assert "Largest Mean Gaps" in report
