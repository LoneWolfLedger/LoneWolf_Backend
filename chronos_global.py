import yfinance as yf
import torch
import torch.nn as nn
import numpy as np
import json
import time
from scipy.fft import fft
from sklearn.preprocessing import StandardScaler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings('ignore')

# 1. THE GLOBAL OMNISCIENCE MATRIX
MARKETS = {
    "US_SP500": "^GSPC",
    "US_NASDAQ": "^IXIC",
    "INDIA_NIFTY": "^NSEI",
    "INDIA_SENSEX": "^BSESN",
    "CHINA_SHANGHAI": "000001.SS",
    "JAPAN_NIKKEI": "^N225",
    "SINGAPORE_STI": "^STI",
    "UK_FTSE": "^FTSE",
    "GOLD_COMEX": "GC=F",
    "CRUDE_OIL": "CL=F",
    "NATURAL_GAS": "NG=F",
    "BITCOIN": "BTC-USD",
    "ETHEREUM": "ETH-USD",
    "SOLANA": "SOL-USD"
}

print("[SYSTEM] INITIALIZING NEURO-SEMANTIC NLP ENGINE...")
analyzer = SentimentIntensityAnalyzer()

# 2. LIGHTWEIGHT LIQUID ODE TOPOLOGY
class LiquidSynapseODE(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.sensory = nn.Linear(input_dim, hidden_dim)
        self.time_gate = nn.Linear(hidden_dim, hidden_dim)
        self.activation = nn.Tanh()

    def forward(self, x, h_prev):
        sensory_input = self.activation(self.sensory(x))
        time_constant = torch.sigmoid(self.time_gate(h_prev))
        return h_prev + (-time_constant * h_prev + (1.0 - time_constant) * sensory_input)

class ChronosOmega(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.liquid = LiquidSynapseODE(input_dim, hidden_dim)
        self.decoder = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        batch_size, seq_len, _ = x.size()
        h_t = torch.zeros(batch_size, self.liquid.hidden_dim)
        for t in range(seq_len):
            h_t = self.liquid(x[:, t, :], h_t)
        return self.decoder(h_t)

# 3. THE ANALYTICAL CORE
def analyze_market(sector, ticker):
    try:
        # A. SCRAPE NLP NEWS SENTIMENT
        stock = yf.Ticker(ticker)
        news = stock.news
        sentiment_score = 0
        sentiment_label = "NEUTRAL"
        
        if news:
            scores = [analyzer.polarity_scores(n['title'])['compound'] for n in news[:5]] # Analyze top 5 headlines
            sentiment_score = np.mean(scores)
            if sentiment_score > 0.2: sentiment_label = "BULLISH (GREED)"
            elif sentiment_score < -0.2: sentiment_label = "BEARISH (FEAR)"

        # B. FETCH MATHEMATICAL CHAOS
        df = stock.history(period='5y', interval='1d')
        if df.empty: return {"error": "DATA DROPOUT"}
        
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        df['Vol'] = (df['High'] - df['Low']) / df['Close']
        
        # C. FOURIER SPECTRAL MAPPING
        prices = df['Close'].dropna().values
        yf_fft = fft(prices)
        dominant_freq = np.abs(yf_fft).argmax() / len(prices)
        df['Spectral'] = np.sin(2 * np.pi * dominant_freq * np.arange(len(df)))
        df.dropna(inplace=True)

        # D. TENSOR PREPARATION
        features = ['Log_Returns', 'Vol', 'Spectral']
        X_scaled = StandardScaler().fit_transform(df[features].values)
        y_scaled = StandardScaler().fit_transform(df[['Close']].values)

        SEQ_LENGTH = 30
        X = [X_scaled[i:(i + SEQ_LENGTH)] for i in range(len(X_scaled) - SEQ_LENGTH)]
        y = [y_scaled[i + SEQ_LENGTH, 0] for i in range(len(y_scaled) - SEQ_LENGTH)]
        
        X_tensor = torch.from_numpy(np.array(X)).float()
        y_tensor = torch.from_numpy(np.array(y)).float().unsqueeze(1)

        # E. NEURAL FORGING
        model = ChronosOmega(input_dim=len(features), hidden_dim=32)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()

        model.train()
        for epoch in range(40): # Optimized loop for global iteration
            optimizer.zero_grad()
            loss = criterion(model(X_tensor), y_tensor)
            loss.backward()
            optimizer.step()

        # F. MONTE CARLO EPISTEMIC UNCERTAINTY
        last_seq = torch.from_numpy(X_scaled[-SEQ_LENGTH:]).float().unsqueeze(0)
        simulations = [model(last_seq).item() for _ in range(50)]
        mean_pred = np.mean(simulations)
        uncertainty = np.std(simulations)
        
        current_price = float(df['Close'].values[-1])
        y_std, y_mean = np.std(df['Close'].values), np.mean(df['Close'].values)
        projected_target = (mean_pred * y_std) + y_mean
        epistemic = (uncertainty * y_std)
        
        # G. CONFLUENCE: MATH + SENTIMENT
        price_diff = projected_target - current_price
        conf = max(0, min(100, 100 - (epistemic / projected_target * 1000)))
        
        # Adjust confidence based on whether Math agrees with News
        if price_diff > 0 and sentiment_score > 0: conf = min(99.9, conf + 5)
        elif price_diff < 0 and sentiment_score < 0: conf = min(99.9, conf + 5)
        else: conf = max(10.0, conf - 15) # Divergence lowers confidence

        if price_diff > 0 and conf > 80: vector = "AGGRESSIVE BULL"
        elif price_diff > 0: vector = "BULLISH DIVERGENCE"
        elif price_diff < 0 and conf > 80: vector = "SEVERE BEAR"
        else: vector = "BEARISH CONTRACTION"

        return {
            "asset": ticker,
            "current_price": f"{current_price:.2f}",
            "projected_target": f"{projected_target:.2f}",
            "chronos_vector": vector,
            "nlp_sentiment": sentiment_label,
            "epistemic_uncertainty": f"±{epistemic:.2f}",
            "spectral_resonance": f"{dominant_freq:.5f} Hz",
            "accuracy_confidence": f"{conf:.2f}%"
        }
    except Exception as e:
        return {"asset": ticker, "error": str(e)}

print("[SYSTEM] IGNITING GLOBAL OMNISCIENCE...")
global_intel = {}
for sector, ticker in MARKETS.items():
    print(f"-> Extracting Math & NLP for {sector} ({ticker})...")
    global_intel[sector] = analyze_market(sector, ticker)
    time.sleep(2) # CRITICAL: Prevents Yahoo Finance from IP banning the GitHub server

with open("oracle_memory.json", "w") as f:
    json.dump(global_intel, f, indent=4)

print("[SYSTEM] GLOBAL OMNI-MATRIX SECURED.")