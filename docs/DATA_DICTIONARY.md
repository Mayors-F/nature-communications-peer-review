# Data dictionary

`data/sample/` is fictional test material. `sample_reviews.jsonl`, `sample_papers.csv`, and `sample_author_metadata.csv` exercise joins; `sample_term_mapping.csv` is an invented class mapping; `mock_*_responses.jsonl` are offline mock provider messages. `data/sample/public_results/` has synthetic aggregate fixtures, including synthetic bins that are **not** the withheld real bins. Fixture estimates are not findings.

| Released research path | Unit and fields | Use |
| --- | --- | --- |
| `data/taxonomy/term_class_mapping.csv` | One normalized term; `term_norm`, `term_type`, `major_class_final` only | Frozen 12-class mapping; no raw normalization notes or counts. |
| `data/public/publication_tables/*.csv` | Six aggregate model, sample-count, chi-square, and consistency tables | Formal table rendering; no paper-level rows. |
| `data/public/figure_data/figure_data_country_aspect_deviation_pp.csv` and `figure_data_gender_aspect_deviation_pp.csv` | One group per row; `group` and 12 percentage-point deviations | Aspect heatmaps. Country is institutional attribution; gender is name-inferred. |
| `data/public/figure_data/descriptive_per_aspect_disagreement_main_strict.csv` | One aspect class per row; aggregate counts and disagreement statistics | Per-aspect disagreement plot. |
| `data/public/figure_data/figure_data_jsd_country_coefficients.csv` and `figure_data_jsd_gender_coefficients.csv` | Combined-model coefficient subsets; estimate, confidence limits, p-values and model metadata | JSD coefficient plots; not standalone fits. |
| `data/public/descriptive/*.csv` | Aggregate aspect, JSD, and paper-review-count summaries | Summary reporting; no row-level records. |
| `results/figures/**/*.png` | Six approved final-layout image files | Descriptive figure assets, not a numbering declaration. |

`n_papers` counts papers and `n_reviews` counts reviews. JSD is Jensen–Shannon divergence between review aspect-share vectors. Percentage-point deviations are not proportions. Real JSD histogram bins and raw term-normalization mapping are absent.
