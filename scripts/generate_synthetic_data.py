"""Generate deterministic, wholly fictional inputs for offline pipeline tests.

No research files are read. Scientific estimates from these records are meaningless.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

RANDOM_SEED = 20260925
GENERATOR_VERSION = "s1-2"
N_PAPERS = 96
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample"

CLASSES_AND_TERMS = [
    ("Methodology", "method design", "method reproducibility"),
    ("Results", "result reporting", "result consistency"),
    ("Experiments and Evaluation", "experiment evaluation", "evaluation design"),
    ("Data and Datasets", "data description", "dataset availability"),
    ("Figures and Tables", "figure clarity", "table description"),
    ("Writing, Language and Terminology", "writing clarity", "terminology consistency"),
    ("Theory and Models", "theory assumption", "model explanation"),
    ("Comparison and Context", "related work", "baseline comparison"),
    ("Paper Assessment", "publication suitability", "study quality"),
    ("Novelty and Impact", "method novelty", "study impact"),
    ("Validity, Rigor and Quality", "method validity", "result robustness"),
    ("Limitations", "study limitation", "data limitation"),
]
TERMS = [term for _, first, second in CLASSES_AND_TERMS for term in (first, second)]
COUNTRIES = ("US", "CN", "GB", "DE", "FR", "CA")
SUBJECTS = ("SYN-BIO", "SYN-MAT", "SYN-COMP")
TEXT_TEMPLATES = (
    "The synthetic method description could be more precise.",
    "The illustrative result needs a clearer explanation.",
    "The invented evaluation could include another comparison.",
    "The example figure would benefit from simpler labels.",
    "The artificial data description should explain its construction.",
    "The hypothetical model assumptions deserve more detail.",
    "The generic discussion should state a limitation.",
    "The fictional manuscript is clearly organized.",
)


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def gender_fields(paper_index: int, order: int) -> tuple[str, object, object]:
    # Include confident, two uncertain threshold cases, and genuinely missing.
    state = (paper_index // 6 + paper_index * 7 + order * 3) % 8
    if state in (0, 1, 4):
        return "male", 0.95, 100
    if state in (2, 3, 6):
        return "female", 0.95, 100
    if state == 5:
        return "female", 0.75, 100
    if paper_index % 2 == 0:
        return "male", 0.95, 5
    return "unknown", "", ""


def generate() -> dict:
    rng = random.Random(RANDOM_SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    papers, reviews, aspects, authors, provider_rows = [], [], [], [], []
    author_serial = 0
    review_serial = 0
    for paper_index in range(N_PAPERS):
        paper_code = f"P{paper_index + 1:04d}"
        n_authors = {0: 49, 1: 50, 2: 51}.get(paper_index, 2 + paper_index % 5)
        country = COUNTRIES[paper_index % len(COUNTRIES)]
        subject = SUBJECTS[(paper_index // 6 + paper_index) % len(SUBJECTS)]
        year = 2018 + (paper_index // 6 + paper_index * 2) % 6
        papers.append({
            "paper_code": paper_code, "subject_code": subject,
            "pub_date": f"{year}-03-15", "publication_year": year,
            "title": f"Synthetic study {paper_code}", "topic": "Fictional demonstration",
            "openalex_found": False, "openalex_authorships_returned": n_authors,
            "openalex_truncated_suspected": False, "doi_url": "",
        })
        for order in range(1, n_authors + 1):
            author_serial += 1
            author_uid = f"A{author_serial:06d}"
            author_country = country if order == 1 or (paper_index + order) % 4 else COUNTRIES[(paper_index + 2) % 6]
            if order == 1 and paper_index % 19 == 7:
                author_country = ""
            if order > 1 and (paper_index + order) % 23 == 0:
                author_country = ""
            gender, probability, count = gender_fields(paper_index, order)
            authors.append({
                "author_uid": author_uid, "paper_code": paper_code, "author_order": order,
                "is_first_author": order == 1, "is_last_author": order == n_authors,
                "is_corresponding_author": order == n_authors,
                "author_affil_country_primary": author_country,
                "name_inferred_gender": gender, "gender_probability": probability,
                "gender_count": count,
            })
            if paper_index == 0 and order == 2:
                provider_rows.append({"provider": "genderize", "request_id": "MOCK-G-001", "mock": True,
                                      "payload": {"author_uid": author_uid, "gender": gender,
                                                  "probability": probability, "count": count}})
        for review_index in range(3):
            review_serial += 1
            review_id = f"R{review_serial:05d}"
            term_by_sentence = {}
            sentences = []
            for sentence_index in range(4):
                template_index = (paper_index + review_index * 3 + sentence_index) % len(TEXT_TEMPLATES)
                sentences.append(TEXT_TEMPLATES[template_index])
                term_index = (paper_index * 7 + review_index * 5 + sentence_index * 3 + rng.randrange(4)) % len(TERMS)
                term_by_sentence[str(sentence_index)] = TERMS[term_index]
            if paper_index % 20 == 13 and review_index == 2:
                term_by_sentence = {str(index): "None" for index in range(4)}
            reviews.append({"review_id": review_id, "paper_code": paper_code,
                            "reviewer_tag": f"Synthetic Reviewer {review_index + 1}",
                            "content_raw": " ".join(sentences)})
            aspects.append({"paper_id": paper_code, "review_id": review_id,
                            "aspects": term_by_sentence, "mock": True})
    mapping = [{"term_raw": term, "term_norm": "result report" if term == "result reporting" else term,
                "term_type": "review_aspect",
                "major_class_final": aspect_class, "label_source_final": "SYNTHETIC TEST FIXTURE"}
               for aspect_class, first, second in CLASSES_AND_TERMS for term in (first, second)]
    write_csv(OUT / "sample_papers.csv", papers, list(papers[0]))
    write_jsonl(OUT / "sample_reviews.jsonl", reviews)
    write_jsonl(OUT / "mock_aspect_responses.jsonl", aspects)
    write_csv(OUT / "sample_term_mapping.csv", mapping, list(mapping[0]))
    write_csv(OUT / "sample_author_metadata.csv", authors, list(authors[0]))
    write_jsonl(OUT / "mock_author_responses.jsonl", provider_rows)
    (OUT / "SYNTHETIC_TEST_FIXTURE.txt").write_text(
        "SYNTHETIC TEST FIXTURE. Generated from independent templates; no research records. "
        "Software validation only; no scientific interpretation.\n", encoding="utf-8")
    return {"generator_version": GENERATOR_VERSION, "seed": RANDOM_SEED,
            "papers": len(papers), "reviews": len(reviews), "authors": len(authors),
            "mock_aspect_responses": len(aspects), "taxonomy_terms": len(mapping)}


if __name__ == "__main__":
    print(json.dumps(generate(), sort_keys=True))
