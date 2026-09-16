import os
import sys

# Add modules dir to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

from resume_optimizer import optimize_resume

def test_resume_optimizer():
    sample_resume = '''
    John Doe
    Software Engineer
    
    Experience:
    Google - Software Engineer (Jan 2020 - Present)
    Developed backend systems using Python and Java. Built microservices for cloud deployment.
    Improved database query performance by 20%. Designed REST APIs for the new user portal.
    
    Education:
    B.S. in Computer Science, Stanford University (2015 - 2019)
    
    Skills: Python, Java, SQL, AWS, Docker, Kubernetes, React, JavaScript, Agile
    '''
    
    target_role = "Senior Software Engineer"
    
    print("Running Resume Optimizer...")
    result = optimize_resume(sample_resume, target_role)
    
    print(f"Status: {result.get('status')}")
    if result.get("status") == "success":
        print("\n=== Extracted Entities ===")
        print(result["entities"])
        print("\n=== Keyword Analysis ===")
        print(result["keyword_analysis"])
        print("\n=== Groq Optimization Suggestions ===")
        print(result["groq_optimization"])
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    test_resume_optimizer()
