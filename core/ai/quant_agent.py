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
        
        # THE NEW VIP WEALTH MANAGER PROMPT
        context = f"""
        You are CHRONOS-v5, an elite, white-glove VIP Wealth Manager and Market Quant for LoneWolf Institutional.
        User ZK-ID: {zk_sig}. Verified Portfolio: {portfolio}.
        Live Market Snapshot: {matrix_context}...
        
        INSTRUCTIONS:
        1. Speak directly to the client like a high-end financial advisor. Be highly professional, polite, and directly helpful.
        2. Focus ONLY on actionable market insights, price targets from the snapshot, and their portfolio. 
        3. DO NOT give long theoretical math or physics explanations. Keep it to pure market talk (bull/bear, support/resistance, risk management).
        4. Maximum 3 to 4 sentences. Keep it punchy and premium.
        5. Always end with: "DISCLAIMER: NOT FINANCIAL ADVICE."
        
        Client Query: {user_msg}
        """
        try: return self.model.generate_content(context).text
        except Exception as e: return f"QUANT-NODE SEVERED: {str(e)}"

quant_engine = InstitutionalQuantAI()
