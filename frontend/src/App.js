import React, { useState } from 'react';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchMarketPulse = async () => {
    setLoading(true);
    setData(null);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/market-pulse?ticker=${ticker}`);
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Error fetching market pulse:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>📈 Market Pulse</h1>

      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        placeholder="Enter stock ticker (e.g., TSLA)"
      />
      <button onClick={fetchMarketPulse} disabled={loading || !ticker}>
        {loading ? 'Loading...' : 'Get Pulse'}
      </button>

      {data && (
        <div className="result">
          <h2>📊 Ticker: {data.ticker}</h2>
          <p>
            <strong>Sentiment:</strong> {data.pulse}
          </p>
          <p>
            <strong>LLM Explanation:</strong> {data.llm_explanation}
          </p>

          <h3>📰 News:</h3>
          <ul>
            {data.news.map((item, index) => (
              <li key={index}>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  <strong>{item.title}</strong>
                </a>
                <p>{item.description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
