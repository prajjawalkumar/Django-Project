import os
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")

try:
    from google import genai
    client = genai.Client(api_key=api_key)
    print("Testing gemini-2.5-flash...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Hello'
    )
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
