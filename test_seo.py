from modules.seo_analyzer import analyze_blog

blog_text = """
Machine learning is a subset of artificial intelligence that enables 
computers to learn from data without being explicitly programmed. 
It uses algorithms to parse data, learn from it, and make informed 
decisions. Machine learning is used in many real world applications 
like recommendation systems, image recognition, natural language 
processing, and fraud detection. There are three main types of 
machine learning: supervised learning, unsupervised learning, and 
reinforcement learning. Python is the most popular language for 
machine learning due to its simplicity and powerful libraries like 
scikit-learn, TensorFlow, and PyTorch.
"""

blog_topic = "Machine Learning for Beginners"

result = analyze_blog(blog_text, blog_topic)

if result["status"] == "success":
    print("\n" + "="*50)
    print(f"Blog Topic    : {result['blog_topic']}")
    print(f"Word Count    : {result['word_count']}")
    print("\n📌 KeyBERT Keywords:")
    for kw, score in result["keyword_analysis"]["keybert_scores"].items():
        print(f"   {kw} → {score}")
    print("\n📌 TF-IDF Keywords:")
    for kw in result["keyword_analysis"]["tfidf_keywords"]:
        print(f"   {kw}")
    print("\n📌 Groq SEO Analysis:")
    print(result["gemini_seo_analysis"])
else:
    print(f"Error: {result['error']}")