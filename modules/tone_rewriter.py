"""
Tone Rewriter Module for Quillify.
Pipeline:
1. Detect current tone using HuggingFace 'j-hartmann/emotion-english-distilroberta-base'.
2. Use Groq LLaMA 3.3 to rewrite the text into the desired tone.
"""

import os
from dotenv import load_dotenv
from transformers import pipeline
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize HuggingFace pipeline once
tone_classifier = pipeline(
    'text-classification', 
    model='j-hartmann/emotion-english-distilroberta-base', 
    top_k=3,
    truncation=True
)

EMOTION_TO_TONE_MAP = {
    "joy": "Friendly/Casual",
    "neutral": "Professional/Formal",
    "anger": "Aggressive",
    "fear": "Cautious",
    "sadness": "Somber",
    "surprise": "Enthusiastic",
    "disgust": "Critical"
}

ALLOWED_TARGET_TONES = ["Professional", "Casual", "Formal", "Friendly", "Persuasive", "Academic"]


def detect_tone(text):
    """Detect tone using HuggingFace emotion classifier."""
    try:
        results = tone_classifier(text)
        if not results:
            return None
        
        # result for top_k is a list of lists of dicts e.g. [[{'label': 'joy', 'score': 0.9}]]
        top_emotions = results[0]
        
        primary_emotion = top_emotions[0]['label']
        primary_tone = EMOTION_TO_TONE_MAP.get(primary_emotion, "Unknown")
        confidence = top_emotions[0]['score']
        
        return {
            "primary_tone": primary_tone,
            "confidence": confidence,
            "top_emotions": top_emotions
        }
    except Exception as e:
        print(f"Error in detect_tone: {e}")
        return None

def rewrite_with_groq(text, detected_tone, desired_tone):
    """Rewrite text using Groq API."""
    prompt = (
        f"Rewrite the following text from its current tone ({detected_tone}) to a {desired_tone} tone.\n"
        f"Provide the rewritten text, an explanation of what was changed, and key modifications made.\n\n"
        f"Text:\n{text}\n"
    )
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are an expert NLP assistant that rewrites text for tone adjustment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in rewrite_with_groq: {e}")
        return None

def rewrite_tone(text, desired_tone):
    """
    Main public orchestrator function to rewrite text tone.
    """
    if not text or not isinstance(text, str):
        return {"status": "failed", "error": "Input text must be a non-empty string."}
    
    words = text.split()
    if len(words) < 5:
        return {"status": "failed", "error": "Input text must be at least 5 words long."}
        
    if desired_tone not in ALLOWED_TARGET_TONES:
        return {"status": "failed", "error": f"Desired tone must be one of {ALLOWED_TARGET_TONES}."}

    tone_info = detect_tone(text)
    if not tone_info:
        return {"status": "failed", "error": "Failed to detect tone."}
        
    rewritten_text = rewrite_with_groq(text, tone_info["primary_tone"], desired_tone)
    if not rewritten_text:
        return {"status": "failed", "error": "Failed to rewrite text with Groq."}
        
    return {
        "status": "success",
        "detected_tone": tone_info["primary_tone"],
        "confidence": round(tone_info["confidence"], 3),
        "top_emotions": tone_info["top_emotions"],
        "desired_tone": desired_tone,
        "rewritten_text": rewritten_text
    }
