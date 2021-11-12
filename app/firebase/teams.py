from firebase_admin import db, auth
from fastapi import HTTPException
import random
from app.constants import constants
from app.firebase.common import getUserDetails, hasEventStarted
import time
from .models import Team


def checkTeamChangeAllowed():
    if hasEventStarted():
        raise HTTPException(status_code=403, detail=constants["EVENT_STARTED"])

    user = getUserDetails(id)

    if user['team'] is not None:
        raise HTTPException(status_code=403, detail=constants['USER_HAS_TEAM'])


def setTeam(id, code):
    teamRef = db.reference(f"users/{id}/team")

    if teamRef.get():
        raise HTTPException(status_code=403, detail=constants['USER_HAS_TEAM'])

    return teamRef.set(code)


def createTeam(id, name):
    teamRef = db.reference('teams')
    snapshot = teamRef.order_by_child('name').equalTo(name).get()

    checkTeamChangeAllowed()

    if snapshot:
        raise HTTPException(status_code=403, detail=constants['TEAM_NAME_EXISTS'])

    code = time.time()
    setTeam(code)
    return {
        code: teamRef.child(code).set(Team(name=name, members=[id]))
    }


def joinTeam(id, code):
    checkTeamChangeAllowed()

    def __updateTeam(members):
        if len(members) == 2:
            raise HTTPException(status_code=403, detail=constants['TEAM_FULL'])

        members.append(id)
        return members

    ref = db.reference(f'teams/{code}/members/')
    try:
        ref.transaction(__updateTeam)
        setTeam(id, code)
    except db.TransactionAbortedError:
        raise HTTPException(status_code=500, detail=constants["INTERNAL_ERROR"])


    