# Resume Job Matcher

Rank job descriptions against your resume and see exactly which skills each role wants that you have - and which you are missing.

TF-IDF (1-2 word n-grams) cosine similarity for ranking, plus a transparent keyword taxonomy for the skill-gap report. No API keys, no black box: every score and every "missing skill" is inspectable.

## Why

When you apply to many jobs, the useful question is not "am I good?" but "which roles fit my current profile, and what should I add to my resume for this specific posting?" This tool answers both in one pass.

## Usage

```bash
pip install -r requirements.txt
python -m matcher.cli path/to/resume.txt 'jobs/*.txt' --top 5
```

Plain-text files in, ranked matches out. Sample data is included:

```bash
python -m matcher.cli samples/resume.txt 'samples/jobs/*.txt'
```

## Real output (bundled samples)

```
#1  ai-engineer  (similarity 0.197)
    matched skills : docker, embeddings, fastapi, llm, python, rag, sql, vector search
    missing skills : prompt engineering

#2  ml-engineer  (similarity 0.137)
    matched skills : docker, machine learning, python, pytorch, sql, tensorflow
    missing skills : airflow, aws, ci/cd, deep learning, kubernetes, nlp

#3  data-analyst  (similarity 0.121)
    matched skills : a/b testing, pandas, power bi, python, sql, statistics
    missing skills : excel, tableau

#4  backend-engineer  (similarity 0.018)
    matched skills : -
    missing skills : aws, ci/cd, java, kafka, kubernetes, postgresql, redis
```

The sample resume and job posts under `samples/` are fictional but realistic. Similarity scores are cosine similarities over TF-IDF vectors: relative ranking is the point, not the absolute number.

## How it works

1. `matcher/core.py` vectorizes the resume and all job descriptions with `TfidfVectorizer(stop_words="english", ngram_range=(1,2))` and ranks by cosine similarity.
2. `matcher/skills.py` is a flat, editable skill list; extraction uses word-boundary regex so "R" the language does not match "rust" and "C++" is handled explicitly.
3. The gap report is set difference: job skills minus resume skills.

## Honest limitations

- TF-IDF matches wording, not meaning: "built ML models" and "machine learning engineer" score well, but "worked on predictive systems" will not match "machine learning". (That is what the n-gram range and the skill taxonomy partly cover.)
- The skill list is small on purpose; extend `matcher/skills.py` for your field.
- Resumes in PDF/DOCX need converting to text first (`pdftotext` works well).

## Tests

```bash
pytest -q
```
