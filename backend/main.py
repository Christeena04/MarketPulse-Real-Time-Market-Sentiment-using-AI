from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests
import json
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not GEMINI_API_KEY or not NEWS_API_KEY:
    raise Exception("API keys not found. Please check your .env file.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Create FastAPI app
app = FastAPI()

# CORS configuration: allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import re

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {
                "pulse": "neutral",
                "explanation": "LLM responded but JSON was malformed."
            }
    return {
        "pulse": "neutral",
        "explanation": "LLM response did not contain JSON."
    }

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "✅ Market Pulse API is working (with Gemini)!"}

# Market Pulse endpoint
@app.get("/api/v1/market-pulse")
def get_market_pulse(ticker: str):
    # Step 1: Get recent news about the ticker
    news_url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    
    try:
        news_resp = requests.get(news_url)
        news_data = news_resp.json()
    except Exception as e:
        return {"error": "Failed to fetch news", "details": str(e)}

    # Extract relevant news headlines
    headlines = []
    for article in news_data.get("articles", []):
        headlines.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"]
        })

    if not headlines:
        return {
            "ticker": ticker,
            "pulse": "neutral",
            "llm_explanation": "No recent news articles found.",
            "news": []
        }

    # Step 2: Prepare LLM prompt
    news_text = "\n".join([f"{n['title']} - {n['description']}" for n in headlines])
    prompt = f"""You are a financial expert. Based on the following recent news about {ticker}, determine the market sentiment (bullish, bearish, or neutral) and explain briefly.

News:
{news_text}

Respond with a JSON like:
{{
  "pulse": "bullish",
  "explanation": "short explanation here"
}}
"""

    # Step 3: Call Gemini API
    try:
        response = model.generate_content(prompt)
        content = response.text

        # Parse Gemini response
        llm_data = extract_json(content)

    except Exception as e:
        llm_data = {
            "pulse": "neutral",
            "explanation": f"Could not interpret LLM response: {str(e)}"
        }

    # Step 4: Return to frontend
    return {
        "ticker": ticker,
        "pulse": llm_data["pulse"],
        "llm_explanation": llm_data["explanation"],
        "news": headlines
    }
