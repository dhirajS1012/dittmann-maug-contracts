from __future__ import annotations

import pandas as pd

from schemas import ContractParameters, ExecuCompTables, RunConfig


def apply_sas_sample_filters(
    *,
    config: RunConfig,
    tables: ExecuCompTables,
) -> pd.DataFrame:
    """
    Reproduce SAS sample-selection logic up to work.a10.

    This implements Step 4:
    - CEO selection + linked salary rule,
    - backward exclusion from shrown/pinclopt,
    - continuity/history requirement,
    - multi-company exclusion.
    """
    # SAS work.a1: merge anncomp and coperol.
    a1 = tables.anncomp.merge(
        tables.coperol,
        on=["co_per_rol", "year"],
        how="outer",
        suffixes=("", "_coperol"),
    )

    # SAS work.a2a / work.a2b / work.a2.
    a2a = a1.loc[
        a1["year"].eq(config.measurement_year),
        ["co_per_rol", "ceoann", "execid"],
    ]
    a2b = a1.loc[
        a1["year"].eq(config.reference_year),
        ["co_per_rol", "salary"],
    ]
    a2 = a2a.merge(a2b, on="co_per_rol", how="outer")
    a2 = a2[(a2["ceoann"] == "CEO") & a2["salary"].notna()]
    flagged_execids = a2["execid"].dropna().astype("Int64").unique()

    # SAS work.a3: keep full exec history up to reference year for selected execids.
    a3 = a1[a1["execid"].isin(flagged_execids) & a1["year"].le(config.reference_year)]

    # SAS work.a4-a6: drop rows with missing shrown / pinclopt='TRUE' and all prior rows.
    a4 = a3.copy()
    a4["invalid_obs"] = a4["shrown"].isna() | a4["pinclopt"].eq("TRUE")
    a4 = a4.sort_values(
        ["execid", "year", "invalid_obs"],
        ascending=[True, False, False],
        kind="stable",
    )
    a4["drop_from_here_backward"] = a4.groupby("execid", dropna=False)[
        "invalid_obs"
    ].cummax()
    a6 = a4[~a4["drop_from_here_backward"]].copy()

    # SAS work.a7: enforce required history years.
    if config.history_years > 1:
        required_years = list(
            range(
                config.reference_year - config.history_years + 1,
                config.reference_year,
            )
        )
        years_by_exec = (
            a6.dropna(subset=["execid", "year"])
            .groupby("execid")["year"]
            .agg(lambda years: set(years.dropna().astype(int)))
        )
        valid_execids = [
            execid
            for execid, year_set in years_by_exec.items()
            if all(required_year in year_set for required_year in required_years)
        ]
        a7 = a6[a6["execid"].isin(valid_execids)].copy()
    else:
        a7 = a6.copy()

    # SAS work.a8-a10: drop execs appearing in >1 company in any same year.
    year_freq = (
        a7.dropna(subset=["execid", "year"])
        .groupby(["execid", "year"])
        .size()
        .rename("freq")
        .reset_index()
    )
    max_freq = year_freq.groupby("execid")["freq"].max()
    multi_company_execids = max_freq[max_freq > 1].index
    a10 = a7[~a7["execid"].isin(multi_company_execids)].copy()

    # SAS work.a10 construction fields.
    a10["total_salary"] = (
        a10["salary"] + a10["bonus"] + a10["othann"] + a10["ltip"] + a10["allothtot"]
    )
    a10["execid_num"] = a10["execid"].astype("Int64")
    a10["year_num"] = a10["year"].astype("Int64")
    a10["permid_num"] = a10["permid"].astype("Int64")

    return a10.reset_index(drop=True)


def get_contract_parameters(
    *,
    execid: int,
    permid: int,
    reference_year: int,
    measurement_year: int,
    anncomp_row: pd.Series,
    codirfin_row: pd.Series,
    option_rows: pd.DataFrame,
    history_rows: pd.DataFrame,
) -> ContractParameters:
    """
    Compute contract parameters for one executive-year.

    This is the core single-observation API requested in TODOS-HUMAN.
    Full implementation is delivered in Step 5.
    """
    raise NotImplementedError(
        "get_contract_parameters interface is ready; implementation is part of Step 5."
    )


def get_contract_parameters_for_dataset(
    *,
    config: RunConfig,
    tables: ExecuCompTables,
) -> pd.DataFrame:
    """
    Dataset-level wrapper around get_contract_parameters.

    Step 4 returns the SAS-equivalent filtered history panel (work.a10).
    Step 5 will construct final contract parameters from this panel.
    """
    return apply_sas_sample_filters(config=config, tables=tables)

