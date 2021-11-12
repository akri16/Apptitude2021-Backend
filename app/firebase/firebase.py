import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, auth
from fastapi import HTTPException
import random
from app.constants import constants


def init():
    cred = credentials.Certificate('app/firebase/service-account.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://acminternal.firebaseio.com/'
    })


def __updateFeats(curentVal):
    if curentVal == None:
        return getRandomFeatures()
    else:
        return curentVal

def verify_id_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        return None
    
    return decoded_token

def getRandomFeatures():
    feats = db.reference('features').get()

    for x in ['easy', 'medium', 'hard']:
        feats[x] = random.choice(feats[x])

    return feats

def getUserDetails(id):
    return db.reference(f'users/{id}').get()

def setFeat(id):
    user = getUserDetails(id)
    canGenerateStatements = db.reference('admin/allowProblemStatementGeneration').get()

    if not canGenerateStatements:
        raise HTTPException(status_code=403, detail=constants["EVENT_NOT_STARTED"])

    if not 'teamId' in user:
        return HTTPException(status_code=403, detail=constants["NO_TEAM_JOINED"])
    
    teamId = user['teamId']
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



