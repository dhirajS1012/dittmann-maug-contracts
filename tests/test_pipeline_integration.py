from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src/py"))

import pipeline as pipeline_module
from schemas import ExecuCompTables, RunConfig


def _build_synthetic_tables() -> ExecuCompTables:
    anncomp_rows = []
    coperol_rows = []
    for year in [1995, 1996, 1997, 1998, 1999, 2000]:
        anncomp_rows.append(
            {
                "co_per_rol": 1,
                "year": year,
                "salary": 1000.0,
                "bonus": 100.0,
                "othann": 10.0,
                "allothtot": 5.0,
                "ltip": 20.0,
                "shrown": 100.0,
                "pinclopt": "FALSE",
                "rstkgrnt": 0.0,
                "rstkhld": 0.0,
                "soptexer": 0.0,
                "soptexsh": 0.0,
                "uexnumun": 0.0,
                "uexnumex": 0.0,
                "inmonun": 0.0,
                "inmonex": 0.0,
            }
        )
        coperol_rows.append(
            {
                "co_per_rol": 1,
                "year": year,
                "execid": 10,
                "permid": 20,
                "ceoann": "CEO" if year == 2000 else "NON-CEO",
            }
        )

    codirfin_rows = []
    for year in [1995, 1996, 1997, 1998, 1999]:
        codirfin_rows.append(
            {
                "permid": 20,
                "year": year,
                "prccf": 50.0,
                "ajex": 1.0,
                "divyield": 2.0,
                "fyr": 12,
                "shrsout": 1000.0,
                "bs_volatility": 0.30,
            }
        )

    stgrttab_rows = [
        {
            "co_per_rol": 1,
            "year": 1999,
            "numsecur": 0.0,
            "expric": 0.0,
            "exdate": pd.Timestamp("2009-12-31"),
        }
    ]

    return ExecuCompTables(
        anncomp=pd.DataFrame(anncomp_rows),
        coperol=pd.DataFrame(coperol_rows),
        codirfin=pd.DataFrame(codirfin_rows),
        stgrttab=pd.DataFrame(stgrttab_rows),
    )


def test_run_pipeline_end_to_end(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "data_raw"
    output_dir = tmp_path / "output"
    synthetic_tables = _build_synthetic_tables()

    monkeypatch.setattr(pipeline_module, "missing_required_tables", lambda _config: {})
    monkeypatch.setattr(
        pipeline_module,
        "load_required_tables",
        lambda _config: synthetic_tables,
    )

    config = RunConfig(
        reference_year=1999,
        history_years=5,
        data_dir=data_dir,
        output_dir=output_dir,
    )
    result = pipeline_module.run_pipeline(config)

    assert not result.contracts.empty
    assert {"execid_num", "phi", "W0", "nS", "nO", "K", "T", "P0", "sigma", "d", "rf"}.issubset(
        result.contracts.columns
    )
    assert len(result.paper_table1) == 19
    assert not result.replicated_table1.empty
    assert not result.table1_diff.empty
    assert "sample_sizes:" in result.table1_stats_yaml
    assert "# Validation Report" in result.validation_report_markdown
