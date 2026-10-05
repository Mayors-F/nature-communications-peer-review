# Validation and interpretation

The offline synthetic runner (`python scripts/run_synthetic_smoke.py`) checks the generator and notebooks 01–10 plus S1 in fresh kernels. It is a software/schema test; fictional results are not empirical findings. Notebook 09/10 `public-results` mode renders released aggregates in `data/public/` without row-level inputs or model refitting. This is data-level reproducibility, not pixel-identical reproduction of separately released final-layout figures.

The released JSD distribution image is not regenerated from released aggregates because exact histogram bins are withheld. Public-results mode explicitly skips that plot. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the software, aggregate-rendering, and full-empirical distinctions.
