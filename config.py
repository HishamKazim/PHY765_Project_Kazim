"""Loader for config.yaml.

Every notebook imports this rather than hardcoding parameters.
Edit config.yaml to regenerate results with different settings.
"""
from pathlib import Path
import yaml


def load_config(path: str | Path = "config.yaml") -> dict:
    """Load and return the configuration dictionary."""
    p = Path(path)
    if not p.exists():
        # Try parent directory (for notebooks running from subdirs)
        p = Path("..") / path
    if not p.exists():
        raise FileNotFoundError(
            f"config.yaml not found in current directory or parent. "
            f"Run notebooks from the repository root."
        )
    with open(p) as f:
        return yaml.safe_load(f)


def thc_compression_for(norb: int, cfg: dict) -> float:
    """Pick THC compression factor for a given orbital count."""
    thresh = cfg["thc"]["compression_thresholds"]
    if norb >= thresh["large"]["min_orb"]:
        return thresh["large"]["factor"]
    if norb >= thresh["medium"]["min_orb"]:
        return thresh["medium"]["factor"]
    return thresh["small"]["factor"]


def geometry_string(cfg: dict) -> str:
    """Format the geometry as a PySCF-compatible atom string."""
    lines = []
    for atom in cfg["system"]["geometry"]:
        lines.append(f"    {atom['atom']:2s}  {atom['x']:.3f}  "
                     f"{atom['y']:.3f}  {atom['z']:.3f}")
    return "\n".join(lines)


def ensure_dirs(cfg: dict) -> None:
    """Create data/ and figures/ directories if they don't exist."""
    Path(cfg["paths"]["data_dir"]).mkdir(exist_ok=True)
    Path(cfg["paths"]["figures_dir"]).mkdir(exist_ok=True)
