from transformers import pipeline
from sqlmodel import Session, select
from app_main import engine
from models import Source, Insight
import re

# Sentiment pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def extract_unmet_demand(text: str) -> (bool, str):
    # Simple pattern matching (expand later with NLP)
    patterns = [r"\bi wish\b", r"\bwant more\b", r"\bneed more\b", r"\blooking for\b"]
    found = [p for p in patterns if re.search(p, text.lower())]
    return (len(found) > 0, "; ".join(found))

def analyze_new_sources():
    with Session(engine) as s:
        results = s.exec(select(Source).where(Source.id.not_in(
            select(Insight.source_id)
        ))).all()
        for src in results:
            sentiment = sentiment_analyzer(src.raw_text[:512])[0]["score"] * (
                1 if sentiment_analyzer(src.raw_text[:512])[0]["label"] == "POSITIVE" else -1
            )
            unmet, phrases = extract_unmet_demand(src.raw_text)
            insight = Insight(
                source_id=src.id,
                sentiment=sentiment,
                unmet_demand=unmet,
                key_phrases=phrases
            )
            s.add(insight)
        s.commit()
    print(f"✅ Analyzed {len(results)} new posts")

if __name__ == "__main__":
    analyze_new_sources()
