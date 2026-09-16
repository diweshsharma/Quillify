import requests
import time
import sys
import io

# Fix printing unicode to windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

URL = "http://127.0.0.1:8001/api"

print("Waiting for server to start...")
time.sleep(2)

print("1. Testing Paragraph Enhancer...")
res = requests.post(f"{URL}/enhance", json={
    "text": "The quick brown fox jumps over the lazy dog repeatedly while the cat sleeps lazily on the couch.",
    "topic": "Animals"
})
print(res.json())
print("-" * 50)

print("2. Testing Tone Rewriter...")
res = requests.post(f"{URL}/tone", json={
    "text": "I really hate when this happens. It's so frustrating and annoying.",
    "desired_tone": "Professional"
})
print(res.json())
print("-" * 50)

print("3. Testing SEO Analyzer...")
res = requests.post(f"{URL}/seo", json={
    "blog_text": "This is a blog post about artificial intelligence and machine learning. AI is transforming the world. Machine learning models like ChatGPT are getting smarter every day. Technology is evolving rapidly, and the future is AI. It is important to realize that artificial intelligence is not just a buzzword, it is a fundamental shift in how computing works and how businesses operate. From self driving cars to medical diagnosis, machine learning algorithms are providing value in numerous different industries and use cases. We need to prepare for this new era of innovation.",
    "blog_topic": "Artificial Intelligence"
})
print(res.json())
print("-" * 50)

print("4. Testing Resume Optimizer...")
res = requests.post(f"{URL}/resume", json={
    "resume_text": "I am a software engineer at Google with experience in Python and Java. I have worked for 5 years in San Francisco. I know how to build scalable backend APIs and design microservices architecture. My skills include Kubernetes, Docker, AWS, GCP, SQL, and NoSQL databases like MongoDB. I graduated from Stanford University with a degree in Computer Science. I am very passionate about coding and building large scale distributed systems.",
    "target_role": "Backend Developer"
})
print(res.json())
print("-" * 50)
