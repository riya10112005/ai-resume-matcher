from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(resume_text: str, job_description: str) -> float:
    """
    Compares a resume and job description and returns a match score from 0-100.
    Uses TF-IDF (term frequency-inverse document frequency) + cosine similarity —
    a lightweight, well-established NLP technique that doesn't require loading
    a large deep learning model, making it fast and memory-efficient to deploy.
    """
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    score = round(float(similarity) * 100, 2)
    return score