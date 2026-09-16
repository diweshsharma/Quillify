# 🪶 Quillify — AI Powered Writing Assistant

> Your intelligent writing partner for SEO, enhancement, resume optimization, and tone rewriting

**Live Demo:** [https://quillify-ypwl.onrender.com](https://quillify-ypwl.onrender.com/)

---

## 📌 Project Overview

Quillify is an end-to-end Natural Language Processing (NLP) web application that serves as an AI-powered writing assistant. It combines classical NLP techniques with modern Large Language Models (LLMs) to help users optimize and enhance their written content across multiple use cases.

| Module | Function |
|--------|----------|
| Blog SEO Analyzer | Extracts keywords and suggests SEO improvements |
| Paragraph Enhancer | Suggests synonyms and rewrites paragraphs |
| Resume Optimizer | Analyzes resumes and suggests ATS-friendly keywords |
| Tone Rewriter | Detects and rewrites content in a desired tone |

Built with a **FastAPI** backend, **HTML/CSS/JavaScript** frontend, and ready for deployment on **Render** and **Vercel**.

---

## ❗ Problem Statement

In the digital age, content quality directly impacts visibility, opportunity, and communication effectiveness. However, most individuals face significant challenges:

- **Bloggers** struggle with SEO optimization — over 90% of online content receives zero organic traffic
- **Writers and Students** lack tools to assess readability and vocabulary strength in real time
- **Job Seekers** are unaware that 75% of resumes never reach a human reviewer due to ATS filtering
- **Professionals** need to adapt writing tone for different audiences but lack intelligent tools

Existing solutions like Grammarly, Surfer SEO, and Jobscan address these problems individually and charge premium fees ($50–$100/month). **Quillify fills this gap** by combining NLP and LLM technologies into a single, accessible, open-source writing assistant.

---

## 🎯 Objectives

- Develop a multi-module NLP application that addresses real-world writing challenges
- Implement keyword extraction using BERT-based models (KeyBERT) and TF-IDF
- Build synonym suggestion system using NLTK WordNet and spaCy POS tagging
- Integrate Large Language Models (LLaMA 3.3 via Groq API) for intelligent content generation
- Implement tone detection using HuggingFace pretrained transformer models
- Design and develop a clean, responsive web interface using HTML, CSS, and JavaScript
- Build a scalable REST API backend using FastAPI
- Deploy the complete application for public access

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│                HTML + CSS + JavaScript                   │
│                  (Vercel Deploy)                         │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP Requests
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND                         │
│                  REST API Server                         │
│                  (Render Deploy)                         │
│                                                         │
│   /api/seo    /api/enhance    /api/resume    /api/tone  │
└────┬──────────────┬──────────────┬──────────────┬───────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   SEO   │  │Paragraph │  │  Resume  │  │   Tone   │
│Analyzer │  │Enhancer  │  │Optimizer │  │ Rewriter │
└────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │            │              │              │
     ▼            ▼              ▼              ▼
┌─────────────────────────────────────────────────────────┐
│                      NLP LAYER                           │
│   KeyBERT │ TF-IDF │ spaCy │ NLTK │ HuggingFace        │
└─────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                      LLM LAYER                           │
│              Groq API (LLaMA 3.3 70B)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Modules

### Module 1 — Blog SEO Analyzer

**Purpose:** Analyzes blog content and suggests SEO improvements.

**Input:** Blog text + Blog topic/target keyword

**Process:**
1. Text cleaning using NLTK (stopword removal, tokenization)
2. Keyword extraction using KeyBERT (BERT embeddings)
3. Keyword scoring using TF-IDF
4. SEO gap analysis using Groq LLaMA 3.3

**Output:** SEO score, existing keywords, missing keywords, placement tips, improvement suggestions, content gaps

### Module 2 — Paragraph Enhancer

**Purpose:** Analyzes paragraphs and suggests improvements, synonyms, and AI-enhanced rewrites.

**Input:** Paragraph text + Topic

**Process:**
1. POS tagging using spaCy (identifies adjectives and verbs)
2. Synonym suggestions using NLTK WordNet
3. Readability scoring (Flesch Reading Ease)
4. AI enhancement using Groq LLaMA 3.3

**Output:** Synonym suggestions, readability score/level, improvement suggestions, enhanced rewrite

### Module 3 — Resume Optimizer

**Purpose:** Analyzes resumes against target job roles and suggests ATS-friendly keywords.

**Input:** Resume text + Target job role

**Process:**
1. Named Entity Recognition using spaCy (skills, organizations, education)
2. Keyword gap analysis using TF-IDF
3. ATS keyword suggestions using Groq LLaMA 3.3

**Output:** ATS score, skills found, missing keywords, section-wise tips, bullet point suggestions

### Module 4 — Tone Rewriter

**Purpose:** Detects current tone and rewrites in desired tone.

**Input:** Text + Desired tone (Professional/Casual/Formal/Friendly/Persuasive/Academic)

**Process:**
1. Tone detection using HuggingFace pretrained transformer
2. Tone rewriting using Groq LLaMA 3.3

**Output:** Detected tone, rewritten text, transformation explanation

---

## 🛠️ Tech Stack

### AI / NLP Layer
| Technology | Purpose |
|------------|---------|
| KeyBERT | BERT-based keyword extraction |
| sentence-transformers | BERT embeddings for KeyBERT |
| spaCy | POS tagging, NER, text processing |
| NLTK | WordNet synonyms, tokenization |
| scikit-learn | TF-IDF vectorization |
| HuggingFace Transformers | Pretrained tone classification |
| PyTorch | Deep learning backend |

### LLM Layer
| Technology | Purpose |
|------------|---------|
| Groq API | Free LLaMA 3.3 70B inference |
| LLaMA 3.3 70B Versatile | Core LLM for all generation tasks |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Python-dotenv | Environment variable management |
| Pydantic | Data validation |

### Frontend
| Technology | Purpose |
|------------|---------|
| HTML5 | Structure |
| CSS3 | Styling and animations |
| JavaScript (Vanilla) | Interactivity and API calls |

### Deployment
| Platform | Purpose |
|----------|---------|
| Render | FastAPI backend hosting |
| Vercel | Frontend hosting |
| GitHub | Version control |

---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.10+** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/downloads)
- **Groq API Key** (free) — Sign up at [console.groq.com](https://console.groq.com)

### Step 1 — Clone Repository
```bash
git clone https://github.com/yourusername/quillify.git
cd quillify
```

### Step 2 — Create Virtual Environment
```bash
python -m venv quillify_env
```
Activate it:
```bash
# Windows (Command Prompt)
quillify_env\Scripts\activate

# Windows (PowerShell)
quillify_env\Scripts\Activate.ps1

# Mac/Linux
source quillify_env/bin/activate
```
You should see `(quillify_env)` in your terminal prompt.

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```
> **Note:** This installs PyTorch, Transformers, spaCy, NLTK, KeyBERT, FastAPI, and other dependencies. First install may take 5-10 minutes.

### Step 4 — Download NLP Models
```bash
# spaCy English model
python -m spacy download en_core_web_sm

# NLTK data packages
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

### Step 5 — Configure Environment
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```
> Get your free API key from [console.groq.com/keys](https://console.groq.com/keys)

### Step 6 — Run the Application
```bash
uvicorn main:app --reload
```
You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 7 — Open in Browser
Open **http://localhost:8000** in your browser.

> **First launch note:** The HuggingFace emotion detection model (~300MB) downloads automatically on first run. This is a one-time download and may take 1-2 minutes depending on your internet speed.

---

## 🚀 Quick Run (After Setup)

Once installed, you only need two commands to run Quillify:

```bash
# 1. Activate virtual environment
quillify_env\Scripts\activate        # Windows
source quillify_env/bin/activate     # Mac/Linux

# 2. Start the server
uvicorn main:app --reload
```
Then open **http://localhost:8000** in your browser.

---

## 📁 Project Structure

```
Quillify/
│
├── modules/                    ← NLP Module files
│   ├── __init__.py
│   ├── seo_analyzer.py         ← Module 1: Blog SEO
│   ├── para_enhancer.py        ← Module 2: Paragraph
│   ├── resume_optimizer.py     ← Module 3: Resume
│   └── tone_rewriter.py        ← Module 4: Tone
│
├── static/                     ← Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/                      ← Test scripts
│   ├── test_para_enhancer.py
│   ├── test_resume_optimizer.py
│   └── test_tone_rewriter.py
│
├── main.py                     ← FastAPI application
├── requirements.txt            ← Python dependencies
├── .env                        ← API keys (not in git)
├── .gitignore
└── README.md
```

---

## 🔌 API Reference

**Base URL:** `http://localhost:8000`

### `POST /api/seo`
```json
// Request
{ "blog_text": "Your blog content...", "blog_topic": "Target Keyword" }

// Response
{ "status": "success", "keyword_analysis": {...}, "groq_seo_analysis": "..." }
```

### `POST /api/enhance`
```json
// Request
{ "text": "Your paragraph...", "topic": "Topic" }

// Response
{ "status": "success", "synonym_suggestions": {...}, "readability": {...}, "groq_enhancement": "..." }
```

### `POST /api/resume`
```json
// Request
{ "resume_text": "Resume content...", "target_role": "ML Engineer" }

// Response
{ "status": "success", "entities": {...}, "keyword_analysis": {...}, "groq_optimization": "..." }
```

### `POST /api/tone`
```json
// Request
{ "text": "Your text...", "desired_tone": "Professional" }

// Response
{ "status": "success", "detected_tone": "Friendly/Casual", "rewritten_text": "...", "desired_tone": "Professional" }
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

🪶 **Quillify** — Write Smarter, Rank Higher, Communicate Better

Built with ❤️ using Python, NLP, and LLMs

</div>
