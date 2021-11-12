from typing import Any, Optional
from pydantic import BaseModel


class Feats(BaseModel):
    easy: str
    medium: str
    hard: str

class Team(BaseModel):
    code: int
    name: str
    members: List[str]

class BaseResponse(GenericModel, Generic[T]):
    status: str = "Success"
    data: Optional[T]

class EmptyResponse(BaseModel):
    status: str = "Success"


