from firebase_admin import db
from fastapi import HTTPException
from app.constants import constants, MAX_TEAM_NAME_SIZE, MIN_TEAM_NAME_SIZE
from app.firebase.common import getUserDetails, hasEventStarted
import time


def checkTeamChangeAllowed(id):
    if hasEventStarted():
        raise HTTPException(status_code=403, detail=constants["EVENT_STARTED"])

    user = getUserDetails(id)

    if 'team' in user:
        raise HTTPException(status_code=403, detail=constants['USER_HAS_TEAM'])


def setTeam(id, code):
    teamRef = db.reference(f"participants/{id}/team")

    if teamRef.get():
        raise HTTPException(status_code=403, detail=constants['USER_HAS_TEAM'])

    return teamRef.set(code)


def createTeam(id, name):
    teamRef = db.reference('teams')
    snapshot = teamRef.order_by_child('name').equal_to(name).get()

    checkTeamChangeAllowed(id)

    name = name.strip()
    if len(name) > MAX_TEAM_NAME_SIZE or len(name) < MIN_TEAM_NAME_SIZE:
        raise HTTPException(status_code=400, detail=constants['INVALID_TEAM_NAME'])

    if snapshot:
        raise HTTPException(status_code=403, detail=constants['TEAM_NAME_EXISTS'])

    code = str(round(time.time()))
    teamRef.child(code).set({"name": name, "members": [id]})
    setTeam(id, code)
    
    return code


def joinTeam(id, code):
    checkTeamChangeAllowed(id)

    def __updateTeam(members):
        if len(members) == 2:
            raise HTTPException(status_code=403, detail=constants['TEAM_FULL'])

        if members[0] == id:
            raise HTTPException(status_code=403, detail=constants['OWN_TEAM'])

        members.append(id)
        return members

    ref = db.reference(f'teams/{code}/members/')

    if not ref.get():
        raise HTTPException(status_code=403, detail=constants["INVALID_CODE"])

    try:
        ref.transaction(__updateTeam)
        setTeam(id, code)
    except db.TransactionAbortedError:
        raise HTTPException(status_code=500, detail=constants["INTERNAL_ERROR"])


    