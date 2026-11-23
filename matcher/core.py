import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skills import SKILLS


def extract_skills(text: str) -> set[str]:
    lowered = text.lower()
    return {skill for skill in SKILLS if re.search(rf"(?<![a-z0-9+]){re.escape(skill)}(?![a-z0-9])", lowered)}


@dataclass
class Match:
    job: str
    score: float
    matched_skills: list[str]
    missing_skills: list[str]


def rank_jobs(resume_text: str, jobs: dict[str, str], top_k: int | None = None) -> list[Match]:
    """Rank job descriptions against a resume: TF-IDF cosine similarity + skill gap."""
    names = list(jobs)
    corpus = [resume_text] + [jobs[name] for name in names]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus)
    scores = cosine_similarity(matrix[0:1], matrix[1:])[0]
    resume_skills = extract_skills(resume_text)
    matches = []
    for name, score in zip(names, scores):
        job_skills = extract_skills(jobs[name])
        matches.append(
            Match(
                job=name,
                score=round(float(score), 4),
                matched_skills=sorted(resume_skills & job_skills),
                missing_skills=sorted(job_skills - resume_skills),
            )
        )
    matches.sort(key=lambda m: m.score, reverse=True)
    return matches[:top_k] if top_k else matches
