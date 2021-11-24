from .common import getUserDetails
from firebase_admin import db
from fastapi import HTTPException
from ..constants import constants
from ..models.schemas import Submission

def submit(id: str, submission: Submission):
    user = getUserDetails(id)

    if 'team' not in user:
        raise HTTPException(status_code=403, detail=constants["NO_TEAM_JOINED"])

    if not db.reference('adminControl/allowSubmission').get():
        raise HTTPException(status_code=403, detail=constants["SUBMISSION_NOT_ALLOWED"])

    code = user['team']
    return db.reference(f'teams/{code}/submission').set(submission.dict())
