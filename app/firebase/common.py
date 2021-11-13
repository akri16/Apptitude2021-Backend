from fastapi.exceptions import HTTPException
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, auth

from app.constants import constants


def init():
    cred = credentials.Certificate('app/firebase/service-account.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://apptitude2021-backup-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })


def verify_id_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        return None
    
    return decoded_token


def getUserDetails(id):
    user = db.reference(f'participants/{id}').get()
    if user is None:
        raise HTTPException(status_code=403, detail=constants['USER_NOT_CREATED'])

    return user


def hasEventStarted():
    return db.reference('admin/allowProblemStatementGeneration').get()
