# AI Resume Matcher

🔗 **Live demo:** https://ai-resume-matcher-riya.netlify.app/

An AI-powered tool that analyzes how well a resume matches a job description — using semantic embeddings to calculate a match score, identify missing skills, and generate relevant interview questions.


## Features

- 📄 **PDF Resume Parsing** — extracts raw text from uploaded resume PDFs
- 🧠 **Semantic Matching** — uses sentence embeddings (not just keyword matching) to calculate a 0–100 match score between a resume and job description
- 🔍 **Skill Gap Analysis** — automatically detects which required skills are missing from the candidate's resume
- 💬 **Interview Question Suggestions** — generates relevant interview questions based on the specific resume and role
- 🖥️ **Simple Web Interface** — clean, responsive frontend to upload a resume and paste a job description

## Tech Stack

- **Backend:** Python, FastAPI
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Similarity Scoring:** scikit-learn (cosine similarity)
- **PDF Parsing:** pypdf
- **Frontend:** HTML, CSS, vanilla JavaScript

## How It Works

1. User uploads a resume (PDF) and pastes a job description
2. The backend extracts text from the PDF
3. Both texts are converted into vector embeddings that capture their semantic meaning
4. Cosine similarity between the two embeddings produces a match score
5. A skill-matching layer cross-references known technical skills to flag any gaps
6. The API returns the score, an explanation, missing skills, and suggested interview questions — all rendered in the frontend

## Running Locally

\`\`\`bash
# Clone the repo
git clone https://github.com/riya10112005/ai-resume-matcher.git
cd ai-resume-matcher

# Set up a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload
\`\`\`

Then open `index.html` in your browser (make sure the backend is running first).

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/upload-resume` | POST | Upload a PDF and extract its text |
| `/match` | POST | Upload a resume + job description, get a match score |
| `/analyze` | POST | Full analysis — match score, explanation, missing skills, interview questions |

## Future Improvements

- [ ] Support for multiple resumes ranked against one job description
- [ ] PostgreSQL storage for resume/job history
- [ ] Dockerized deployment
- [ ] Support for `.docx` resumes

## Author

Riya Bhowmik
[LinkedIn](https://www.linkedin.com/in/riya-bhowmik10)