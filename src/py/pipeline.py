from __future__ import annotations

from contracts import get_contract_parameters_for_dataset
from data_loading import load_required_tables, missing_required_tables
from reporting import build_table1_artifacts
from schemas import PipelineResult, RunConfig


def run_pipeline(config: RunConfig) -> PipelineResult:
    """
    End-to-end pipeline entrypoint used by main().

    Step 6 behavior:
    - validates required inputs exist,
    - loads and normalizes core tables,
    - constructs contracts dataset,
    - constructs Table I artifacts.
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
    contracts = get_contract_parameters_for_dataset(config=config, tables=tables)
    (
        paper_table1,
        replicated_table1,
        table1_diff,
        stats_yaml,
        validation_report_markdown,
    ) = build_table1_artifacts(
        contracts=contracts,
        tables=tables,
        config=config,
    )
    return PipelineResult(
        contracts=contracts,
        paper_table1=paper_table1,
        replicated_table1=replicated_table1,
        table1_diff=table1_diff,
        table1_stats_yaml=stats_yaml,
        validation_report_markdown=validation_report_markdown,
    )
