from typing import Any
from fastapi import FastAPI
from fastapi.params import Body, Depends
from fastapi.responses import FileResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .firebase.auth import FirebaseBearer
from .firebase import feats, teams, submission, user, common, static
from .models.schemas import *
import docs
from starlette.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=docs.title,
    description=docs.description,
    version=docs.version
)

app.add_middleware(SentryAsgiMiddleware)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.post("/participant", tags=['user'], response_model=BaseResponse[User])
async def createUser(newUser: CreateUser, id: str = Depends(FirebaseBearer())) -> BaseResponse[User]:
    val: User = await run_in_threadpool(user.createUser, id, newUser)
    return BaseResponse(data=val)

@app.get("/participant", tags=['user'], response_model=BaseResponse[User])
async def getUser(id: str = Depends(FirebaseBearer())) -> BaseResponse[User]:
    val: User = await run_in_threadpool(common.getUserDetails, id)
    return BaseResponse(data=val)

@app.get("/participants/status", tags=['user'], response_model=BaseResponse[UserStatus])
async def getUserStatus(id: str = Depends(FirebaseBearer())) -> BaseResponse[UserStatus]:
    val: UserStatus = await run_in_threadpool(user.getUserStatus, id)
    return BaseResponse(data=val)

@app.get("/{static_path}", tags=['static'], response_model=BaseResponse[Any])
async def getStatic(static_path: StaticPath) -> BaseResponse[Any]:
    val = static.getStatic(static_path)
    return BaseResponse(data=val)


@app.get("/team/{team_path}", tags=['team'], response_model=BaseResponse[Team], response_model_exclude_none=True)
async def getTeam(
    team_path: TeamPath,
    id: str = Depends(FirebaseBearer())
) -> BaseResponse[Team]:
    val = await run_in_threadpool(teams.getTeam, id, team_path)
    return BaseResponse(data=Team(**{team_path: val}))


@app.get("/team/", response_model=BaseResponse[Team], tags=['team'])
async def getTeam(
    id: str = Depends(FirebaseBearer())
) -> BaseResponse[Team]:
    val = await run_in_threadpool(teams.getTeam, id, None)
    return BaseResponse(data=Team(**val))


@app.put("/feats/generate", status_code=201, tags=['team'], response_model=BaseResponse[GenerateFeatResponse]) 
async def generateFeats(id: str = Depends(FirebaseBearer())) -> BaseResponse[GenerateFeatResponse]:
    val = await run_in_threadpool(feats.setFeat, id)
    return BaseResponse(data=val)


@app.post("/team", tags=['team'], status_code=201, response_model=BaseResponse[Team], response_model_exclude_none=True)
async def createTeam(createTeam: CreateTeam, id: str = Depends(FirebaseBearer())) -> BaseResponse[Team]:
    code = await run_in_threadpool(teams.createTeam, id, createTeam.name)
    return BaseResponse(data=Team(code=code))


@app.put("/team/{code}", tags=['team'], response_model=EmptyResponse)
async def joinTeam(code: int, id: str = Depends(FirebaseBearer())) -> EmptyResponse:
    await run_in_threadpool(teams.joinTeam, id, code)
    return EmptyResponse()


@app.put("/submit", tags=['submit'], response_model=EmptyResponse)
async def submit(submissionBody: Submission, id: str = Depends(FirebaseBearer())) -> EmptyResponse:
    await run_in_threadpool(submission.submit, id, submissionBody)
    return EmptyResponse()


@app.get("/control/{control_path}", tags=['control'], response_model=BaseResponse[Any])
async def getControlPath(control_path: ControlPath) -> BaseResponse[Any]:
    val = await run_in_threadpool(common.getControlPath, control_path)
    return BaseResponse(data=val)

@app.get("/loaderio-bbee6adfa96244093c1f157a930fa71f/", include_in_schema=False)
async def test():
    return FileResponse("static/loaderio-02936ad9bf9a9b15ed1ba9646d645907.txt")

