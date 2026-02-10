from __future__ import annotations

import argparse
from pathlib import Path

from dittmann_maug.pipeline import check_data, run_stage1, inspect_inputs


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dittmann-maug")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check-data", help="Check required input files exist")
    c.add_argument("--repo-root", default=".", help="Repo root (default: current directory)")

    i = sub.add_parser("inspect", help="Print quick stats about input tables")
    i.add_argument("--repo-root", default=".", help="Repo root (default: current directory)")

    s = sub.add_parser("stage1", help="Build stage1 contract inputs (phi, ns, p0, d, sigma, rf)")
    s.add_argument("--repo-root", default=".", help="Repo root (default: current directory)")
    s.add_argument("--year", type=int, required=True, help="Considered year, e.g. 2000")
    s.add_argument("--rf", type=float, default=None, help="Risk-free rate, decimals, e.g. 0.0664")

    return p


def main() -> None:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()

    if args.cmd == "check-data":
        paths = check_data(repo_root)
        for k, v in paths.items():
            print(f"{k}: {v}")
        return

    if args.cmd == "inspect":
        check_data(repo_root)
        inspect_inputs(repo_root)
        return

    if args.cmd == "stage1":
        out_path = run_stage1(repo_root, considered_year=int(args.year), rf=args.rf)
        print(str(out_path))
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
