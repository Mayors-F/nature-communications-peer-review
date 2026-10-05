# Peer-review aspect analysis

Research workflow and released aggregate results for the unpublished manuscript **“Do review focus and disagreement vary by author identity characteristics? Evidence from 35,015 Nature Communications articles.”** This repository contains cleaned code, fictional test fixtures, selected research-derived aggregates, a frozen taxonomy, and descriptive final figure files. It does not contain underlying review or author-level research records.

## Contents

- `notebooks/01...10` and `notebooks/supporting/`: analysis workflow and checks, with no saved outputs.
- `data/sample/`: deterministic fictional fixtures for software testing, not study estimates.
- `data/taxonomy/term_class_mapping.csv`: frozen three-column, 12-class taxonomy.
- `data/public/publication_tables/`: six formal aggregate tables.
- `data/public/figure_data/`: five aggregate figure-input tables, including coefficient subsets from the **combined** publication model.
- `data/public/descriptive/`: three aggregate summaries.
- `results/figures/`: six approved PNG figure files with descriptive filenames, including the JSD distribution image.
- `scripts/`, `src/`, `config/`, `docs/`: generator, offline smoke test, path helper, configuration, and documentation.

The released JSD distribution figure is **not regenerated from the released aggregate data**: exact JSD histogram bins are not distributed. The raw term-normalization mapping is also absent. No manuscript figure number is inferred from file order or name.

## Quick start

Use Python 3.10 and run from the repository root:

```text
python -m venv .venv
# Activate the environment for your platform.
python -m pip install -r requirements.txt
python scripts/run_synthetic_smoke.py
```

The runner generates fictional inputs and executes notebooks 01–10 plus S1 in fresh kernels in `demo` mode. Disposable `data/work/`, `results/demo/`, and `validation/` outputs are excluded from version control. Notebook 02 and 05 use mock provider responses by default. The offline demo does not call research APIs or download models.

For aggregate result rendering, execute notebooks 09 and 10 with `NC_RUNTIME_MODE=public-results`, using the default `paths.public_results_data_dir: data/public`. This path contains only released aggregates. The notebooks write under ignored `results/regenerated/`; they do not refit models or read private row-level tables in this mode. Absent JSD bins cause an explicit histogram skip. See [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) and [PIPELINE.md](docs/PIPELINE.md).

## Reproducibility boundary

1. **Software reproduction:** notebooks 01–10 and S1 run with synthetic fixtures; their fictional outputs do not reproduce empirical estimates.
2. **Result-rendering reproduction:** notebooks 09/10 render supported tables and aggregate-based figures from `data/public/`. This does not recreate the approved final-layout image files pixel-for-pixel.
3. **Full empirical reproduction:** not guaranteed. Original reviews, provider histories, manual taxonomy-creation decisions, and person/paper-level analysis inputs are not included.

Country grouping uses first-author institutional-affiliation attribution, not nationality. Gender is name-inferred, not biological sex or self-identification; confident assignment requires probability ≥0.80 and count ≥20. The formal country threshold is 500 papers; the fictional demo uses 5 only for coverage. The formal strict sample retains `n_authors <= 50`; the separate `large_team_ge_50` flag has another purpose. See [DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md) and [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).

## License

Source code (`.py`, `.ipynb`, and code configuration) is licensed under the [MIT License](LICENSE). Released research-derived taxonomy, aggregate data, figures, and synthetic fixture data are licensed under [CC BY-NC 4.0](LICENSE-DATA-ASSETS.md). Repository documentation and metadata describe these scopes; file-by-file classifications are in `REPO_MANIFEST.csv`. These licenses do not grant rights to excluded third-party source material or provider data not distributed here.

## Citation

Unpublished manuscript: *Do review focus and disagreement vary by author identity characteristics? Evidence from 35,015 Nature Communications articles*. Formal citation metadata will be added when manuscript authorship and publication metadata are finalized; no DOI or journal publication is claimed here.
