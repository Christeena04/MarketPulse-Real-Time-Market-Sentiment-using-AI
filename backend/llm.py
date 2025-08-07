import os
import google.generativeai as genai
import json

# Set Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_pulse_from_llm(ticker: str, momentum: dict, news: list) -> dict:
    news_text = "\n".join([f"- {n['title']}" for n in news])

    prompt = f"""
You are a market analyst.

Given the following data for {ticker}, decide if the market outlook for tomorrow is 'bullish', 'bearish', or 'neutral', and explain why.

Momentum: returns = {momentum['returns']}, score = {momentum['score']}
News headlines:
{news_text}

Answer ONLY in this JSON format:
{{
  "pulse": "...",
  "explanation": "..."
}}
"""

    try:
        # Use a supported model (most stable as of now is "models/gemini-1.5-flash" or "models/gemini-1.5-pro")
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # or "models/gemini-1.5-pro"

        response = model.generate_content(prompt)

        return json.loads(response.text)

    except Exception as e:
        return {
            "pulse": "neutral",
            "explanation": f"Error using Gemini: {str(e)}"
        }
