import os
import google.generativeai as genai
class InstitutionalQuantAI:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key: genai.configure(api_key=self.api_key)
        self.model_name = 'models/gemini-1.5-flash'
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                    self.model_name = m.name; break
        except: pass
        self.model = genai.GenerativeModel(self.model_name)
    def generate_risk_analysis(self, user_msg, zk_sig, portfolio, live_matrix):
        matrix_context = str(live_matrix)[:1000] 
        context = f"""You are CHRONOS-OMEGA, an Institutional Quant AI. 
        User ZK-ID: {zk_sig}. VERIFIED PORTFOLIO: {portfolio}.
        Matrix Snapshot: {matrix_context}...
        Calculate Expected Return. Cite academic literature (Gatheral, Peters).
        End with: "PROBABILITY SYNTHESIS ONLY. NOT FINANCIAL ADVICE."
        Max 4 sentences. Tone: Cold, elite, mathematical. Query: {user_msg}"""
        try: return self.model.generate_content(context).text
        except Exception as e: return f"QUANT-NODE SEVERED: {str(e)}"
quant_engine = InstitutionalQuantAI()
