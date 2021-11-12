from fastapi import FastAPI
from fastapi.params import Depends

from .firebase.auth import FirebaseBearer
from .firebase import firebase
from .schemas import FeatsResponse
from . import docs


app = FastAPI(
    title=docs.title,
    description=docs.description,
    version=docs.version
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/feats/generate", response_model=FeatsResponse, tags=['features']) 
async def generateFeats(id = Depends(FirebaseBearer())) -> FeatsResponse:
    val = firebase.setFeat(id)
    return FeatsResponse(data=val)
