from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')

class Feats(BaseModel):
    easy: str
    medium: str
    hard: str

class Team(BaseModel):
    code: str

class BaseResponse(GenericModel, Generic[T]):
    status: str = "Success"
    data: Optional[T]

class EmptyResponse(BaseModel):
    status: str = "Success"

class CreateTeam(BaseModel):
    name: str


