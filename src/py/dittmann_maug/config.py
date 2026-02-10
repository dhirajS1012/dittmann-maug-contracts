from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    """Runtime settings.

    Conventions:
    - Raw data and large artifacts live under .DROPBOX/ (or DROPBOX/).
    - Code lives under src/py/.

    Override:
    - Set DM_DROPBOX_ROOT to an absolute path if your data folder lives elsewhere.
    """

    repo_root: Path
    dropbox_dirname: str = ".DROPBOX"

    def dropbox_root(self) -> Path:
        env = os.getenv("DM_DROPBOX_ROOT")
        if env:
            return Path(env).expanduser().resolve()

        preferred = self.repo_root / self.dropbox_dirname
        if preferred.exists():
            return preferred

        fallback = self.repo_root / "DROPBOX"
        return fallback


def settings_from_repo_root(repo_root: str | Path) -> Settings:
    return Settings(repo_root=Path(repo_root).resolve())
