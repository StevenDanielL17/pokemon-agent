import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key length: {len(api_key)}")
    print(f"API Key prefix: {api_key[:4]}...")

genai.configure(api_key=api_key)

print("\nListing models:")
try:
    count = 0
    for m in genai.list_models():
        print(f"- {m.name}")
        count += 1
    print(f"Total models found: {count}")
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTesting generation with 'gemini-1.5-flash':")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error with gemini-1.5-flash: {e}")

print("\nTesting generation with 'gemini-pro':")
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error with gemini-pro: {e}")
