import feedparser, numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
class NarrativeEconomics:
    def __init__(self):
        self.nlp = SentimentIntensityAnalyzer()
        self.sources = ['https://cointelegraph.com/rss', 'https://finance.yahoo.com/news/rssindex']
    def quantify_global_narrative(self):
        scores, narratives = [], []
        for url in self.sources:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]:
                    scores.append(self.nlp.polarity_scores(entry.title)['compound'])
                    narratives.append(entry.title)
            except: pass
        if not scores: return "EQUILIBRIUM", 0.0, ["AWAITING DATA"]
        macro_vector = np.mean(scores)
        if macro_vector > 0.25: regime = "IRRATIONAL EXUBERANCE (EXPANSION)"
        elif macro_vector < -0.25: regime = "SYSTEMIC RISK (CONTRACTION)"
        else: regime = "STOCHASTIC EQUILIBRIUM"
        return regime, macro_vector, narratives[:3]
