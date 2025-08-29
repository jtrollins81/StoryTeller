from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Source(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    platform: str
    url: str
    author: str
    posted_at: datetime
    raw_text: str

class Insight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: int
    sentiment: float
    unmet_demand: bool
    key_phrases: str
