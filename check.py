
print("Checking all Quillify dependencies...\n")

try:
    import google.generativeai as genai
    print("✅ google-generativeai")
except:
    print("❌ google-generativeai — run: pip install google-generativeai")

try:
    import langchain
    print("✅ langchain")
except:
    print("❌ langchain — run: pip install langchain")

try:
    import langchain_google_genai
    print("✅ langchain-google-genai")
except:
    print("❌ langchain-google-genai — run: pip install langchain-google-genai")

try:
    import keybert
    print("✅ keybert")
except:
    print("❌ keybert — run: pip install keybert")

try:
    import sentence_transformers
    print("✅ sentence-transformers")
except:
    print("❌ sentence-transformers — run: pip install sentence-transformers")

try:
    import spacy
    print("✅ spacy")
except:
    print("❌ spacy — run: pip install spacy")

try:
    import nltk
    print("✅ nltk")
except:
    print("❌ nltk — run: pip install nltk")

try:
    import transformers
    print("✅ transformers")
except:
    print("❌ transformers — run: pip install transformers")

try:
    import torch
    print("✅ torch")
except:
    print("❌ torch — run: pip install torch")

try:
    import streamlit
    print("✅ streamlit")
except:
    print("❌ streamlit — run: pip install streamlit")

try:
    import fastapi
    print("✅ fastapi")
except:
    print("❌ fastapi — run: pip install fastapi")

try:
    import uvicorn
    print("✅ uvicorn")
except:
    print("❌ uvicorn — run: pip install uvicorn")

try:
    import sklearn
    print("✅ scikit-learn")
except:
    print("❌ scikit-learn — run: pip install scikit-learn")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv")
except:
    print("❌ python-dotenv — run: pip install python-dotenv")

print("\n")

# Check CUDA
try:
    import torch
    if torch.cuda.is_available():
        print(f"✅ CUDA Available → {torch.cuda.get_device_name(0)}")
        print(f"✅ VRAM → {round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 1)} GB")
    else:
        print("⚠️ CUDA not available → will use CPU")
except:
    print("⚠️ Could not check CUDA")

print("\n")

# Check spaCy model
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy English model (en_core_web_sm)")
except:
    print("❌ spaCy model missing → run: python -m spacy download en_core_web_sm")

# Check NLTK data
try:
    import nltk
    from nltk.corpus import wordnet
    from nltk.corpus import stopwords
    print("✅ NLTK WordNet data")
    print("✅ NLTK Stopwords data")
except:
    print("❌ NLTK data missing → run the nltk.download commands")

print("\n")
print("=" * 40)
print("🪶 Quillify Dependency Check Complete!")
print("=" * 40)