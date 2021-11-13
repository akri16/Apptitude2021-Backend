import os
from fastapi.exceptions import HTTPException
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, auth

from app.constants import constants


def init():
    cred = credentials.Certificate('app/firebase/service-account.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('DATABASE_URL')
    })


def verify_id_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        return None
    
    if decoded_token:
        return decoded_token['uid']


def getUserDetails(id: str):
    user = db.reference(f'participants/{id}').get()
    if user is None:
        raise HTTPException(status_code=403, detail=constants['USER_NOT_CREATED'])

    return user


def hasEventStarted():
    return db.reference('adminControl/allowProblemStatementGeneration').get()
