from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ScrapedData(BaseModel):
    title: str
    link: str
    description: Optional[str] = None
    published: Optional[str] = None
    source: str
    scraped_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    category: str
