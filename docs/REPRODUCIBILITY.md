# Reproducibility scope

| Workflow | Public-data status | Boundary |
| --- | --- | --- |
| 01–03, 05–08, S1 | `RUNNABLE_WITH_SYNTHETIC_DATA` | Fictional inputs and mock responses exercise software, not historical research data. Real-input branches require authorized nonpublic sources. |
| 04 | `RUNNABLE_WITH_SYNTHETIC_DATA`; frozen mapping released | The formal 12-class mapping is in `data/taxonomy/term_class_mapping.csv`, but manual labeling and raw term-normalization history are not replayed. |
| 09–10 | `FULLY_RUNNABLE_WITH_PUBLIC_DATA` for supported aggregate rendering | Released `data/public/` tables and figure data redraw supported results. Exact JSD bins are absent, so 09 skips that histogram. No model refitting. |
| Full historical empirical workflow | `REQUIRES_NONPUBLIC_INPUT` | Original reviews, paper/person-level data, provider responses, and historical curation decisions are absent. |

Run `python scripts/run_synthetic_smoke.py` for the fictional 01–10 plus S1 pipeline. It uses fresh kernels and writes only ignored outputs. For released aggregate outputs, set `NC_RUNTIME_MODE=public-results` for notebooks 09 and 10. Default input is `data/public`; output is `results/regenerated`. Public-results mode has no private `data/work` fallback and does not refit models.

Notebook 05's real author-feature branch remains an authorized-researcher pathway; aggregate results do not release person-level author features. The frozen taxonomy is an application input, not a complete record of its manual creation. The released JSD distribution image is a separate approved asset, **not regenerated from the released aggregate data**.

Country is first-author institutional attribution, not nationality. Gender is name-inferred, not biological sex or self-identification. The formal country threshold is 500 papers, demo threshold 5. Papers with more than 50 authors are excluded; exactly 50 are retained. `large_team_ge_50` independently means at least 50. Confident inferred gender requires probability ≥0.80 and provider count ≥20.
