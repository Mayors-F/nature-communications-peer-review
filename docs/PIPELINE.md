# Notebook pipeline

| Stage | Purpose | Available inputs |
| --- | --- | --- |
| 01–03 | Segment reviews, extract aspects, build vocabulary | Fictional reviews and mock responses for public demo. |
| 04 | Apply frozen 12-class taxonomy | Fictional mapping for demo; released `data/taxonomy/term_class_mapping.csv` for authorized real-input work. Manual labeling history is not replayed. |
| 05 | Build author features | Mock/offline by default; real author/provider data are not distributed. |
| 06 | Build analysis tables | Demo work tables; real paper/review microdata are absent. |
| 07–08 | Strict main analysis and robustness | Synthetic demo from public files. |
| 09 | Publication tables and figures | Demo from synthetic work, or aggregate-only `public-results` from `data/public/`. No refitting in public-results mode. |
| 10 | Single-column formatting | Demo or `data/public/figure_data/` in public-results mode. |
| S1 | Intermediate/final checks | After 06 and after 10 in synthetic workflow. |

`python scripts/run_synthetic_smoke.py` executes the full synthetic sequence in fresh kernels. For released aggregate rendering, set `NC_RUNTIME_MODE=public-results` and execute 09 then 10 from the repository root. Default `paths.public_results_data_dir` is `data/public`; outputs appear under ignored `results/regenerated/`. The JSD histogram is skipped because real bins are withheld, although the approved pre-rendered image exists under `results/figures/`.
