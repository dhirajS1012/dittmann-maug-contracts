from __future__ import annotations

from pathlib import Path

import pandas as pd

from dittmann_maug.io.loaders import read_parquet, normalize_columns
from dittmann_maug.contracts.stage1_inputs import Stage1Config, build_stage1_contract_inputs
from dittmann_maug.util.log import info


def _write_parquet(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)


def _get_execucomp_paths(repo_root: Path) -> dict[str, Path]:
    """Get paths to required ExecuComp data files in data/raw/execucomp/."""
    data_dir = repo_root / "data" / "raw" / "execucomp"
    anncomp = data_dir / "anncomp.parquet"
    codirfin = data_dir / "codirfin.parquet"
    return {"anncomp": anncomp, "codirfin": codirfin}


def check_data(repo_root: Path) -> dict[str, Path]:
    """Check that required input files exist. Raise if missing."""
    paths = _get_execucomp_paths(repo_root)

    missing = []
    for name, path in paths.items():
        if not path.exists():
            missing.append(f"  - {path}")

    if missing:
        error_msg = "Missing required ExecuComp data files:\n" + "\n".join(missing)
        error_msg += "\n\nTo fix: Copy data files to data/raw/execucomp/"
        raise FileNotFoundError(error_msg)

    return paths


def run_stage1(repo_root: Path, considered_year: int, rf: float | None = None) -> Path:
    """Build Stage 1 contract inputs for a given year and write to output/."""
    paths = _get_execucomp_paths(repo_root)
    check_data(repo_root)  # Verify files exist

    info(f"Loading anncomp from {paths['anncomp']}")
    ann = normalize_columns(read_parquet(paths["anncomp"]))

    info(f"Loading codirfin from {paths['codirfin']}")
    fin = normalize_columns(read_parquet(paths["codirfin"]))

    cfg = Stage1Config(considered_year=considered_year, rf=rf)
    measurement_year = cfg.measurement_year_resolved()
    info(f"Building Stage 1 inputs for considered year {considered_year} (measurement year {measurement_year})")
    out = build_stage1_contract_inputs(ann, fin, cfg)

    output_dir = repo_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"stage1_contract_inputs_{considered_year}.parquet"
    
    info(f"Writing {len(out):,} rows to {out_path}")
    _write_parquet(out, out_path)
    return out_path


def inspect_inputs(repo_root: Path) -> None:
    """Print quick stats about input tables."""
    paths = _get_execucomp_paths(repo_root)
    check_data(repo_root)  # Verify files exist

    info(f"Inspecting {paths['anncomp']}")
    ann = normalize_columns(read_parquet(paths["anncomp"]))
    info(f"anncomp: rows={len(ann):,}, cols={len(ann.columns):,}")
    if "year" in ann.columns:
        info(f"anncomp.year: min={ann['year'].min()}, max={ann['year'].max()}")
    if "ceoann" in ann.columns:
        vc = ann["ceoann"].astype(str).str.strip().value_counts().head(10)
        info("anncomp.ceoann top values:")
        for k, v in vc.items():
            print(f"  {k}: {v}")

    info(f"Inspecting {paths['codirfin']}")
    fin = normalize_columns(read_parquet(paths["codirfin"]))
    info(f"codirfin: rows={len(fin):,}, cols={len(fin.columns):,}")
    if "year" in fin.columns:
        info(f"codirfin.year: min={fin['year'].min()}, max={fin['year'].max()}")
