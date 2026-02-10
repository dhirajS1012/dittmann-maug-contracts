from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    alternatives: tuple[str, ...] = ()

    def all_names(self) -> tuple[str, ...]:
        return (self.name,) + self.alternatives


def _resolve_column(df: pd.DataFrame, spec: ColumnSpec) -> str | None:
    cols = set(df.columns)
    for c in spec.all_names():
        if c in cols:
            return c
    return None


def require_columns(df: pd.DataFrame, specs: Iterable[ColumnSpec], table_name: str) -> dict[str, str]:
    """Validate that required columns exist.

    Returns a mapping of logical name -> actual df column name.
    """

    mapping: dict[str, str] = {}
    missing: list[str] = []

    for spec in specs:
        resolved = _resolve_column(df, spec)
        if resolved is None:
            missing.append("|".join(spec.all_names()))
        else:
            mapping[spec.name] = resolved

    if missing:
        missing_str = ", ".join(missing)
        raise KeyError(f"{table_name}: missing required columns: {missing_str}")

    return mapping
