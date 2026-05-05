#!/usr/bin/env python3
"""Run all notebooks in order to regenerate every figure and result.

Usage:
    python scripts/regenerate_figures.py

Outputs:
    data/integrals.npz
    data/pauli_lcu_results.json
    data/df_results.json
    data/thc_results.json
    data/fci_validation.json
    data/summary.json
    figures/scaling_summary.png
"""
import subprocess
import sys
from pathlib import Path

NOTEBOOKS = [
    "01_setup_integrals.ipynb",
    "02_pauli_lcu.ipynb",
    "03_double_factorization.ipynb",
    "04_thc.ipynb",
    "05_fci_validation.ipynb",
    "06_physical_and_crossover.ipynb",
]


def run_notebook(nb: str) -> None:
    """Execute a notebook in place using nbconvert."""
    print(f"\n>>> Running {nb}")
    result = subprocess.run(
        [sys.executable, "-m", "jupyter", "nbconvert",
         "--to", "notebook",
         "--execute", nb,
         "--inplace",
         "--ExecutePreprocessor.timeout=600"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"FAILED: {nb}")
        print(result.stderr)
        sys.exit(1)
    print(f"OK: {nb}")


def main() -> None:
    repo_root = Path(__file__).parent.parent
    for nb in NOTEBOOKS:
        nb_path = repo_root / nb
        if not nb_path.exists():
            print(f"missing: {nb_path}")
            sys.exit(1)
    import os
    os.chdir(repo_root)
    for nb in NOTEBOOKS:
        run_notebook(nb)
    print("\nAll notebooks executed. Outputs in data/ and figures/.")


if __name__ == "__main__":
    main()
