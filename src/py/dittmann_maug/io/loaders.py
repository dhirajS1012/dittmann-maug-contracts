from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


def read_parquet(path: Path, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Read a parquet file.

    Uses pyarrow via pandas.
    """

    if not path.exists():
        raise FileNotFoundError(f"Missing parquet file: {path}")
    return pd.read_parquet(path, columns=list(columns) if columns is not None else None)


def read_table_auto(path: Path, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Read parquet or csv.

    This helps when your export format changes.
    """

    if path.suffix.lower() == ".parquet":
        return read_parquet(path, columns=columns)

    if path.suffix.lower() == ".csv":
        if not path.exists():
            raise FileNotFoundError(f"Missing csv file: {path}")
        usecols = list(columns) if columns is not None else None
        return pd.read_csv(path, usecols=usecols)

    raise ValueError(f"Unsupported table format: {path}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase.

    Keeps data unchanged.
    """

    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df
