from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src/py"))

from contracts import _grow_wealth_across_years, _tax_rate_for_year


def test_tax_rate_mapping():
    assert math.isclose(_tax_rate_for_year(1992), 0.31)
    assert math.isclose(_tax_rate_for_year(1993), 0.396)
    assert math.isclose(_tax_rate_for_year(1994), 0.42)
    assert math.isclose(_tax_rate_for_year(2000), 0.42)


def test_wealth_growth_mapping():
    # Grow from 1998 to 2000 using R[1999]=4.51 and R[2000]=6.12
    grown = _grow_wealth_across_years(100.0, 1998, 2000)
    expected = 100.0 * (1 + 4.51 / 100.0) * (1 + 6.12 / 100.0)
    assert math.isclose(grown, expected, rel_tol=1e-12)
