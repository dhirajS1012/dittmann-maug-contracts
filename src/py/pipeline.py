from __future__ import annotations

import pandas as pd

from contracts import get_contract_parameters_for_dataset
from data_loading import load_required_tables, missing_required_tables
from schemas import RunConfig


def run_pipeline(config: RunConfig) -> pd.DataFrame:
    """
    End-to-end pipeline entrypoint used by main().

    Step 3 behavior:
    - validates required inputs exist,
    - loads and normalizes core tables,
    - exposes the dataset-level construction hook.
    """
    missing = missing_required_tables(config)
    if missing:
        details = "\n".join(f"- {name}: {path}" for name, path in missing.items())
        raise FileNotFoundError(
            "Required raw files are missing under data/raw:\n"
            f"{details}\n"
            "Run src/bash/download_raw_data.sh or copy files manually."
        )

    tables = load_required_tables(config)
    return get_contract_parameters_for_dataset(config=config, tables=tables)
