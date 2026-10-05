"""Repository-relative locations shared by the public notebooks."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
WORK_DATA_DIR = DATA_DIR / "work"
RESULTS_DIR = PROJECT_ROOT / "results"
CONFIG_DIR = PROJECT_ROOT / "config"


def project_path(relative: str) -> Path:
    """Resolve a configured relative path without allowing escape from this release."""
    candidate = (PROJECT_ROOT / relative).resolve()
    if not candidate.is_relative_to(PROJECT_ROOT):
        raise ValueError("Configured path must remain within the public repository")
    return candidate
