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
    },
    "coperol": {
        "co_per_rol_id": "co_per_rol",
        "ceo_ann": "ceoann",
    },
    "codirfin": {
        "bsvolatility": "bs_volatility",
        "volatility": "bs_volatility",
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
    "anncomp": {"co_per_rol", "year"},
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
    for source_col, target_col in aliases.items():
        if source_col in frame.columns and target_col not in frame.columns:
            rename_map[source_col] = target_col

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


def _coerce_numeric_columns(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    for col in TABLE_NUMERIC_COLUMNS[table_name]:
        normalized[col] = pd.to_numeric(normalized[col], errors="coerce")
    return normalized


def _coerce_int_columns(table_name: str, frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    for col in TABLE_INT_COLUMNS[table_name]:
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
    _validate_required_columns(table_name, normalized)
    normalized = _coerce_numeric_columns(table_name, normalized)
    normalized = _coerce_int_columns(table_name, normalized)
    normalized = _normalize_table_values(table_name, normalized)
    normalized = _sort_table(table_name, normalized)
    return normalized


def load_required_tables(config: RunConfig) -> ExecuCompTables:
    missing = missing_required_tables(config)
    if missing:
        details = ", ".join(f"{name}={path}" for name, path in missing.items())
        raise FileNotFoundError(f"Missing required data files: {details}")

    paths = required_table_paths(config)
    anncomp = normalize_table("anncomp", pd.read_parquet(paths["anncomp"]))
    coperol = normalize_table("coperol", pd.read_parquet(paths["coperol"]))
    codirfin = normalize_table("codirfin", pd.read_parquet(paths["codirfin"]))
    stgrttab = normalize_table("stgrttab", pd.read_parquet(paths["stgrttab"]))

    return ExecuCompTables(
        anncomp=anncomp,
        coperol=coperol,
        codirfin=codirfin,
        stgrttab=stgrttab,
    )
