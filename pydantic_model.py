from pydantic import BaseModel
from typing import Optional

class QueryInput(BaseModel):
  session_id : Optional[str] = None
  answer: Optional[str] = None
