import os
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Fixed imports: removed 'app.' prefix
from parser import ResumeParser
from ml_engine import MLEngine
from recommender import CareerRecommender

app = FastAPI(
    title="AI Resume Reviewer & Recommendation System",
    description="NLP & ML powered resume parsing, ATS scoring, skill gap analysis, and career role recommendation.",
    version="1.0.0"
)

# Fixed directory resolution: since main.py is in the root, we only need one dirname
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount Static assets and Templates
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Render main application home dashboard."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health_check():
    """Render health check endpoint."""
    return {"status": "healthy", "service": "AI Resume Reviewer"}


@app.post("/api/review")
async def review_resume(
    file: UploadFile = File(...),
    job_description: str = Form(default="")
):
    """
    API endpoint to upload a resume (PDF/DOCX/TXT) and process it using NLP/ML.
    Returns ATS score breakdown, matched/missing skills, formatting feedback, and role recommendations.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No resume file provided.")

    allowed_exts = ['pdf', 'docx', 'doc', 'txt']
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file format '.{ext}'. Please upload PDF, DOCX, or TXT.")

    try:
        contents = await file.read()
        raw_text = ResumeParser.parse_file(contents, file.filename)
        cleaned_text = ResumeParser.clean_text(raw_text)

        if not cleaned_text or len(cleaned_text.strip()) < 30:
            raise HTTPException(status_code=422, detail="Could not extract readable text from the document. Please ensure it is not scanned or password protected.")

        metadata = ResumeParser.extract_metadata(cleaned_text)
        ats_analysis = MLEngine.analyze_ats_compliance(cleaned_text, job_description, metadata)
        all_skills = ats_analysis["skills_extracted"].get("_all", [])
        recommendations = CareerRecommender.recommend_roles(all_skills)

        return JSONResponse(content={
            "filename": file.filename,
            "metadata": metadata,
            "ats_analysis": ats_analysis,
            "recommendations": recommendations,
            "preview_text": cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")


@app.get("/api/sample")
async def get_sample_review():
    """Return pre-computed sample resume analysis for instant demo testing."""
    sample_text = """
    ROHIT SHARMA
    Email: rohit.sharma@example.com | Phone: +1 (555) 019-2834 | LinkedIn: linkedin.com/in/rohitsharma | GitHub: github.com/rohitsharma
    
    PROFESSIONAL SUMMARY
    Innovative Machine Learning Engineer & Full Stack Developer with 3+ years of experience building scalable AI pipelines, predictive models, and REST APIs. Spearheaded model deployment reducing latency by 35% and optimized database queries improving throughput by 40%.
    
    SKILLS
    - Languages: Python, JavaScript, TypeScript, SQL, HTML, CSS
    - AI & ML: PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, NLP, Transformers, OpenCV
    - Web & Backend: FastAPI, Flask, React, Node.js, REST API, Microservices
    - Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Git, PostgreSQL, MongoDB
    
    EXPERIENCE
    AI Software Engineer | TechSolutions Inc. (2023 - Present)
    - Architected end-to-end NLP pipeline using Python, FastAPI, and Hugging Face Transformers for sentiment analysis on 500k+ customer reviews.
    - Automated CI/CD deployment pipelines using Docker and GitHub Actions, deploying services on AWS ECS.
    - Decreased inference response time by 35% using model quantization and Redis caching.
    
    Junior Data Scientist | Analytics Corp (2021 - 2023)
    - Developed churn prediction model using XGBoost and Scikit-Learn with 89% accuracy, saving $120,000 annually.
    - Built interactive analytics dashboards using React and Power BI for executive leadership.
    
    EDUCATION
    Bachelor of Science in Computer Science | State University (2017 - 2021)
    """

    metadata = ResumeParser.extract_metadata(sample_text)
    sample_jd = "Looking for a Senior ML Engineer with Python, PyTorch, Docker, AWS, FastAPI, CI/CD, Microservices, and SQL skills to build scalable AI applications."
    ats_analysis = MLEngine.analyze_ats_compliance(sample_text, sample_jd, metadata)
    all_skills = ats_analysis["skills_extracted"].get("_all", [])
    recommendations = CareerRecommender.recommend_roles(all_skills)

    return JSONResponse(content={
        "filename": "Sample_Resume_Rohit_Sharma.pdf",
        "metadata": metadata,
        "ats_analysis": ats_analysis,
        "recommendations": recommendations,
        "preview_text": sample_text[:500] + "..."
    })


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    # Fixed uvicorn target to match project structure
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
