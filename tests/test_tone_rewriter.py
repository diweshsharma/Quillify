import sys
import os
import json

# Add parent directory to path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.tone_rewriter import rewrite_tone

def run_test():
    sample_text = "Hey man, the presentation is totally gonna crash and burn if we don't fix the slides right now. It's a huge mess!"
    desired_tone = "Professional"
    
    print("Testing Tone Rewriter...")
    print(f"Original Text: {sample_text}")
    print(f"Desired Tone: {desired_tone}")
    
    result = rewrite_tone(sample_text, desired_tone)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run_test()
