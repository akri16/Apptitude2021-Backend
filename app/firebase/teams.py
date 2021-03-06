from firebase_admin import db
from fastapi import HTTPException
from ..constants import constants, MAX_TEAM_NAME_SIZE, MIN_TEAM_NAME_SIZE
from .common import getUserDetails, hasEventStarted
import time
from ..models.schemas import TeamPath


def checkTeamChangeAllowed():
    if hasEventStarted():
        raise HTTPException(status_code=403, detail=constants["EVENT_STARTED"])


def setTeam(id, code):
    teamRef = db.reference(f"participants/{id}/team")
    return teamRef.set(code)


def createTeam(id, name):
    name = name.strip()
    teamRef = db.reference('teams')
    snapshot = teamRef.order_by_child('name').equal_to(name).get()

    user = getUserDetails(id)
    if 'team' in user:
        raise HTTPException(status_code=403, detail=constants['USER_HAS_TEAM'])


    if len(name) > MAX_TEAM_NAME_SIZE or len(name) < MIN_TEAM_NAME_SIZE:
        raise HTTPException(status_code=400, detail=constants['INVALID_TEAM_NAME'])

    if snapshot:
        raise HTTPException(status_code=403, detail=constants['TEAM_NAME_EXISTS'])

    code = int(str(round(time.time_ns()))[3:14]) # Generate unique time based ids
    teamRef.child(str(code)).set({"name": name, "members": [id]})
    setTeam(id, code)
    
    return code


def joinTeam(id, code):
    checkTeamChangeAllowed()

    ref = db.reference(f'teams/{code}/members/')

    if not ref.get():
        raise HTTPException(status_code=404, detail=constants["INVALID_CODE"])

    user = getUserDetails(id)
    if 'team' in user and __getTeamSize(user['team']) == 2:
        raise HTTPException(status_code=403, detail=constants['USER_HAS_TEAM'])


    def __updateTeam(members):
        if len(members) == 2:
            raise HTTPException(status_code=403, detail=constants['TEAM_FULL'])

        if members[0] == id:
            raise HTTPException(status_code=403, detail=constants['OWN_TEAM'])

        members.append(id)
        return members

    try:
        ref.transaction(__updateTeam)
        if 'team' in user:
            db.reference(f"teams/{user['team']}").delete()
        setTeam(id, code)
    except db.TransactionAbortedError:
        raise HTTPException(status_code=500, detail=constants["INTERNAL_ERROR"])


def __getTeamSize(code: int):
    return len(db.reference(f'teams/{code}/members').get())

def getMembers(code=None, members=None):
    if not members: 
        members = db.reference(f'teams/{code}/members').get()
    l = []
    for x in members:
        l.append(db.reference(f'participants/{x}').get())
    return l

def getTeam(id: str, teamPath: TeamPath):
    user = getUserDetails(id)

    if 'team' not in user:
        raise HTTPException(status_code=403, detail=constants["NO_TEAM_JOINED"])

    code = user['team']

    if teamPath:
        if teamPath == teamPath.code:
            return code

        if teamPath == teamPath.members:  
            return getMembers(code=code)

        return db.reference(f'teams/{code}/{teamPath}').get()

    val = db.reference(f'teams/{code}/').get()
    val['code'] = code
    val['members'] = getMembers(members=val['members'])
    return val



