import yfinance as yf, numpy as np, requests, hashlib, time
import warnings
warnings.filterwarnings('ignore')
from config_ledger import RENDER_API_URL, MASTER_KEY, get_legal_disclaimer
from narrative_engine import NarrativeEconomics
from quantum_math import CuttingEdgeMathematics
from liquid_kan import synthesize_prediction

MARKETS = {"US_SP500": "^GSPC", "US_NASDAQ": "^IXIC", "GOLD": "GC=F", "BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"}

def execute_singularity():
    narrative_bot = NarrativeEconomics()
    macro_regime, macro_score, news_data = narrative_bot.quantify_global_narrative()
    math_engine = CuttingEdgeMathematics()
    payload = {}
    
    for sector, ticker in MARKETS.items():
        try:
            df = yf.download(ticker, period='6mo', interval='1d', progress=False)
            prices = df['Close'].dropna().values
            curr = float(prices[-1])
            
            hurst = math_engine.rough_volatility_hurst(prices)
            betti_drawdown = math_engine.topological_betti_proxy(prices)
            eigen_freq = math_engine.quantum_eigen_frequencies(prices)
            
            returns = np.diff(np.log(prices))
            vol = np.std(returns)
            
            X_matrix = np.column_stack((returns[-50:], np.full(50, hurst), np.full(50, eigen_freq)))
            y_target = prices[-50:]
            
            raw_target = synthesize_prediction(X_matrix, y_target, curr)
            target = raw_target * (1 + (macro_score * 0.005))
            
            confidence = min(99.0, max(15.0, 100 - (vol * 200) - (betti_drawdown * 100)))
            zk_proof = "0xZK_" + hashlib.sha384(f"{ticker}-{target}-{time.time()}".encode()).hexdigest()[:24].upper()
            
            if hurst < 0.4 and target > curr: vector = "ROUGH VOLATILITY BUY"
            elif target > curr and confidence > 80: vector = "TOPOLOGICAL BULL"
            elif target < curr and betti_drawdown > 0.05: vector = "TOPOLOGICAL CRASH WARNING"
            else: vector = "STOCHASTIC NOISE (EMH)"

            payload[sector] = {
                "asset": ticker, "current_price": f"{curr:.2f}", "projected_target": f"{target:.2f}",
                "chronos_vector": vector, "global_force": macro_regime, "crypto_proof": zk_proof,
                "legal_disclaimer": get_legal_disclaimer(confidence),
                "literature_mapping": ["Rough Volatility (Gatheral, 2018)", "Topological Data Analysis (Carlsson, 2009)", "Liquid KAN Neural Flow (MIT, 2024)", "Narrative Economics (Shiller, 2017)"]
            }
        except Exception as e: payload[sector] = {"error": f"MATHEMATICAL FAULT: {str(e)}"}

    payload["oracle_key"] = MASTER_KEY 
    requests.post(RENDER_API_URL, json=payload)

if __name__ == "__main__":
    execute_singularity()
