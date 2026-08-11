from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the embedding model once when this module is imported.
# 'all-MiniLM-L6-v2' is small, fast, and good enough for this kind of matching.
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text: str) -> np.ndarray:
    """Convert a piece of text into a numeric vector representing its meaning."""
    return model.encode(text)


def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Compares a resume and job description and returns a match score from 0-100.
    Higher score = more semantically similar (not just keyword overlap).
    """
    resume_embedding = get_embedding(resume_text)
    jd_embedding = get_embedding(job_description)

    similarity = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    score = round(float(similarity) * 100, 2)
    return score