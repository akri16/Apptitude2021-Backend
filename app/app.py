from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import FileResponse

from .firebase.auth import FirebaseBearer
from .firebase import feats, teams
from .schemas import *
from . import docs
from starlette.concurrency import run_in_threadpool


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
    val = await run_in_threadpool(feats.setFeat, id)
    return BaseResponse(data=val)


@app.post("/team", tags=['team'], response_model=BaseResponse[Team])
async def createTeam(createTeam: CreateTeam, id: str = Depends(FirebaseBearer())) -> BaseResponse[Team]:
    code = await run_in_threadpool(teams.createTeam, id, createTeam.name)
    return BaseResponse(data=Team(code=code))


@app.put("/team/{code}", tags=['team'], response_model=EmptyResponse)
async def joinTeam(code: int, id: str = Depends(FirebaseBearer())) -> EmptyResponse:
    await run_in_threadpool(teams.joinTeam, id, code)
    return EmptyResponse()


@app.get("/loaderio-bbee6adfa96244093c1f157a930fa71f/", include_in_schema=False)
async def test():
    return FileResponse("static/loaderio-02936ad9bf9a9b15ed1ba9646d645907.txt")

