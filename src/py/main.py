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
        output_df = run_pipeline(config)
    except NotImplementedError as exc:
        print(str(exc))
        print("Step 2 is complete (interfaces + pipeline scaffold).")
        print("Continue with Steps 3-5 for full contract construction.")
        return 0
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    config.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = (
        config.output_dir
        / f"contracts_{config.measurement_year}_{config.history_years}yrs.parquet"
    )
    output_df.to_parquet(output_path, index=False)
    print(f"Wrote {len(output_df)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

