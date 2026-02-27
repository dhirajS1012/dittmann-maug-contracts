from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src/py"))

from reporting import paper_table1_reference


def test_paper_table1_reference_shape():
    paper = paper_table1_reference()
    assert len(paper) == 19
    assert set(paper["panel"]) == {"A", "B"}


def test_paper_table1_reference_key_values():
    paper = paper_table1_reference()
    a_phi = paper[(paper["panel"] == "A") & (paper["symbol"] == "phi")].iloc[0]
    b_sigma = paper[(paper["panel"] == "B") & (paper["symbol"] == "sigma")].iloc[0]

    assert math.isclose(float(a_phi["mean"]), 2037.0)
    assert math.isclose(float(b_sigma["mean"]), 0.435)
