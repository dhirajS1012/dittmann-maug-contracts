from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExecuCompPaths:
    """Filesystem conventions for ExecuComp extracts.

    Expected layout under DROPBOX or .DROPBOX:
    - execucomp/anncomp.parquet
    - execucomp/codirfin.parquet
    - execucomp/coperol.parquet (optional)
    - execucomp/stgrttab.parquet (optional, used in later phases)
    """

    root: Path

    def _file(self, name: str) -> Path:
        return self.root / name

    @property
    def anncomp(self) -> Path:
        return self._file("anncomp.parquet")

    @property
    def codirfin(self) -> Path:
        return self._file("codirfin.parquet")

    @property
    def coperol(self) -> Path:
        return self._file("coperol.parquet")

    @property
    def stgrttab(self) -> Path:
        return self._file("stgrttab.parquet")


def resolve_execucomp_dir(dropbox_root: Path) -> Path:
    """Return the execucomp directory.

    Supported:
    - <DROPBOX> / execucomp
    - <DROPBOX> / ExecuComp
    """

    candidates = [
        dropbox_root / "execucomp",
        dropbox_root / "ExecuComp",
    ]

    for c in candidates:
        if c.exists():
            return c

    # Default location even if it does not exist yet.
    return candidates[0]
