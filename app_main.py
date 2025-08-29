from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

app = FastAPI()
engine = create_engine("sqlite:///data/fiction_engine.db")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/health")
def health():
    return {"status": "ok"}
