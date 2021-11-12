from typing import Any, Optional
from pydantic import BaseModel


class Feats(BaseModel):
    easy: str
    medium: str
    hard: str


class FeatsResponse(BaseModel):
    status: str = "Success"
    data: Optional[Feats]


