import re

KNOWN_SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css",
    "react", "angular", "vue", "node.js", "node", "express", "django", "flask",
    "fastapi", "sql", "mysql", "postgresql", "mongodb", "redis", "docker",
    "kubernetes", "aws", "azure", "gcp", "git", "github", "gitlab", "ci/cd",
    "rest api", "graphql", "machine learning", "deep learning", "ai",
    "artificial intelligence", "nlp", "computer vision", "data structures",
    "algorithms", "agile", "scrum", "linux", "bash", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn", "tableau", "power bi", "excel",
    "figma", "ui/ux", "testing", "unit testing", "microservices",
]


def extract_skills(text: str) -> set:
    text_lower = text.lower()
    found = set()
    for skill in KNOWN_SKILLS:
        pattern = r'(?<![a-zA-Z0-9])' + re.escape(skill) + r'(?![a-zA-Z0-9])'
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def analyze_resume_match(resume_text: str, job_description: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = resume_skills & job_skills
    missing_skills = sorted(job_skills - resume_skills)

    if job_skills:
        match_ratio = len(matched_skills) / len(job_skills)
    else:
        match_ratio = 0

    if match_ratio >= 0.7:
        explanation = (
            f"Strong match — the candidate has {len(matched_skills)} of "
            f"{len(job_skills)} key skills mentioned in the job description, "
            f"including {', '.join(sorted(matched_skills)) if matched_skills else 'several relevant areas'}."
        )
    elif match_ratio >= 0.4:
        explanation = (
            f"Moderate match — the candidate covers {len(matched_skills)} of "
            f"{len(job_skills)} key skills from the job description. "
            f"Some relevant gaps exist but the foundation is solid."
        )
    else:
        explanation = (
            f"Limited match — the candidate covers only {len(matched_skills)} of "
            f"{len(job_skills)} key skills explicitly mentioned in the job description. "
            f"Manual review is recommended to check for related experience not captured by keywords."
        )

    interview_questions = []
    if missing_skills:
        for skill in missing_skills[:3]:
            interview_questions.append(
                f"Do you have any experience with {skill}, even outside formal work/projects?"
            )
    else:
        for skill in list(matched_skills)[:3]:
            interview_questions.append(
                f"Can you walk me through a project where you used {skill}?"
            )

    if not interview_questions:
        interview_questions = [
            "Can you walk me through your most relevant project for this role?",
            "What excites you most about this position?",
            "How do you approach learning a new technology quickly?"
        ]

    return {
        "explanation": explanation,
        "missing_skills": missing_skills,
        "interview_questions": interview_questions
    }