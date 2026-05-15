import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")
print("API KEY loaded:", bool(api_key))
genai.configure(api_key=api_key)

try:
    print("Testing gemini-pro...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello")
    print("Response gemini-pro:", response.text)
except Exception as e:
    print("Error gemini-pro:", e)
