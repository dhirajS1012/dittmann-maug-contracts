from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd


REQUIRED_TABLE_FILES: dict[str, str] = {
    "anncomp": "anncomp.parquet",
    "coperol": "coperol.parquet",
    "codirfin": "codirfin.parquet",
    "stgrttab": "stgrttab.parquet",
}


@dataclass(frozen=True)
class RunConfig:
    reference_year: int
    history_years: int
    data_dir: Path = field(default_factory=lambda: Path("data/raw"))
    output_dir: Path = field(default_factory=lambda: Path("output"))

    @property
    def measurement_year(self) -> int:
        return self.reference_year + 1


@dataclass(frozen=True)
class ExecuCompTables:
    anncomp: pd.DataFrame
    coperol: pd.DataFrame
    codirfin: pd.DataFrame
    stgrttab: pd.DataFrame


@dataclass(frozen=True)
class PipelineResult:
    contracts: pd.DataFrame
    paper_table1: pd.DataFrame
    replicated_table1: pd.DataFrame
    table1_diff: pd.DataFrame
    table1_stats_yaml: str
    validation_report_markdown: str


@dataclass(frozen=True)
class ContractParameters:
    execid: int
    permid: int
    reference_year: int
    measurement_year: int
    phi: Optional[float] = None
    w0: Optional[float] = None
    ns: Optional[float] = None
    no: Optional[float] = None
    k: Optional[float] = None
    t: Optional[float] = None
    p0: Optional[float] = None
    sigma: Optional[float] = None
    d: Optional[float] = None
    rf: Optional[float] = None
    error_code: Optional[int] = None
