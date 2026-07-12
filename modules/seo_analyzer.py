"""User Input
│
├── Blog Text
└── Blog Topic/Title
        │
        ▼
Step 1 — Text Cleaning (NLTK)
        Remove stopwords, punctuation, lowercase
        │
        ▼
Step 2 — Keyword Extraction (KeyBERT)
        Find most relevant keywords already in blog
        Uses BERT embeddings internally
        │
        ▼
Step 3 — SEO Gap Analysis (TF-IDF + Gemini)
        Compare existing keywords vs topic
        Find what keywords are MISSING
        │
        ▼
Step 4 — Gemini API (LLM)
        Suggest power keywords to add
        Give SEO improvement tips
        │
        ▼
Output
├── Keywords already in blog
├── Missing high value keywords
├── Suggested keywords to add
└── SEO tips specific to topic"""




import os
import re

from dotenv import load_dotenv

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


from groq import Groq
client = Groq(api_key=GROQ_API_KEY)




kw_model = KeyBERT()

def clean_text(text):
    
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    tokens = word_tokenize(text)

    
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    clean = ' '.join(filtered_tokens)

    return clean, filtered_tokens




def extract_keywords(text, blog_topic, top_n=10):
    clean, tokens = clean_text(text)

    keybert_keywords = kw_model.extract_keywords(
        clean,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_n,
        use_mmr=True,
        diversity=0.5
    )

    keybert_words = [kw[0] for kw in keybert_keywords]
    keybert_scores = {kw[0]: round(kw[1], 3) for kw in keybert_keywords}

   
    tfidf = TfidfVectorizer(
        max_features=20,
        stop_words='english',
        ngram_range=(1, 2)
    )

    tfidf_matrix = tfidf.fit_transform([clean])

    
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]

   
    tfidf_scores = dict(zip(feature_names, scores))

    
    tfidf_keywords = sorted(
        tfidf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    tfidf_words = [kw[0] for kw in tfidf_keywords]

    all_keywords = list(set(keybert_words + tfidf_words))

    return {
        "keybert_keywords": keybert_words,
        "keybert_scores": keybert_scores,
        "tfidf_keywords": tfidf_words,
        "combined_keywords": all_keywords
    }
    
    
def analyze_seo_with_groq(blog_text, blog_topic, existing_keywords):
    prompt = f"""
    You are an expert SEO analyst and content strategist with 10 years of experience.
    
    A blogger has written a blog post and needs your help to optimize it for search engines.
    
    BLOG TOPIC: {blog_topic}
    
    BLOG CONTENT:
    {blog_text}
    
    KEYWORDS ALREADY PRESENT IN BLOG:
    {', '.join(existing_keywords)}
    
    Your task is to analyze this blog and provide:
    
    1. SEO SCORE (out of 10):
       - Rate how SEO friendly this blog currently is
       - Give a brief reason for the score
    
    2. MISSING POWER KEYWORDS (give exactly 10):
       - High value keywords related to the topic
       - Keywords that are NOT already in the blog
       - Keywords people actually search for on Google
       - Include both short tail and long tail keywords
    
    3. KEYWORD PLACEMENT TIPS (give exactly 5):
       - Where exactly to place these keywords in the blog
       - Title, headings, first paragraph, meta description etc
    
    4. SEO IMPROVEMENT TIPS (give exactly 5):
       - Specific actionable tips to improve SEO
       - Based on the actual content of this blog
    
    5. CONTENT GAPS (give exactly 3):
       - Important subtopics related to {blog_topic} that are missing
       - Adding these will improve blog authority and ranking
    
    Format your response clearly with these exact section headers:
    SEO SCORE:
    MISSING POWER KEYWORDS:
    KEYWORD PLACEMENT TIPS:
    SEO IMPROVEMENT TIPS:
    CONTENT GAPS:
    """

    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert SEO analyst and content strategist with 10 years of experience."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content




def analyze_blog(blog_text, blog_topic):
    
    print(f"🔍 Analyzing blog for topic: {blog_topic}")

    
    if not blog_text or not blog_topic:
        return {
            "error": "Blog text and topic are required!",
            "status": "failed"
        }

    if len(blog_text.split()) < 50:
        return {
            "error": "Blog text is too short! Please provide at least 50 words.",
            "status": "failed"
        }

    print("📊 Extracting keywords...")
    keyword_results = extract_keywords(blog_text, blog_topic)

    
    print("🤖 Analyzing with Groq AI...")
    gemini_analysis = analyze_seo_with_groq(
        blog_text,
        blog_topic,
        keyword_results["combined_keywords"]
    )

    
    final_output = {
        "status": "success",
        "blog_topic": blog_topic,
        "word_count": len(blog_text.split()),
        "keyword_analysis": {
            "keybert_keywords": keyword_results["keybert_keywords"],
            "keybert_scores": keyword_results["keybert_scores"],
            "tfidf_keywords": keyword_results["tfidf_keywords"],
            "combined_keywords": keyword_results["combined_keywords"],
            "total_keywords_found": len(keyword_results["combined_keywords"])
        },
        "gemini_seo_analysis": gemini_analysis
    }

    print("✅ Analysis Complete!")
    return final_output