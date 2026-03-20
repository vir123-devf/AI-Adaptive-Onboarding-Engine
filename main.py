from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from skill_extractor import extract_skills, extract_text_from_pdf
from gap_analyzer import GapAnalyzer
from adaptive_pather import AdaptivePather
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Adaptive Onboarding Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],  # Vite dev
    allow_methods=["*"],
    allow_headers=["*"],
)

pather = AdaptivePather()  # Loaded once at startup


@app.get("/")
async def root():
    """Serve the index.html file at the root path"""
    return FileResponse("index.html", media_type="text/html")


class PathwayRequest(BaseModel):
    resume_text: str = None
    jd_text: str = None
    max_hours: float = 40.0


@app.post("/api/analyze")
async def analyze(
    resume_file: UploadFile = File(None),
    jd_file: UploadFile = File(None),
    resume_text: str = Form(None),
    jd_text: str = Form(None),
    max_hours: float = Form(40.0)
):
    """
    Analyze skill gaps from resume and job description.
    Accepts both file uploads (PDF) and text input.
    """
    try:
        # Extract text from resume (file or text)
        if resume_file:
            logger.info(f"Reading resume from file: {resume_file.filename}")
            resume_content = await resume_file.read()
            resume_text = extract_text_from_pdf(resume_content)
        elif not resume_text:
            raise HTTPException(status_code=400, detail="Resume file or text is required")
        
        # Extract text from JD (file or text)
        if jd_file:
            logger.info(f"Reading JD from file: {jd_file.filename}")
            jd_content = await jd_file.read()
            jd_text = extract_text_from_pdf(jd_content)
        elif not jd_text:
            raise HTTPException(status_code=400, detail="Job description file or text is required")

        logger.info("Extracting skills from resume...")
        candidate_skills = extract_skills(resume_text, doc_type="resume")

        logger.info("Extracting skills from JD...")
        required_skills = extract_skills(jd_text, doc_type="jd")

        # Gap analysis
        analyzer = GapAnalyzer()
        analyzer.build_candidate_index([s.skill for s in candidate_skills.skills])
        gaps = analyzer.compute_gaps([s.skill for s in required_skills.skills])

        # Adaptive pathway
        pathway = pather.build_pathway(gaps, max_hours=40.0)

        return {
            "candidate_profile": candidate_skills.model_dump(),
            "required_profile": required_skills.model_dump(),
            "skill_gaps": [
                {
                    "skill": g.required_skill,
                    "severity": round(g.gap_severity, 3),
                    "closest_match": g.closest_match,
                    "similarity": round(g.similarity_score, 3)
                }
                for g in gaps
            ],
            "pathway": {
                "courses": [
                    {
                        "id": c.id,
                        "title": c.title,
                        "skills_covered": c.skills_covered,
                        "duration_hours": c.duration_hours,
                        "difficulty": c.difficulty,
                        "url": c.url,
                        "prerequisites": c.prerequisites
                    }
                    for c in pathway.ordered_courses
                ],
                "total_hours": pathway.total_hours,
                "skill_coverage": pathway.skill_coverage,
                "reasoning_trace": pathway.reasoning_trace
            }
        }
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    logger.info("Anthropic API Key configured: " + ("Yes" if os.getenv("ANTHROPIC_API_KEY") else "No (using mock mode)"))
    
    uvicorn.run(app, host=host, port=port, log_level="info")