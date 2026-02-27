from __future__ import annotations

import argparse
from pathlib import Path

from data_loading import missing_required_tables
from pipeline import run_pipeline
from schemas import RunConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dittmann-Maug replication runner (stepwise implementation)."
    )
    parser.add_argument("--reference-year", type=int, default=1999)
    parser.add_argument("--history-years", type=int, default=5)
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument(
        "--check-data-only",
        action="store_true",
        help="Only validate required input parquet files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = RunConfig(
        reference_year=args.reference_year,
        history_years=args.history_years,
        data_dir=args.data_dir,
        output_dir=args.output_dir,
    )

    missing = missing_required_tables(config)
    if args.check_data_only:
        if missing:
            print("Missing required tables:")
            for name, path in missing.items():
                print(f"- {name}: {path}")
            return 1
        print("All required core tables are present.")
        return 0

    try:
        result = run_pipeline(config)
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    config.output_dir.mkdir(parents=True, exist_ok=True)
    contracts_parquet_path = (
        config.output_dir
        / f"contracts_{config.measurement_year}_{config.history_years}yrs.parquet"
    )
    contracts_csv_path = (
        config.output_dir
        / f"contracts_{config.measurement_year}_{config.history_years}yrs.csv"
    )
    paper_table1_path = config.output_dir / "paper_table1.csv"
    replicated_table1_path = config.output_dir / "replicated_table1.csv"
    table1_diff_path = config.output_dir / "table1_diff.csv"
    table1_stats_path = config.output_dir / "table1_stats.yaml"
    validation_report_path = config.output_dir / "validation_report.md"

    result.contracts.to_parquet(contracts_parquet_path, index=False)
    result.contracts.to_csv(contracts_csv_path, index=False)
    result.paper_table1.to_csv(paper_table1_path, index=False)
    result.replicated_table1.to_csv(replicated_table1_path, index=False)
    result.table1_diff.to_csv(table1_diff_path, index=False)
    table1_stats_path.write_text(result.table1_stats_yaml, encoding="utf-8")
    validation_report_path.write_text(result.validation_report_markdown, encoding="utf-8")

    print(f"Wrote contracts parquet: {contracts_parquet_path}")
    print(f"Wrote contracts csv: {contracts_csv_path}")
    print(f"Wrote paper table reference: {paper_table1_path}")
    print(f"Wrote replicated table summary: {replicated_table1_path}")
    print(f"Wrote table diff csv: {table1_diff_path}")
    print(f"Wrote table stats yaml: {table1_stats_path}")
    print(f"Wrote validation report: {validation_report_path}")
    print(f"Contract rows: {len(result.contracts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
