"""Rebuild the cached approximation-ratio graph PDFs used in the paper."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


FIGURES_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = FIGURES_DIR / "generated"
GRAPH_SOURCES = (
    "tree_approximation_ratio_2d_plot.tex",
    "tree_approximation_ratio_3d_plot.tex",
)


def run(command: list[str]) -> None:
    print(f"> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=FIGURES_DIR, check=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(FIGURES_DIR / "generate_tree_approximation_ratio_3d.py")])

    for graph_source in GRAPH_SOURCES:
        run(
            [
                "latexmk",
                "-g",
                "-lualatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-outdir={OUTPUT_DIR.name}",
                graph_source,
            ]
        )

    print(f"Rebuilt graph PDFs in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()