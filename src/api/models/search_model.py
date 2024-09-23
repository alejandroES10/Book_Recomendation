from pydantic import BaseModel

class SearchModel(BaseModel):
    content: str
    k_results: int 
  