from matcher.core import extract_skills, rank_jobs

RESUME = "Python developer with scikit-learn, pandas and SQL experience. Built FastAPI services."


def test_extract_skills_word_boundaries():
    assert "python" in extract_skills(RESUME)
    assert "r" not in extract_skills("I like rust and ruby")
    assert "c++" in extract_skills("systems work in C++")


def test_ranking_prefers_overlapping_job():
    jobs = {
        "ml": "Python machine learning scikit-learn pandas SQL role",
        "java": "Java spring microservices kubernetes role",
    }
    matches = rank_jobs(RESUME, jobs)
    assert matches[0].job == "ml"
    assert matches[0].score > matches[1].score
    assert "python" in matches[0].matched_skills
    assert "machine learning" in matches[0].missing_skills
