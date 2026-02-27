from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from schemas import ExecuCompTables, RunConfig

PAPER_PANEL_A_N = 598
PAPER_PANEL_B_N = 1417
MEAN_PCT_DIFF_TOLERANCE = 20.0


def _summary_stats(series: pd.Series) -> dict[str, float]:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return {
            "mean": float("nan"),
            "median": float("nan"),
            "std_dev": float("nan"),
            "min": float("nan"),
            "max": float("nan"),
        }
    return {
        "mean": float(clean.mean()),
        "median": float(clean.median()),
        "std_dev": float(clean.std(ddof=1)),
        "min": float(clean.min()),
        "max": float(clean.max()),
    }


def _measurement_year_panel(
    tables: ExecuCompTables,
    measurement_year: int,
) -> pd.DataFrame:
    a1 = tables.anncomp.merge(
        tables.coperol,
        on=["co_per_rol", "year"],
        how="outer",
        suffixes=("", "_coperol"),
    )
    panel = a1.loc[
        (a1["year"] == measurement_year) & (a1["ceoann"] == "CEO")
    ].copy()
    return panel


def _reference_year_holdings_panel(
    tables: ExecuCompTables,
    reference_year: int,
) -> pd.DataFrame:
    a1 = tables.anncomp.merge(
        tables.coperol,
        on=["co_per_rol", "year"],
        how="outer",
        suffixes=("", "_coperol"),
    )
    panel = a1.loc[a1["year"] == reference_year].copy()
    return panel


def _find_age_series(frame: pd.DataFrame) -> pd.Series:
    for candidate in ["age", "exec_age", "age_years"]:
        if candidate in frame.columns:
            return pd.to_numeric(frame[candidate], errors="coerce")
    return pd.Series(np.nan, index=frame.index, dtype=float)


def _build_panel_b_dataset(
    tables: ExecuCompTables,
    config: RunConfig,
) -> pd.DataFrame:
    measurement_panel = _measurement_year_panel(tables, config.measurement_year)
    reference_panel = _reference_year_holdings_panel(tables, config.reference_year)
    codirfin_cols = ["permid", "prccf", "ajex", "shrsout", "bs_volatility"]
    if "mktval" in tables.codirfin.columns:
        codirfin_cols.append("mktval")
    codirfin_ref = tables.codirfin.loc[
        tables.codirfin["year"] == config.reference_year,
        codirfin_cols,
    ].copy()
    if "mktval" not in codirfin_ref.columns:
        codirfin_ref["mktval"] = float("nan")

    panel_b_cols = ["co_per_rol", "execid", "permid", "salary", "bonus", "othann", "allothtot"]
    panel_b = measurement_panel[
        [col for col in panel_b_cols if col in measurement_panel.columns]
    ].copy()
    for col in ["salary", "bonus", "othann", "allothtot"]:
        if col not in panel_b.columns:
            panel_b[col] = 0.0
    panel_b["age"] = _find_age_series(measurement_panel)
    panel_b["phi"] = (
        pd.to_numeric(panel_b["salary"], errors="coerce")
        + pd.to_numeric(panel_b["bonus"], errors="coerce")
        + pd.to_numeric(panel_b["othann"], errors="coerce")
        + pd.to_numeric(panel_b["allothtot"], errors="coerce")
    )

    ref_cols = ["co_per_rol", "shrown", "uexnumun", "uexnumex"]
    if "shrown_excl_opts_pct" in reference_panel.columns:
        ref_cols.append("shrown_excl_opts_pct")
    panel_b = panel_b.merge(reference_panel[ref_cols], on="co_per_rol", how="left")
    panel_b = panel_b.merge(codirfin_ref, on="permid", how="left")

    for col in [
        "shrown",
        "uexnumun",
        "uexnumex",
        "shrown_excl_opts_pct",
        "prccf",
        "ajex",
        "shrsout",
        "mktval",
    ]:
        if col in panel_b.columns:
            panel_b[col] = pd.to_numeric(panel_b[col], errors="coerce")

    panel_b["shrown_a"] = panel_b["shrown"] * panel_b["ajex"]
    panel_b["shrsout_a"] = panel_b["shrsout"] * panel_b["ajex"]
    panel_b["num_of_shares_th"] = panel_b["shrsout_a"] * 1000.0
    panel_b["num_of_shares"] = panel_b["shrsout_a"] * 1_000_000.0
    panel_b["prccf_a"] = panel_b["prccf"] / panel_b["ajex"]
    p0_from_price = panel_b["prccf_a"] * panel_b["num_of_shares"]
    p0_from_mktval = panel_b["mktval"] * 1_000_000.0
    panel_b["p0"] = np.where(p0_from_mktval.notna(), p0_from_mktval, p0_from_price)

    ns_from_shares = panel_b["shrown_a"] / panel_b["num_of_shares_th"]
    if "shrown_excl_opts_pct" in panel_b.columns:
        ns_from_pct = panel_b["shrown_excl_opts_pct"] / 100.0
        panel_b["ns"] = np.where(ns_from_pct.notna(), ns_from_pct, ns_from_shares)
    else:
        panel_b["ns"] = ns_from_shares

    panel_b["no"] = (
        (panel_b["uexnumun"] + panel_b["uexnumex"]) * panel_b["ajex"]
    ) / panel_b["num_of_shares_th"]
    panel_b["value_stock_m"] = panel_b["ns"] * panel_b["p0"] / 1_000_000.0
    panel_b["market_value_m"] = panel_b["p0"] / 1_000_000.0
    panel_b["sigma"] = panel_b["bs_volatility"]
    panel_b = panel_b[
        panel_b["ns"].ge(0.0)
        & panel_b["ns"].le(1.0)
        & panel_b["no"].ge(0.0)
        & panel_b["no"].le(1.0)
    ].copy()
    return panel_b


def _build_panel_a_age(
    contracts: pd.DataFrame,
    tables: ExecuCompTables,
    config: RunConfig,
) -> pd.Series:
    if contracts.empty:
        return pd.Series(dtype=float)

    measurement_panel = _measurement_year_panel(tables, config.measurement_year)
    age_map = measurement_panel[["execid", "permid"]].copy()
    age_map["age"] = _find_age_series(measurement_panel)
    age_map = age_map.drop_duplicates(["execid", "permid"], keep="first")

    enriched = contracts.merge(
        age_map,
        left_on=["execid_num", "permid"],
        right_on=["execid", "permid"],
        how="left",
    )
    return pd.to_numeric(enriched["age"], errors="coerce")


def _summary_row(
    *,
    panel: str,
    variable: str,
    symbol: str,
    series: pd.Series,
    t_test: float | None = None,
) -> dict[str, Any]:
    stats = _summary_stats(series)
    return {
        "panel": panel,
        "variable": variable,
        "symbol": symbol,
        "mean": stats["mean"],
        "median": stats["median"],
        "std_dev": stats["std_dev"],
        "min": stats["min"],
        "max": stats["max"],
        "t_test": t_test,
    }


def build_replicated_table1(
    contracts: pd.DataFrame,
    tables: ExecuCompTables,
    config: RunConfig,
) -> tuple[pd.DataFrame, int, int]:
    panel_a_n = int(len(contracts))
    panel_b = _build_panel_b_dataset(tables, config)
    panel_b_n = int(len(panel_b))

    panel_a_age = _build_panel_a_age(contracts, tables, config)

    panel_a_rows = [
        _summary_row(
            panel="A",
            variable="Base salary ($'000)",
            symbol="phi",
            series=contracts["phi"],
        ),
        _summary_row(
            panel="A",
            variable="Stock (%)",
            symbol="nS",
            series=contracts["nS"] * 100.0,
        ),
        _summary_row(
            panel="A",
            variable="Options (%)",
            symbol="nO",
            series=contracts["nO"] * 100.0,
        ),
        _summary_row(
            panel="A",
            variable="Options adjusted (%)",
            symbol="nOexp(-dT)",
            series=contracts["nO"] * np.exp(-contracts["d"] * contracts["T"]) * 100.0,
        ),
        _summary_row(
            panel="A",
            variable="Value of stock ($ m)",
            symbol="nSP0",
            series=contracts["nS"] * contracts["P0"] / 1_000_000.0,
        ),
        _summary_row(
            panel="A",
            variable="Value of options ($ m)",
            symbol="nOBS",
            series=contracts["nO"] * contracts["BS"] / 1_000_000.0,
        ),
        _summary_row(
            panel="A",
            variable="Market value ($ m)",
            symbol="P0",
            series=contracts["P0"] / 1_000_000.0,
        ),
        _summary_row(
            panel="A",
            variable="Wealth ($ m)",
            symbol="W0",
            series=contracts["W0"] / 1_000.0,
        ),
        _summary_row(
            panel="A",
            variable="Option delta",
            symbol="N(d1)",
            series=contracts["Nd1"],
        ),
        _summary_row(
            panel="A",
            variable="Maturity (years)",
            symbol="T",
            series=contracts["T"],
        ),
        _summary_row(
            panel="A",
            variable="Volatility",
            symbol="sigma",
            series=contracts["sigma"],
        ),
        _summary_row(
            panel="A",
            variable="Age of CEO",
            symbol="age",
            series=panel_a_age,
        ),
    ]

    panel_b_rows = [
        _summary_row(
            panel="B",
            variable="Base salary ($'000)",
            symbol="phi",
            series=panel_b["phi"],
        ),
        _summary_row(
            panel="B",
            variable="Stock (%)",
            symbol="nS",
            series=panel_b["ns"] * 100.0,
        ),
        _summary_row(
            panel="B",
            variable="Options (%)",
            symbol="nO",
            series=panel_b["no"] * 100.0,
        ),
        _summary_row(
            panel="B",
            variable="Value of stock ($ m)",
            symbol="nSP0",
            series=panel_b["value_stock_m"],
        ),
        _summary_row(
            panel="B",
            variable="Market value ($ m)",
            symbol="P0",
            series=panel_b["market_value_m"],
        ),
        _summary_row(
            panel="B",
            variable="Stock price volatility",
            symbol="sigma",
            series=panel_b["sigma"],
        ),
        _summary_row(
            panel="B",
            variable="Age of CEO",
            symbol="age",
            series=panel_b["age"],
        ),
    ]

    replicated = pd.DataFrame(panel_a_rows + panel_b_rows)
    return replicated, panel_a_n, panel_b_n


def paper_table1_reference() -> pd.DataFrame:
    rows = [
        # Panel A
        ("A", "Base salary ($'000)", "phi", 2037.0, 1261.0, 2570.0, 97.0, 22109.0, np.nan),
        ("A", "Stock (%)", "nS", 2.29, 0.29, 6.00, 0.00, 46.34, np.nan),
        ("A", "Options (%)", "nO", 1.29, 0.84, 1.82, 0.00, 24.32, np.nan),
        ("A", "Options adjusted (%)", "nOexp(-dT)", 1.22, 0.76, 1.79, 0.00, 24.32, np.nan),
        ("A", "Value of stock ($ m)", "nSP0", 91.98, 6.62, 571.95, 0.00, 11814.08, np.nan),
        ("A", "Value of options ($ m)", "nOBS", 29.47, 6.11, 104.42, 0.00, 1334.43, np.nan),
        ("A", "Market value ($ m)", "P0", 9857.0, 1668.0, 27845.0, 7.0, 280114.0, np.nan),
        ("A", "Wealth ($ m)", "W0", 34.60, 6.86, 234.79, 0.03, 5431.72, np.nan),
        ("A", "Option delta", "N(d1)", 0.834, 0.856, 0.126, 0.001, 1.000, np.nan),
        ("A", "Maturity (years)", "T", 5.89, 5.54, 1.96, 1.20, 22.18, np.nan),
        ("A", "Volatility", "sigma", 0.377, 0.335, 0.196, 0.136, 3.487, np.nan),
        ("A", "Age of CEO", "age", 57.0, 57.0, 7.0, 36.0, 84.0, np.nan),
        # Panel B
        ("B", "Base salary ($'000)", "phi", 1718.0, 1059.0, 3150.0, 0.0, 90000.0, 3.43),
        ("B", "Stock (%)", "nS", 2.97, 0.35, 6.78, 0.00, 56.42, -3.32),
        ("B", "Options (%)", "nO", 1.45, 0.96, 1.88, 0.00, 27.93, -2.74),
        ("B", "Value of stock ($ m)", "nSP0", 132.44, 6.45, 1385.87, 0.00, 47838.75, -1.07),
        ("B", "Market value ($ m)", "P0", 8012.0, 1256.0, 27551.0, 7.0, 508329.0, 2.15),
        ("B", "Stock price volatility", "sigma", 0.435, 0.384, 0.205, 0.136, 3.487, -9.36),
        ("B", "Age of CEO", "age", 55.0, 55.0, 8.0, 29.0, 86.0, 7.41),
    ]
    return pd.DataFrame(
        rows,
        columns=[
            "panel",
            "variable",
            "symbol",
            "mean",
            "median",
            "std_dev",
            "min",
            "max",
            "t_test",
        ],
    )


def _format_yaml_scalar(value: Any) -> str:
    if isinstance(value, float):
        if math.isnan(value):
            return "null"
        return f"{value:.6g}"
    if value is None:
        return "null"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return str(value)


def build_table1_stats_yaml(
    *,
    paper: pd.DataFrame,
    replicated: pd.DataFrame,
    panel_a_n: int,
    panel_b_n: int,
) -> str:
    merged = paper.merge(
        replicated,
        on=["panel", "variable", "symbol"],
        suffixes=("_paper", "_rep"),
        how="left",
    )
    merged["mean_abs_diff"] = (merged["mean_rep"] - merged["mean_paper"]).abs()
    merged["mean_pct_diff"] = np.where(
        merged["mean_paper"].abs() > 0,
        (merged["mean_rep"] - merged["mean_paper"]) / merged["mean_paper"] * 100.0,
        np.nan,
    )

    lines = []
    lines.append("sample_sizes:")
    lines.append(f"  panel_a: {panel_a_n}")
    lines.append(f"  panel_b: {panel_b_n}")
    lines.append("mean_comparison:")

    for _, row in merged.iterrows():
        key = f"{row['panel']}_{row['symbol']}_{row['variable']}".lower()
        key = "".join(ch if ch.isalnum() else "_" for ch in key)
        lines.append(f"  {key}:")
        lines.append(f"    paper_mean: {_format_yaml_scalar(row['mean_paper'])}")
        lines.append(f"    replicated_mean: {_format_yaml_scalar(row['mean_rep'])}")
        lines.append(f"    abs_diff: {_format_yaml_scalar(row['mean_abs_diff'])}")
        lines.append(f"    pct_diff: {_format_yaml_scalar(row['mean_pct_diff'])}")

    overall_abs = merged["mean_abs_diff"].dropna()
    lines.append("overall:")
    if overall_abs.empty:
        lines.append("  mean_abs_diff: null")
        lines.append("  max_abs_diff: null")
    else:
        lines.append(f"  mean_abs_diff: {_format_yaml_scalar(float(overall_abs.mean()))}")
        lines.append(f"  max_abs_diff: {_format_yaml_scalar(float(overall_abs.max()))}")

    return "\n".join(lines) + "\n"


def build_table1_diff_table(
    *,
    paper: pd.DataFrame,
    replicated: pd.DataFrame,
) -> pd.DataFrame:
    merged = paper.merge(
        replicated,
        on=["panel", "variable", "symbol"],
        suffixes=("_paper", "_rep"),
        how="left",
    )
    for metric in ["mean", "median", "std_dev", "min", "max"]:
        merged[f"{metric}_abs_diff"] = (
            merged[f"{metric}_rep"] - merged[f"{metric}_paper"]
        ).abs()
        merged[f"{metric}_pct_diff"] = np.where(
            merged[f"{metric}_paper"].abs() > 0,
            (merged[f"{metric}_rep"] - merged[f"{metric}_paper"])
            / merged[f"{metric}_paper"]
            * 100.0,
            np.nan,
        )

    merged["mean_abs_pct_diff"] = merged["mean_pct_diff"].abs()
    return merged


def build_validation_report_markdown(
    *,
    diff_table: pd.DataFrame,
    panel_a_n: int,
    panel_b_n: int,
    config: RunConfig,
) -> str:
    size_pass = panel_a_n == PAPER_PANEL_A_N and panel_b_n == PAPER_PANEL_B_N
    mean_pct = diff_table["mean_abs_pct_diff"]
    mean_pct_non_null = mean_pct.dropna()
    mean_values_missing = int(diff_table["mean_rep"].isna().sum())
    means_within_tol = (
        not mean_pct_non_null.empty
        and bool((mean_pct_non_null <= MEAN_PCT_DIFF_TOLERANCE).all())
        and mean_values_missing == 0
    )
    overall_pass = size_pass and means_within_tol

    lines: list[str] = []
    lines.append("# Validation Report")
    lines.append("")
    lines.append("## Run")
    lines.append(
        f"- Reference year: {config.reference_year}, Measurement year: {config.measurement_year}, History: {config.history_years}"
    )
    lines.append("")
    lines.append("## Status")
    lines.append(f"- Overall: {'PASS' if overall_pass else 'FAIL'}")
    lines.append(
        f"- Sample-size check: {'PASS' if size_pass else 'FAIL'} (Panel A: {panel_a_n} vs {PAPER_PANEL_A_N}, Panel B: {panel_b_n} vs {PAPER_PANEL_B_N})"
    )
    lines.append(
        f"- Mean-diff check: {'PASS' if means_within_tol else 'FAIL'} (tolerance: <= {MEAN_PCT_DIFF_TOLERANCE:.1f}% absolute percent diff)"
    )
    lines.append(f"- Missing replicated means: {mean_values_missing}")
    lines.append("")

    if not mean_pct_non_null.empty:
        lines.append("## Mean-Diff Summary")
        lines.append(f"- Variables compared: {len(mean_pct_non_null)}")
        lines.append(
            f"- Mean absolute percent diff (across variables): {float(mean_pct_non_null.mean()):.3f}%"
        )
        lines.append(
            f"- Max absolute percent diff: {float(mean_pct_non_null.max()):.3f}%"
        )
        lines.append("")

    lines.append("## Largest Mean Gaps")
    top = diff_table.sort_values("mean_abs_pct_diff", ascending=False).head(10)
    lines.append("| Panel | Variable | Paper Mean | Replicated Mean | Abs % Diff |")
    lines.append("|---|---|---:|---:|---:|")
    for _, row in top.iterrows():
        paper_mean = row["mean_paper"]
        rep_mean = row["mean_rep"]
        pct = row["mean_abs_pct_diff"]
        if pd.isna(paper_mean):
            paper_text = "null"
        else:
            paper_text = f"{float(paper_mean):.6g}"
        if pd.isna(rep_mean):
            rep_text = "null"
        else:
            rep_text = f"{float(rep_mean):.6g}"
        if pd.isna(pct):
            pct_text = "null"
        else:
            pct_text = f"{float(pct):.3f}%"
        lines.append(
            f"| {row['panel']} | {row['variable']} | {paper_text} | {rep_text} | {pct_text} |"
        )
    lines.append("")

    lines.append("## Notes")
    lines.append(
        "- This report compares replicated Table I statistics against paper targets."
    )
    lines.append(
        "- If sample sizes fail first, prioritize filter/timing logic before tuning option or wealth calculations."
    )
    lines.append(
        "- If sample sizes pass but means fail, inspect units/scaling (`P0`, `W0`, `%` fields), then option and wealth steps."
    )
    lines.append("")
    return "\n".join(lines)


def build_table1_artifacts(
    contracts: pd.DataFrame,
    tables: ExecuCompTables,
    config: RunConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str, str]:
    paper = paper_table1_reference()
    replicated, panel_a_n, panel_b_n = build_replicated_table1(contracts, tables, config)
    diff_table = build_table1_diff_table(paper=paper, replicated=replicated)
    stats_yaml = build_table1_stats_yaml(
        paper=paper,
        replicated=replicated,
        panel_a_n=panel_a_n,
        panel_b_n=panel_b_n,
    )
    validation_markdown = build_validation_report_markdown(
        diff_table=diff_table,
        panel_a_n=panel_a_n,
        panel_b_n=panel_b_n,
        config=config,
    )
    return paper, replicated, diff_table, stats_yaml, validation_markdown
