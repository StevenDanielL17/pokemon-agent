import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Use the new model name
model = genai.GenerativeModel('gemini-flash-latest')

print("Testing generation with gemini-flash-latest...")
try:
    response = model.generate_content("Say hello to PolyPuff!")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
