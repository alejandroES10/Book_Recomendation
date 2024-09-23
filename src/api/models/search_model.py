from pydantic import BaseModel
from typing import Optional

class SearchModel(BaseModel):
    content: str
    k_results: Optional[int] = 10
  