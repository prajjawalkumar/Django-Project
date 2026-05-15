import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=FutureWarning)
load_dotenv()

from google import genai

# Initialize Gemini API client
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")

def generate_product_description(title, category, price=None):
    if not client:
        return "AI model not configured. Please check GEMINI_API_KEY."
    
    prompt = f"""
    You are an expert e-commerce copywriter. Write a compelling, SEO-friendly, and detailed product description for the following item:
    Product Title: {title}
    Category: {category}
    Price: {price if price else 'N/A'}
    
    The description should be 2-3 paragraphs long. Focus on the benefits, style, and why a customer would want to buy it.
    Use HTML formatting (e.g., <p>, <ul>, <li>, <strong>) to structure the description so it looks good on a website. Do not include `html` block markers, just return the raw HTML string.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```html"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        return f"Error generating description: {e}"

def chatbot_response(user_message, store_context=""):
    if not client:
        return "I am currently offline. Please check the AI configuration."
    
    system_prompt = f"""
    You are a helpful and polite customer support assistant for an online e-commerce clothing store.
    Your goal is to assist customers with their queries regarding products, policies, and navigation.
    Keep your responses concise, friendly, and formatted nicely (you can use basic HTML like <br> or <b> if needed, but plain text is also fine).
    
    Store Context (if any):
    {store_context}
    
    User says: "{user_message}"
    Assistant response:
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=system_prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I am having trouble processing your request right now. (Error: {str(e)})"

def parse_search_query(query, available_categories):
    """
    Uses Gemini to extract structured intent from a natural language search query.
    """
    if not client:
        return {"keywords": query, "category": None}
        
    categories_str = ", ".join(available_categories)
    
    prompt = f"""
    Analyze the following e-commerce search query: "{query}"
    
    Available Categories in our store: {categories_str}
    
    Task:
    1. Identify the core search keywords (what the user is actually looking for, removing filler words).
    2. Identify the closest matching category from the 'Available Categories' list, if any. If none match, return "None".
    
    Return the result strictly in this JSON format:
    {{
        "keywords": "core search terms",
        "category": "matched category or None"
    }}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        import json
        data = json.loads(text.strip())
        return data
    except Exception as e:
        return {"keywords": query, "category": None}

def get_ai_recommendations(target_item_title, target_category, all_items):
    """
    Given a target item and a list of all items, uses Gemini to select the 4 most recommended items.
    all_items is a list of dicts: [{'id': 1, 'title': '...', 'category': '...'}, ...]
    """
    if not client:
        return []
    
    import json
    
    prompt = f"""
    You are an AI e-commerce recommendation engine.
    The user is currently viewing:
    Title: {target_item_title}
    Category: {target_category}
    
    Below is a JSON list of available products in the store:
    {json.dumps(all_items)}
    
    Task: Pick exactly 4 product IDs that are the best complementary recommendations (e.g., matching outfit, similar style, or related accessories). Do not recommend the same product back.
    Return ONLY a JSON list of integers representing the recommended product IDs. For example: [12, 34, 5, 8]
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        recommended_ids = json.loads(text.strip())
        if isinstance(recommended_ids, list):
            return [int(id) for id in recommended_ids[:4]]
        return []
    except Exception as e:
        print("Recommendation error:", e)
        return []

def summarize_reviews(reviews_text_list):
    if not client or not reviews_text_list:
        return "No summary available."
        
    reviews_str = "\n".join([f"- {r}" for r in reviews_text_list])
    
    prompt = f"""
    You are an expert sentiment analyzer. Below are customer reviews for a single product.
    
    Reviews:
    {reviews_str}
    
    Task: Write a concise, 1-2 sentence helpful summary of what people think about this product. Highlight the main positives and any notable negatives.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return "Could not generate summary at this time."
