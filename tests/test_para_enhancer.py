import os
import sys
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.para_enhancer import enhance_paragraph

def test_enhance_paragraph():
    text = "Climate change is very bad for the world. The temperatures are going up and ice is melting fast. Animals are losing their homes and dying. We need to do something quick before it is too late."
    topic = "Climate Change Impacts"
    
    print("Testing Paragraph Enhancer Module...")
    print("-" * 50)
    print(f"Original Text: {text}")
    print(f"Topic: {topic}")
    print("-" * 50)
    
    result = enhance_paragraph(text, topic)
    
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'success':
        print("\nReadability:")
        print(f"Score: {result['readability']['score']}")
        print(f"Level: {result['readability']['level']}")
        
        print("\nSynonym Suggestions:")
        for word, syns in result['synonym_suggestions'].items():
            print(f"- {word}: {', '.join(syns)}")
            
        print("\nGroq Enhancement:")
        print(result['groq_enhancement'])
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    test_enhance_paragraph()
