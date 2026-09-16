"""Pipeline docstring
1. spaCy NER — Extract named entities from resume text. Categorize them: ORG, GPE, DATE, and skills.
2. TF-IDF Keyword Analysis — Extract important keywords and compare against target role.
3. Groq LLaMA 3.3 — Ask for ATS compatibility score, missing keywords, section-wise improvement tips, suggested bullet points, and action verbs.
"""

import os
from dotenv import load_dotenv
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from groq import Groq
client = Groq(api_key=GROQ_API_KEY)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_resume_entities(text):
    """Extracts entities and skill-like tokens using spaCy."""
    doc = nlp(text)
    entities = {
        "organizations": [],
        "locations": [],
        "dates": [],
        "skills": []
    }
    
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
            
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2:
            entities["skills"].append(token.text)
            
    # Deduplicate
    entities["organizations"] = list(set(entities["organizations"]))
    entities["locations"] = list(set(entities["locations"]))
    entities["dates"] = list(set(entities["dates"]))
    entities["skills"] = list(set(entities["skills"]))
    
    return entities

def analyze_keyword_gap(resume_text, target_role):
    """Uses TF-IDF to analyze keyword gaps between resume and target role context."""
    role_context = f"{target_role} requirements skills experience responsibilities qualifications"
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform([resume_text, role_context])
        feature_names = vectorizer.get_feature_names_out()
        
        resume_tfidf = X[0].toarray()[0]
        role_tfidf = X[1].toarray()[0]
        
        resume_keywords = [feature_names[i] for i in resume_tfidf.argsort()[-10:][::-1] if resume_tfidf[i] > 0]
        role_keywords = [feature_names[i] for i in role_tfidf.argsort()[-10:][::-1] if role_tfidf[i] > 0]
        
        return {
            "resume_keywords": resume_keywords,
            "role_context_keywords": role_keywords
        }
    except Exception as e:
        return {"error": str(e), "resume_keywords": [], "role_context_keywords": []}

def optimize_with_groq(resume_text, target_role, entities, keywords):
    """Sends extracted info to Groq for ATS optimization suggestions."""
    prompt = f"""
    You are an expert Resume Optimizer and ATS Consultant. 
    Analyze the following resume against the target role: "{target_role}".
    
    Resume Text:
    {resume_text}
    
    Extracted Entities:
    Organizations: {entities.get('organizations', [])}
    Skills: {entities.get('skills', [])}
    
    Keyword Analysis:
    Resume Keywords: {keywords.get('resume_keywords', [])}
    Role Keywords: {keywords.get('role_context_keywords', [])}
    
    Please provide:
    1. ATS compatibility score (0-100)
    2. Missing keywords for the target role
    3. Section-wise improvement tips
    4. Suggested bullet points
    5. Action verb recommendations
    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"

def optimize_resume(resume_text, target_role):
    """
    Main public orchestrator function to optimize a resume.
    """
    if not resume_text or len(resume_text.strip()) == 0:
        return {"status": "failed", "error": "Resume text cannot be empty"}
        
    word_count = len(resume_text.split())
    if word_count < 30:
        return {"status": "failed", "error": "Resume text must be at least 30 words long"}
        
    if not target_role or len(target_role.strip()) == 0:
        return {"status": "failed", "error": "Target role cannot be empty"}
        
    entities = extract_resume_entities(resume_text)
    keywords = analyze_keyword_gap(resume_text, target_role)
    groq_optimization = optimize_with_groq(resume_text, target_role, entities, keywords)
    
    return {
        "status": "success",
        "entities": entities,
        "keyword_analysis": keywords,
        "groq_optimization": groq_optimization
    }
