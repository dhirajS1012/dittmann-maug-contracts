from __future__ import annotations

from pathlib import Path

import pandas as pd

from dittmann_maug.config import settings_from_repo_root
from dittmann_maug.io.paths import ExecuCompPaths, resolve_execucomp_dir
from dittmann_maug.io.loaders import read_parquet, normalize_columns
from dittmann_maug.contracts.stage1_inputs import Stage1Config, build_stage1_contract_inputs
from dittmann_maug.util.log import info


def _write_parquet(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)


def check_data(repo_root: Path) -> dict[str, Path]:
    """Return resolved file paths and raise if missing core inputs."""

    s = settings_from_repo_root(repo_root)
    exec_dir = resolve_execucomp_dir(s.dropbox_root())
    p = ExecuCompPaths(root=exec_dir)

    missing = []
    for f in [p.anncomp, p.codirfin]:
        if not f.exists():
            missing.append(str(f))

    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))

    return {"anncomp": p.anncomp, "codirfin": p.codirfin}


def run_stage1(repo_root: Path, considered_year: int, rf: float | None = None) -> Path:
    s = settings_from_repo_root(repo_root)
    exec_dir = resolve_execucomp_dir(s.dropbox_root())
    paths = ExecuCompPaths(root=exec_dir)

    info(f"Loading anncomp from {paths.anncomp}")
    ann = normalize_columns(read_parquet(paths.anncomp))

    info(f"Loading codirfin from {paths.codirfin}")
    fin = normalize_columns(read_parquet(paths.codirfin))

    cfg = Stage1Config(considered_year=considered_year, rf=rf)
    info(f"Building Stage 1 inputs for considered year {considered_year} (measurement year {cfg.measurement_year_resolved()})")
    out = build_stage1_contract_inputs(ann, fin, cfg)

    out_path = s.dropbox_root() / "out" / f"stage1_contract_inputs_{considered_year}.parquet"
    info(f"Writing {len(out):,} rows to {out_path}")
    _write_parquet(out, out_path)
    return out_path


def inspect_inputs(repo_root: Path) -> None:
    s = settings_from_repo_root(repo_root)
    exec_dir = resolve_execucomp_dir(s.dropbox_root())
    paths = ExecuCompPaths(root=exec_dir)

    info(f"Inspecting {paths.anncomp}")
    ann = normalize_columns(read_parquet(paths.anncomp))
    info(f"anncomp: rows={len(ann):,}, cols={len(ann.columns):,}")
    if "year" in ann.columns:
        info(f"anncomp.year: min={ann['year'].min()}, max={ann['year'].max()}")
    if "ceoann" in ann.columns:
        vc = ann["ceoann"].astype(str).str.strip().value_counts().head(10)
        info("anncomp.ceoann top values:")
        for k, v in vc.items():
            print(f"  {k}: {v}")

    info(f"Inspecting {paths.codirfin}")
    fin = normalize_columns(read_parquet(paths.codirfin))
    info(f"codirfin: rows={len(fin):,}, cols={len(fin.columns):,}")
    if "year" in fin.columns:
        info(f"codirfin.year: min={fin['year'].min()}, max={fin['year'].max()}")
