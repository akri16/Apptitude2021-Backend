from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field, HttpUrl, validator
from pydantic.generics import GenericModel
from enum import Enum

T = TypeVar('T')

class Feats(BaseModel):
    easy: str
    medium: str
    hard: str


class GenerateFeatResponse(BaseModel):
    features: Feats
    featGenCnt: int


class User(BaseModel):
    name: str
    emailId: str
    phoneNo: str
    team: Optional[int] = None


class Submission(BaseModel):
    github: HttpUrl
    video: Optional[HttpUrl]

    @validator('github')
    def check_url_host(cls, val):
        if val and val.host != 'github.com':
            raise ValueError('The host has to be github.com')
        return val


class Team(BaseModel):
    code: Optional[int]
    name: Optional[str]
    members: Optional[List[User]]
    features: Optional[Feats]
    submission: Optional[Submission]
    featGenCnt: Optional[int]


class BaseResponse(GenericModel, Generic[T]):
    status: str = "Success"
    data: Optional[T]

class EmptyResponse(BaseModel):
    status: str = "Success"

class CreateTeam(BaseModel):
    name: str = Field(
        None, max_length=30, min_length=3
    )

class TeamPath(str, Enum):
    members = "members"
    features = "features"
    submission = "submission"
    name = "name"
    code = "code"
    featGenCnt = "featGenCnt"



