from models.base_model import ScrapedData
from typing import Optional

class HealthData(ScrapedData):
    topic: Optional[str] = None
    author: Optional[str] = None
