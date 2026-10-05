# Data availability and redistribution boundary

## Publicly released here

The repository includes the frozen minimal taxonomy (`data/taxonomy/term_class_mapping.csv`), six aggregate publication tables, five aggregate figure-data tables, three aggregate descriptive summaries under `data/public/`, and six descriptive-filename PNG figures under `results/figures/`. Coefficient figure-data files are subsets of the formal combined model. The approved JSD distribution image is included, but exact bins are not.

## Synthetic

`data/sample/` contains deterministic fictional reviews, papers, authors, mock responses, taxonomy mapping, and aggregate fixtures. These are software tests, not anonymized research records or empirical estimates. Generated `data/work/`, `results/demo/`, and `validation/` files are disposable and not shipped.

## Not redistributed

Original Nature peer-review texts and sentence data; raw aspect/model responses; author names, IDs, affiliations, DOI/title linkage; OpenAlex/Genderize or other provider records and caches; v2 microdata; strict paper/review-level samples; and person-level author features are absent. Separately authorized researchers may use private inputs, but code availability does not grant rights in source or provider content.

## Withheld by release decision

The exact real 40-bin JSD count vector, related restricted histogram inputs, and raw term-normalization mapping are withheld. No re-binned or fabricated substitutes have been added. The released JSD distribution figure is not regenerated from the released aggregate data.
