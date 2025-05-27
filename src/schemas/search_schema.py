from pydantic import BaseModel
from typing import Optional

class SearchSchema(BaseModel):
    content: str
    k_results: Optional[int] = 10
  