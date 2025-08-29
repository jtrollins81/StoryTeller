import streamlit as st
from sqlmodel import Session, select
from app_main import engine
from models import Source, Insight
import pandas as pd

st.title("📊 Fiction Engine - Market Insights")

with Session(engine) as s:
    rows = s.exec(select(Source, Insight).join(Insight, Source.id == Insight.source_id)).all()

data = []
for src, ins in rows:
    data.append({
        "Platform": src.platform,
        "URL": src.url,
        "Date": src.posted_at,
        "Text": src.raw_text[:200] + "...",
        "Sentiment": ins.sentiment,
        "Unmet Demand": ins.unmet_demand,
        "Phrases": ins.key_phrases
    })

df = pd.DataFrame(data)

if not df.empty:
    st.dataframe(df)
    unmet_df = df[df["Unmet Demand"] == True]
    st.subheader("🔥 Top Unmet Demands")
    st.table(unmet_df[["Date", "Text", "Phrases"]].head(10))
else:
    st.write("No insights yet. Run scraper + analyzer first.")
