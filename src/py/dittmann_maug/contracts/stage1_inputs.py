from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from dittmann_maug.validate import ColumnSpec, require_columns


@dataclass(frozen=True)
class Stage1Config:
    considered_year: int
    measurement_year: Optional[int] = None
    rf: Optional[float] = None

    def measurement_year_resolved(self) -> int:
        return self.measurement_year if self.measurement_year is not None else self.considered_year - 1


_TRUE_SET = {"1", "y", "yes", "t", "true", "ceo"}


def _flag_is_true(x) -> bool:
    if x is None:
        return False
    if isinstance(x, (int, np.integer)):
        return x != 0
    if isinstance(x, float) and np.isnan(x):
        return False
    s = str(x).strip().lower()
    return s in _TRUE_SET


def _ensure_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def build_stage1_contract_inputs(
    anncomp: pd.DataFrame,
    codirfin: pd.DataFrame,
    cfg: Stage1Config,
) -> pd.DataFrame:
    """Build the contract inputs we can compute without option detail and W0.

    Output columns:
    - gvkey, execid, considered_year
    - phi, ns
    - p0, d, sigma, rf
    - prccf_a, shrsout_a, ajex

    Units:
    - p0 is in thousands of dollars (matches SAS scaling with SHRSOUT * 1000).
    - ns is a fraction of shares outstanding.
    """

    # Required columns with common alternatives
    ann_map = require_columns(
        anncomp,
        [
            ColumnSpec("gvkey"),
            ColumnSpec("execid", ("exec_id", "executiveid")),
            ColumnSpec("year", ("fyear", "fiscyr")),
            ColumnSpec("salary"),
            ColumnSpec("bonus"),
            ColumnSpec("othann"),
            ColumnSpec("allothtot"),
            ColumnSpec("shrown", ("shrown_tot", "shrown_excl_opts")),
        ],
        table_name="anncomp",
    )

    # Optional columns
    ceo_col = "ceoann" if "ceoann" in anncomp.columns else None
    pinclopt_col = "pinclopt" if "pinclopt" in anncomp.columns else None

    fin_map = require_columns(
        codirfin,
        [
            ColumnSpec("gvkey"),
            ColumnSpec("year", ("fyear", "fiscyr")),
            ColumnSpec("prccf"),
            ColumnSpec("shrsout"),
            ColumnSpec("ajex"),
            ColumnSpec("divyield"),
            ColumnSpec("bs_volatility", ("bs_vol", "volatility")),
        ],
        table_name="codirfin",
    )

    considered_year = int(cfg.considered_year)
    measurement_year = int(cfg.measurement_year_resolved())

    ann = anncomp.copy()
    ann = ann[ann[ann_map["year"]] == considered_year]

    if ceo_col is not None:
        ann = ann[ann[ceo_col].apply(_flag_is_true)]

    # Exclude missing salary
    ann = _ensure_numeric(ann, [ann_map["salary"], ann_map["bonus"], ann_map["othann"], ann_map["allothtot"], ann_map["shrown"]])
    ann = ann[ann[ann_map["salary"]].notna()]

    if pinclopt_col is not None:
        ann = ann[~ann[pinclopt_col].apply(_flag_is_true)]

    fin = codirfin.copy()
    fin = fin[fin[fin_map["year"]] == measurement_year]
    fin = _ensure_numeric(fin, [fin_map["prccf"], fin_map["shrsout"], fin_map["ajex"], fin_map["divyield"], fin_map["bs_volatility"]])

    merged = ann.merge(
        fin[[fin_map["gvkey"], fin_map["prccf"], fin_map["shrsout"], fin_map["ajex"], fin_map["divyield"], fin_map["bs_volatility"]]],
        left_on=ann_map["gvkey"],
        right_on=fin_map["gvkey"],
        how="inner",
        suffixes=("", "_fin"),
    )

    # Handle AJEX
    ajex = merged[fin_map["ajex"]].copy()
    ajex = ajex.fillna(1.0)
    ajex = ajex.replace(0.0, 1.0)
    merged["ajex"] = ajex

    merged["prccf_a"] = merged[fin_map["prccf"]] / merged["ajex"]
    merged["shrsout_a"] = merged[fin_map["shrsout"]] * merged["ajex"]

    # Shares outstanding in thousands
    merged["shares_out_k"] = merged["shrsout_a"] * 1000.0

    merged["p0"] = merged["prccf_a"] * merged["shares_out_k"]
    merged["d"] = merged[fin_map["divyield"]] / 100.0
    merged["sigma"] = merged[fin_map["bs_volatility"]]

    # Shares owned adjusted for splits
    merged["shrown_a"] = merged[ann_map["shrown"]] * merged["ajex"]
    merged["ns"] = merged["shrown_a"] / merged["shares_out_k"]

    # Fixed pay, fill missing as 0 except salary
    for c in [ann_map["bonus"], ann_map["othann"], ann_map["allothtot"]]:
        merged[c] = merged[c].fillna(0.0)

    merged["phi"] = merged[ann_map["salary"]] + merged[ann_map["bonus"]] + merged[ann_map["othann"]] + merged[ann_map["allothtot"]]

    # rf
    rf = cfg.rf
    if rf is None:
        # Default for the paper's main sample: considered year 2000
        if considered_year == 2000:
            rf = 0.0664
        else:
            raise ValueError(
                "rf is not set. Pass --rf or extend the rf lookup for your target year."
            )

    merged["rf"] = float(rf)
    merged["considered_year"] = considered_year
    merged["measurement_year"] = measurement_year

    out_cols = [
        ann_map["gvkey"],
        ann_map["execid"],
        "considered_year",
        "measurement_year",
        "phi",
        "ns",
        "p0",
        "d",
        "sigma",
        "rf",
        "prccf_a",
        "shrsout_a",
        "shares_out_k",
        "ajex",
    ]

    out = merged[out_cols].rename(columns={ann_map["gvkey"]: "gvkey", ann_map["execid"]: "execid"})

    # Basic cleanup
    out = out.replace([np.inf, -np.inf], np.nan)
    out = out.dropna(subset=["p0", "sigma", "ns", "phi"])

    return out.reset_index(drop=True)
