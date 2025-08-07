import yfinance as yf
from datetime import datetime

def get_momentum(ticker: str):
    data = yf.Ticker(ticker).history(period="7d")  # covers weekends
    closes = data['Close'].dropna().tolist()

    if len(closes) < 6:
        return {"returns": [], "score": 0.0}

    returns = [round((closes[i+1] - closes[i]) / closes[i], 4)
               for i in range(-6, -1)]

    score = round(sum(returns) / len(returns), 4)
    return {"returns": returns, "score": score}
