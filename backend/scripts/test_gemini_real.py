import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

def test_gemini():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    print(f"Testing Gemini API with key: {api_key[:5]}...")
    
    try:
        genai.configure(api_key=api_key)
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Say 'Hello from Gemini!' if you can hear me.")
        print("\n=== Gemini Response ===")
        print(response.text)
        print("=======================")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_gemini()
