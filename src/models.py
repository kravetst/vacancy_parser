from pydantic import BaseModel, Field
from datetime import datetime


class Vacancy(BaseModel):
    title: str
    company: str
    url: str
    published_at: str
    keyword: str
    is_sent_to_telegram: bool = False
    is_written_to_google: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        extra = "ignore"
