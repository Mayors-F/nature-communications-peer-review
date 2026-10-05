"""Build aggregate-only public-results test fixtures from synthetic demo outputs."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample" / "public_results"
FIGURE = OUT / "figure_data"
TABLE = OUT / "publication_tables"
STRICT = ROOT / "results" / "demo" / "strict"
PUBLICATION = ROOT / "results" / "demo" / "publication"

FIGURE_NAMES = (
    "figure_data_country_aspect_deviation_pp.csv",
    "figure_data_gender_aspect_deviation_pp.csv",
    "figure_data_jsd_country_coefficients.csv",
    "figure_data_jsd_gender_coefficients.csv",
    "descriptive_per_aspect_disagreement_main_strict.csv",
)
TABLE_NAMES = (
    "model_paper_jsd_ols__country_gender_combined_main.csv",
    "table_ols_poisson_consistency_summary.csv",
    "table_chi_square_tests_formatted.csv",
    "sample_count__paper_jsd_country_gender_combined.csv",
)


def copy_csv(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    frame = pd.read_csv(source)
    forbidden = {"paper_code", "review_id", "author_uid", "author_name", "paper_title", "review_text", "doi", "orcid"}
    if forbidden.intersection(frame.columns):
        raise ValueError(f"Aggregate fixture contains a row identifier: {source}")
    frame.to_csv(target, index=False, encoding="utf-8-sig")


def main() -> None:
    FIGURE.mkdir(parents=True, exist_ok=True)
    TABLE.mkdir(parents=True, exist_ok=True)
    for name in FIGURE_NAMES:
        copy_csv(STRICT / "tables" / name, FIGURE / name)
    for name in TABLE_NAMES:
        copy_csv(PUBLICATION / name, TABLE / name)
    # Only synthetic row-level values are read here; they are never copied out.
    synthetic_jsd = pd.read_parquet(STRICT / "samples" / "main_strict_paper_jsd_no_large50.parquet",
                                    columns=["mean_pairwise_jsd"])["mean_pairwise_jsd"].dropna().to_numpy(dtype=float)
    counts, edges = np.histogram(synthetic_jsd, bins=40)
    pd.DataFrame({"bin_left": edges[:-1], "bin_right": edges[1:], "count": counts}).to_csv(
        FIGURE / "jsd_distribution_bins.csv", index=False, encoding="utf-8-sig")
    (OUT / "SYNTHETIC_TEST_FIXTURE.txt").write_text(
        "SYNTHETIC TEST FIXTURE. Derived solely from generated demonstration data. "
        "Not reviewed or approved for real-data public release. No scientific interpretation.\n",
        encoding="utf-8",
    )
    print(f"Created {len(FIGURE_NAMES) + len(TABLE_NAMES) + 1} aggregate test CSVs")


if __name__ == "__main__":
    main()
