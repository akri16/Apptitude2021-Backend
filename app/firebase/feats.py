from firebase_admin import db, auth
from fastapi import HTTPException
import random
from ..constants import constants
from ..firebase.common import getUserDetails, isProblemStatementGenerationAllowed
from ..models.schemas import Feats, GenerateFeatResponse, Team


def __updateFeatCnt(curentVal: int):
    if not curentVal:
        return 1
    
    if curentVal < 3:
        return curentVal + 1

    raise HTTPException(status_code=403, detail=constants["FEAT_ALREADY_GENERATED"])

def getRandomFeatures():
    feats = db.reference('features').get()

    for x in ['easy', 'medium', 'hard']:
        feats[x] = random.choice(feats[x])

    return feats


def setFeat(id: str) -> Team:
    user = getUserDetails(id)

    if not isProblemStatementGenerationAllowed():
        raise HTTPException(status_code=403, detail=constants["FEAT_CANNOT_BE_GENERATED"])

    if not 'team' in user:
        raise HTTPException(status_code=403, detail=constants["NO_TEAM_JOINED"])
    
    teamId = user['team']
    featGenCntRef = db.reference(f'teams/{teamId}/featGenCnt')
    featRef = db.reference(f'teams/{teamId}/features')

    try:
        cnt: int = featGenCntRef.transaction(__updateFeatCnt)
        feats = getRandomFeatures()
        featRef.set(feats)
        return GenerateFeatResponse(features=Feats(**feats), featGenCnt=cnt)

    except db.TransactionAbortedError:
        raise HTTPException(status_code=500, detail=constants["INTERNAL_ERROR"])


