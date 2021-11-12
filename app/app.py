from fastapi import FastAPI
from fastapi.params import Depends

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


@app.put("/feats/generate", tags=['features']) 
async def generateFeats(id: str = Depends(FirebaseBearer())) -> BaseResponse[Feats]:
    val = feats.setFeat(id)
    return BaseResponse(data=val)


@app.post("/team", tags=['team'])
async def createTeam(name: str, id: str = Depends(FirebaseBearer())) -> BaseResponse[Team]:
    val = teams.createTeam(id, name)
    code = val.keys()[0]
    members = val[code]['members']

    return BaseResponse(data=Team(code=code, name=name, members=members))


@app.put("/team/{code}", tags=['team'])
async def joinTeam(name: str, code: int, id: str = Depends(FirebaseBearer())) -> EmptyResponse:
    teams.joinTeam(id, code)
    return EmptyResponse()


