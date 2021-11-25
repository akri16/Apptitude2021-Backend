from fastapi.exceptions import HTTPException

from app.firebase import common
from ..constants import constants
from ..models.schemas import CreateUser, StaticPath, User
from firebase_admin import auth, db


def getStatic(path: StaticPath):

    if path == StaticPath.problemStatements and not common.hasEventStarted():
        raise HTTPException(status_code=403, detail=constants['EVENT_NOT_STARTED'])

    return db.reference(path).get()

