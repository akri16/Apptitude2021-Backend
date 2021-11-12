from fastapi import FastAPI
from fastapi.params import Body, Depends

from .firebase.auth import FirebaseBearer
from .firebase import feats, teams
from .schemas import *
from . import docs


app = FastAPI(
    title=docs.title,
    description=docs.description,
    version=docs.version
)

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.put("/feats/generate", tags=['features'], response_model=BaseResponse[Feats]) 
async def generateFeats(id: str = Depends(FirebaseBearer())) -> BaseResponse[Feats]:
    val = feats.setFeat(id)
    return BaseResponse(data=val)


@app.post("/team", tags=['team'], response_model=BaseResponse[Team])
async def createTeam(createTeam: CreateTeam, id: str = Depends(FirebaseBearer())) -> BaseResponse[Team]:
    code = teams.createTeam(id, createTeam.name)
    return BaseResponse(data=Team(code=code))


@app.put("/team/{code}", tags=['team'], response_model=EmptyResponse)
async def joinTeam(code: int, id: str = Depends(FirebaseBearer())) -> EmptyResponse:
    teams.joinTeam(id, code)
    return EmptyResponse()


