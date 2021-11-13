from firebase_admin import db, auth
from fastapi import HTTPException
import random
from app.constants import constants
from app.firebase.common import getUserDetails, hasEventStarted


def __updateFeats(curentVal):
    if curentVal == None:
        return getRandomFeatures()
    else:
        raise HTTPException(status_code=403, detail=constants["FEAT_ALREADY_GENERATED"])


def getRandomFeatures():
    feats = db.reference('features').get()

    for x in ['easy', 'medium', 'hard']:
        feats[x] = random.choice(feats[x])

    return feats


def setFeat(id: str):
    user = getUserDetails(id)

    if not hasEventStarted():
        raise HTTPException(status_code=403, detail=constants["EVENT_NOT_STARTED"])

    if not 'team' in user:
        raise HTTPException(status_code=403, detail=constants["NO_TEAM_JOINED"])
    
    teamId = user['team']
    teamRef = db.reference(f'teams/{teamId}')
    featRef = teamRef.child('features')

    team = teamRef.get()
    if team != None and 'features' not in team:
        try:
            return featRef.transaction(__updateFeats)
        except db.TransactionAbortedError:
            raise HTTPException(status_code=500, detail=constants["INTERNAL_ERROR"])

    if 'features' in team:
        raise HTTPException(status_code=403, detail=constants["FEAT_ALREADY_GENERATED"])

    if team == None:
        raise HTTPException(status_code=500, detail=constants["INVALID_STATE"]) 

    return None



