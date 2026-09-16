"""Paragraph Enhancer Module for Quillify

Pipeline:
1. spaCy POS Tagging: Identifies adjectives (ADJ) and verbs (VERB) as enhancement candidates.
2. NLTK WordNet: Finds synonym suggestions for the identified candidates.
3. Flesch Reading Ease: Calculates readability score and maps to a difficulty level.
4. Groq LLaMA 3.3: Generates 5 specific improvement suggestions, an enhanced rewrite, and an explanation of changes.
"""

import os
import re
import spacy
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from dotenv import load_dotenv

# Download NLTK resources
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt_tab', quiet=True)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from groq import Groq
client = Groq(api_key=GROQ_API_KEY)

import gc

def get_synonym_suggestions(text):
    """Get synonym suggestions for adjectives and verbs using spaCy and WordNet."""
    # Load spacy model locally to save memory
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
        
    doc = nlp(text)
    
    # Free memory immediately
    del nlp
    gc.collect()
    synonyms_dict = {}
    
    for token in doc:
        if token.pos_ in ["ADJ", "VERB"] and len(token.text) > 3:
            word = token.text.lower()
            if word not in synonyms_dict:
                synsets = wordnet.synsets(word)
                synonyms = set()
                for syn in synsets:
                    for lemma in syn.lemmas():
                        if lemma.name() != word and '_' not in lemma.name():
                            synonyms.add(lemma.name())
                if synonyms:
                    # Limit to 5 synonyms for brevity
                    synonyms_dict[word] = list(synonyms)[:5]
    return synonyms_dict

def count_syllables(word):
    """Estimate the number of syllables in a word."""
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def calculate_readability(text):
    """Calculate Flesch Reading Ease score and corresponding level."""
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [w for w in words if w.isalnum()]
    
    if not sentences or not words:
        return {"score": 0, "level": "Very Confusing"}
        
    avg_sentence_length = len(words) / len(sentences)
    total_syllables = sum(count_syllables(word) for word in words)
    avg_syllables_per_word = total_syllables / len(words)
    
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    
    if score >= 90:
        level = "Very Easy"
    elif score >= 80:
        level = "Easy"
    elif score >= 70:
        level = "Fairly Easy"
    elif score >= 60:
        level = "Standard"
    elif score >= 50:
        level = "Fairly Difficult"
    elif score >= 30:
        level = "Difficult"
    else:
        level = "Very Confusing"
        
    return {"score": round(score, 2), "level": level}

def enhance_with_groq(text, topic, synonyms, readability):
    """Enhance paragraph using Groq LLaMA 3.3 model."""
    prompt = f"""
    You are an expert AI writing assistant. Enhance the following paragraph about the topic: "{topic}".
    
    Original Text:
    {text}
    
    Readability Analysis:
    Score: {readability['score']} ({readability['level']})
    
    Suggested Synonyms for key words:
    {synonyms}
    
    Please provide:
    1. 5 specific improvement suggestions.
    2. An enhanced rewrite of the paragraph.
    3. An explanation of the changes made.
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq API: {str(e)}"

def enhance_paragraph(text, topic):
    """
    Public orchestrator to enhance a paragraph.
    Validates input and returns a structured dictionary.
    """
    if not text or not text.strip():
        return {"status": "failed", "error": "Text cannot be empty."}
        
    word_count = len([w for w in text.split() if w.strip()])
    if word_count < 10:
        return {"status": "failed", "error": "Text must be at least 10 words long."}
        
    synonyms = get_synonym_suggestions(text)
    readability = calculate_readability(text)
    groq_enhancement = enhance_with_groq(text, topic, synonyms, readability)
    
    return {
        "status": "success",
        "synonym_suggestions": synonyms,
        "readability": readability,
        "groq_enhancement": groq_enhancement
    }
