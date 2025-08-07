from pydantic import BaseModel
from typing import List

class NewsItem(BaseModel):
    title: str
    description: str
    url: str

class Momentum(BaseModel):
    returns: List[float]
    score: float

class MarketPulseResponse(BaseModel):
    ticker: str
    as_of: str
    momentum: Momentum
    news: List[NewsItem]
    pulse: str
    llm_explanation: str
