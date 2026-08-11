from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from pypdf import PdfReader
from matcher import calculate_match_score
from ai_analysis import analyze_resume_match
import io

app = FastAPI(title="AI Resume Matcher")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Simple health check — visit this to confirm the server is running."""
    return {"message": "AI Resume Matcher API is running"}


def extract_pdf_text(contents: bytes) -> str:
    """Helper: extract raw text from PDF file bytes."""
    reader = PdfReader(io.BytesIO(contents))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Accepts a PDF resume upload and extracts its raw text."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    contents = await file.read()

    try:
        extracted_text = extract_pdf_text(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {str(e)}")

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text found in PDF (it may be a scanned image, not real text)"
        )

    return {
        "filename": file.filename,
        "character_count": len(extracted_text),
        "extracted_text": extracted_text
    }


@app.post("/match")
async def match_resume_to_job(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Accepts a PDF resume + a job description text, and returns a match score
    showing how semantically similar the resume is to the job.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    contents = await file.read()

    try:
        resume_text = extract_pdf_text(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {str(e)}")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")

    score = calculate_match_score(resume_text, job_description)

    return {
        "filename": file.filename,
        "match_score": score,
        "note": "Score out of 100 — higher means more semantically similar to the job description"
    }
    
@app.post("/analyze")
async def analyze_match(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Full AI-powered analysis: match score + explanation + missing skills + interview questions.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    contents = await file.read()

    try:
        resume_text = extract_pdf_text(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {str(e)}")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")

    score = calculate_match_score(resume_text, job_description)
    ai_analysis = analyze_resume_match(resume_text, job_description)

    return {
        "filename": file.filename,
        "match_score": score,
        "explanation": ai_analysis.get("explanation"),
        "missing_skills": ai_analysis.get("missing_skills"),
        "interview_questions": ai_analysis.get("interview_questions")
    }