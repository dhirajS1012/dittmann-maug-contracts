from __future__ import annotations

from pathlib import Path

import pandas as pd

from schemas import ExecuCompTables, REQUIRED_TABLE_FILES, RunConfig


TABLE_REQUIRED_COLUMNS: dict[str, set[str]] = {
    "anncomp": {
        "co_per_rol",
        "year",
        "salary",
        "bonus",
        "othann",
        "allothtot",
        "ltip",
        "shrown",
        "pinclopt",
        "rstkgrnt",
        "rstkhld",
        "soptexer",
        "soptexsh",
        "uexnumun",
        "uexnumex",
        "inmonun",
        "inmonex",
    },
    "coperol": {"co_per_rol", "year", "execid", "permid", "ceoann"},
    "codirfin": {
        "permid",
        "year",
        "prccf",
        "ajex",
        "divyield",
        "fyr",
        "shrsout",
        "bs_volatility",
    },
    "stgrttab": {"co_per_rol", "year", "numsecur", "expric", "exdate"},
}


TABLE_ALIAS_COLUMNS: dict[str, dict[str, str]] = {
    "anncomp": {
        "co_per_rol_id": "co_per_rol",
        "shrown_excl_opts": "shrown",
        "shrown_tot": "shrown",
        "opt_exer_val": "soptexer",
        "opt_exer_num": "soptexsh",
        "stock_unvest_num": "rstkhld",
        "opt_unex_unexer_num": "uexnumun",
        "opt_unex_exer_num": "uexnumex",
        "opt_unex_unexer_est_val": "inmonun",
        "opt_unex_exer_est_val": "inmonex",
        "gvkey": "permid",
    },
    "coperol": {
        "co_per_rol_id": "co_per_rol",
        "ceo_ann": "ceoann",
        "pceo": "ceoann",
        "gvkey": "permid",
    },
    "codirfin": {
        "bsvolatility": "bs_volatility",
        "volatility": "bs_volatility",
        "gvkey": "permid",
    },
    "stgrttab": {
        "num_secur": "numsecur",
        "exp_price": "expric",
        "ex_date": "exdate",
    },
}


TABLE_NUMERIC_COLUMNS: dict[str, set[str]] = {
    "anncomp": {
        "co_per_rol",
        "year",
        "execid",
        "permid",
        "salary",
        "bonus",
        "othann",
        "allothtot",
        "ltip",
        "shrown",
        "rstkgrnt",
        "rstkhld",
        "soptexer",
        "soptexsh",
        "uexnumun",
        "uexnumex",
        "inmonun",
        "inmonex",
    },
    "coperol": {"co_per_rol", "year", "execid", "permid"},
    "codirfin": {
        "permid",
        "year",
        "prccf",
        "ajex",
        "divyield",
        "fyr",
        "shrsout",
        "bs_volatility",
    },
    "stgrttab": {"co_per_rol", "year", "numsecur", "expric"},
}


TABLE_INT_COLUMNS: dict[str, set[str]] = {
    "anncomp": {"co_per_rol", "year", "execid", "permid"},
    "coperol": {"co_per_rol", "year", "execid", "permid"},
    "codirfin": {"permid", "year", "fyr"},
    "stgrttab": {"co_per_rol", "year"},
}


TABLE_SORT_KEYS: dict[str, list[str]] = {
    "anncomp": ["co_per_rol", "year"],
    "coperol": ["co_per_rol", "year"],
    "codirfin": ["permid", "year"],
    "stgrttab": ["co_per_rol", "year"],
}


TABLE_DEFAULT_VALUES: dict[str, dict[str, object]] = {
    "anncomp": {
        "pinclopt": "FALSE",
        "rstkhld": 0.0,
        "soptexer": 0.0,
        "soptexsh": 0.0,
        "uexnumun": 0.0,
        "uexnumex": 0.0,
        "inmonun": 0.0,
        "inmonex": 0.0,
    },
    "coperol": {
        "ceoann": "NON-CEO",
    },
}


def required_table_paths(config: RunConfig) -> dict[str, Path]:
    return {
        table_name: config.data_dir / filename
        for table_name, filename in REQUIRED_TABLE_FILES.items()
    }


def missing_required_tables(config: RunConfig) -> dict[str, Path]:
    table_paths = required_table_paths(config)
    return {
        table_name: path for table_name, path in table_paths.items() if not path.exists()
    }


def _normalize_column_names(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    normalized.columns = [str(col).strip().lower() for col in normalized.columns]
    return normalized


def _apply_aliases(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    aliases = TABLE_ALIAS_COLUMNS.get(table_name, {})
    if not aliases:
        return frame

    rename_map: dict[str, str] = {}
    occupied_targets = set(frame.columns)
    for source_col, target_col in aliases.items():
        if source_col in frame.columns and target_col not in occupied_targets:
            rename_map[source_col] = target_col
            occupied_targets.add(target_col)

    if not rename_map:
        return frame
    return frame.rename(columns=rename_map)


def _validate_required_columns(table_name: str, frame: pd.DataFrame) -> None:
    required_cols = TABLE_REQUIRED_COLUMNS[table_name]
    missing_cols = sorted(required_cols - set(frame.columns))
    if not missing_cols:
        return

    available_preview = ", ".join(sorted(frame.columns)[:25])
    raise ValueError(
        f"Missing required columns in {table_name}: {missing_cols}. "
        f"Available columns preview: {available_preview}"
    )


def _apply_default_columns(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    defaults = TABLE_DEFAULT_VALUES.get(table_name, {})
    if not defaults:
        return frame

    normalized = frame.copy()
    for col, default in defaults.items():
        if col not in normalized.columns:
            normalized[col] = default
        else:
            normalized[col] = normalized[col].fillna(default)
    return normalized


def _coerce_numeric_columns(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    for col in TABLE_NUMERIC_COLUMNS[table_name]:
        if col in normalized.columns:
            normalized[col] = pd.to_numeric(normalized[col], errors="coerce")
    return normalized


def _coerce_int_columns(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    for col in TABLE_INT_COLUMNS[table_name]:
        if col in normalized.columns:
            normalized[col] = normalized[col].astype("Int64")
    return normalized


def _normalize_table_values(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    if table_name == "anncomp":
        normalized["pinclopt"] = (
            normalized["pinclopt"].astype("string").str.strip().str.upper()
        )
    elif table_name == "coperol":
        normalized["ceoann"] = (
            normalized["ceoann"].astype("string").str.strip().str.upper()
        )
    elif table_name == "stgrttab":
        normalized["exdate"] = pd.to_datetime(normalized["exdate"], errors="coerce")
    return normalized


def _sort_table(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    sort_keys = TABLE_SORT_KEYS[table_name]
    return frame.sort_values(sort_keys, kind="stable").reset_index(drop=True)


def normalize_table(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    if table_name not in TABLE_REQUIRED_COLUMNS:
        raise ValueError(f"Unsupported table name for normalization: {table_name}")

    normalized = _normalize_column_names(frame)
    normalized = _apply_aliases(table_name, normalized)
    normalized = _apply_default_columns(table_name, normalized)
    _validate_required_columns(table_name, normalized)
    normalized = _coerce_numeric_columns(table_name, normalized)
    normalized = _coerce_int_columns(table_name, normalized)
    normalized = _normalize_table_values(table_name, normalized)
    normalized = _sort_table(table_name, normalized)
    return normalized


def _anncomp_lookup_for_coperol(anncomp: pd.DataFrame) -> pd.DataFrame:
    required_cols = ["co_per_rol", "year", "execid", "permid", "ceoann"]
    available_cols = [col for col in required_cols if col in anncomp.columns]
    if not {"co_per_rol", "year"}.issubset(available_cols):
        return pd.DataFrame()

    lookup = anncomp[available_cols].drop_duplicates(
        subset=["co_per_rol", "year"],
        keep="first",
    )
    return lookup


def _normalize_coperol_with_anncomp(raw_coperol: pd.DataFrame, anncomp: pd.DataFrame) -> pd.DataFrame:
    normalized = _normalize_column_names(raw_coperol)
    normalized = _apply_aliases("coperol", normalized)
    normalized = _apply_default_columns("coperol", normalized)

    ann_lookup = _anncomp_lookup_for_coperol(anncomp)
    if "year" not in normalized.columns and not ann_lookup.empty:
        role_years = ann_lookup[["co_per_rol", "year"]].drop_duplicates()
        if "co_per_rol" in normalized.columns:
            role_level = normalized.drop_duplicates(subset=["co_per_rol"], keep="first")
            normalized = role_years.merge(role_level, on="co_per_rol", how="left")
        else:
            normalized = role_years.copy()

    if not ann_lookup.empty and {"co_per_rol", "year"}.issubset(normalized.columns):
        normalized = normalized.merge(
            ann_lookup,
            on=["co_per_rol", "year"],
            how="left",
            suffixes=("", "_anncomp"),
        )
        for col in ["execid", "permid", "ceoann"]:
            ann_col = f"{col}_anncomp"
            if ann_col not in normalized.columns:
                continue
            if col not in normalized.columns:
                normalized[col] = normalized[ann_col]
            else:
                normalized[col] = normalized[col].where(
                    normalized[col].notna(),
                    normalized[ann_col],
                )
            normalized = normalized.drop(columns=[ann_col])

    missing_after_fill = TABLE_REQUIRED_COLUMNS["coperol"] - set(normalized.columns)
    if missing_after_fill and set(TABLE_REQUIRED_COLUMNS["coperol"]).issubset(ann_lookup.columns):
        normalized = ann_lookup.copy()

    normalized = _apply_default_columns("coperol", normalized)
    _validate_required_columns("coperol", normalized)
    normalized = _coerce_numeric_columns("coperol", normalized)
    normalized = _coerce_int_columns("coperol", normalized)
    normalized = _normalize_table_values("coperol", normalized)
    normalized = _sort_table("coperol", normalized)
    return normalized


def load_required_tables(config: RunConfig) -> ExecuCompTables:
    missing = missing_required_tables(config)
    if missing:
        details = ", ".join(f"{name}={path}" for name, path in missing.items())
        raise FileNotFoundError(f"Missing required data files: {details}")

    paths = required_table_paths(config)
    anncomp = normalize_table("anncomp", pd.read_parquet(paths["anncomp"]))
    coperol = _normalize_coperol_with_anncomp(
        pd.read_parquet(paths["coperol"]),
        anncomp,
    )
    codirfin = normalize_table("codirfin", pd.read_parquet(paths["codirfin"]))
    stgrttab = normalize_table("stgrttab", pd.read_parquet(paths["stgrttab"]))

    return ExecuCompTables(
        anncomp=anncomp,
        coperol=coperol,
        codirfin=codirfin,
        stgrttab=stgrttab,
    )
