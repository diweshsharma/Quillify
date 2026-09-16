"""Quillify — AI Powered Writing Assistant
FastAPI backend serving 4 NLP modules:
  /api/seo     — Blog SEO Analyzer
  /api/enhance — Paragraph Enhancer
  /api/resume  — Resume Optimizer
  /api/tone    — Tone Rewriter
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from modules.seo_analyzer import analyze_blog
from modules.para_enhancer import enhance_paragraph
from modules.resume_optimizer import optimize_resume
from modules.tone_rewriter import rewrite_tone

app = FastAPI(
    title="Quillify API",
    description="AI Powered Writing Assistant",
    version="1.0.0"
)

# CORS — allow frontend on different origins (Vercel, localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Models ──────────────────────────────────────

class SEORequest(BaseModel):
    blog_text: str
    blog_topic: str

class EnhanceRequest(BaseModel):
    text: str
    topic: str

class ResumeRequest(BaseModel):
    resume_text: str
    target_role: str

class ToneRequest(BaseModel):
    text: str
    desired_tone: str


# ── API Endpoints ───────────────────────────────────────

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "Quillify API", "version": "1.0.0"}

@app.post("/api/seo")
def seo_endpoint(req: SEORequest):
    return analyze_blog(req.blog_text, req.blog_topic)

@app.post("/api/enhance")
def enhance_endpoint(req: EnhanceRequest):
    return enhance_paragraph(req.text, req.topic)

@app.post("/api/resume")
def resume_endpoint(req: ResumeRequest):
    return optimize_resume(req.resume_text, req.target_role)

@app.post("/api/tone")
def tone_endpoint(req: ToneRequest):
    return rewrite_tone(req.text, req.desired_tone)


# ── Static Files (serve frontend in development) ───────

app.mount("/", StaticFiles(directory="static", html=True), name="static")
