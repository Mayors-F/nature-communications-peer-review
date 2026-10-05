"""Run the repository's synthetic workflow in fresh offline kernels.

This script writes only ignored synthetic work/results and validation artifacts
under this repository root. It does not use research data or call external APIs.
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "validation"
NOTEBOOKS = [
    (f"{i:02d}", ROOT / "notebooks" / name) for i, name in enumerate((
        "01_prepare_and_segment_reviews.ipynb",
        "02_extract_review_aspects.ipynb",
        "03_build_aspect_vocabulary.ipynb",
        "04_normalize_and_classify_terms.ipynb",
        "05_build_author_features.ipynb",
        "06_build_analysis_tables.ipynb",
        "07_strict_sample_and_main_analysis.ipynb",
        "08_robustness_analysis.ipynb",
        "09_publication_tables_and_figures.ipynb",
        "10_format_single_column_figures.ipynb",
    ), 1)
]
S1 = ROOT / "notebooks" / "supporting" / "01_validate_inputs_and_coverage.ipynb"


def install_local_kernel() -> None:
    kernelspec = VALIDATION / "jupyter" / "kernels" / "nc-synthetic" / "kernel.json"
    kernelspec.parent.mkdir(parents=True, exist_ok=True)
    kernelspec.write_text(json.dumps({
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "NC synthetic workflow", "language": "python",
    }), encoding="utf-8")
    os.environ["JUPYTER_PATH"] = str(VALIDATION / "jupyter")


def execute(label: str, path: Path, *, final: bool = False) -> dict:
    os.environ["NC_RUNTIME_MODE"] = "demo"
    os.environ["NC_VALIDATION_FINAL"] = "1" if final else "0"
    os.environ["MPLBACKEND"] = "Agg"
    notebook = nbformat.read(path, as_version=4)
    started = time.perf_counter()
    client = NotebookClient(notebook, timeout=1200, kernel_name="nc-synthetic",
                            resources={"metadata": {"path": str(ROOT)}}, allow_errors=False)
    status, error = "PASS", ""
    try:
        client.execute()
    except Exception as exc:
        status, error = "FAIL", f"{type(exc).__name__}: {str(exc)[:500]}"
    finally:
        out = VALIDATION / "executed_notebooks" / f"{label}.ipynb"
        out.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, out)
    result = {"stage": label, "status": status,
              "seconds": round(time.perf_counter() - started, 2), "error": error}
    print(result, flush=True)
    return result


def main() -> int:
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    VALIDATION.mkdir(exist_ok=True)
    install_local_kernel()
    env = os.environ.copy()
    env["NC_RUNTIME_MODE"] = "demo"
    env["MPLBACKEND"] = "Agg"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_synthetic_data.py")],
                   cwd=ROOT, env=env, check=True)
    results: list[dict] = []
    for label, path in NOTEBOOKS:
        if label == "07":
            results.append(execute("S1_intermediate", S1))
            if results[-1]["status"] != "PASS":
                break
        results.append(execute(label, path))
        if results[-1]["status"] != "PASS":
            break
    if results and results[-1]["status"] == "PASS":
        results.append(execute("S1_final", S1, final=True))
    (VALIDATION / "smoke_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 0 if len(results) == 12 and all(row["status"] == "PASS" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
