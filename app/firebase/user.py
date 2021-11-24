from fastapi.exceptions import HTTPException
from .common import getUserDetails
from ..constants import constants
from ..models.schemas import CreateUser, User
from firebase_admin import auth, db


def createUser(id: str, createUser: CreateUser) -> User:
    userRef = db.reference(f'participants/{id}')
    user = userRef.get()
    if user != None: 
        raise HTTPException(status_code=403, detail=constants['USER_ALREADY_EXISTS'])

    userRec: auth.UserRecord = auth.get_user(id)

    # phNo = None
    # for x in userRec.provider_data:
    #     if x.provider_id == "phone":
    #         phNo = x.phone_number
    #         break
        
    if userRec.email == None or not userRec.email_verified:
        raise HTTPException(status_code=403, detail=constants['NO_EMAIL_FOUND'])

    # if not phNo:
    #     raise HTTPException(status_code=403, detail=constants['NO_PHNO_FOUND'])

    newUser = User(**createUser.dict(), emailId=userRec.email)
    db.reference(f'participants/{id}').set(newUser.dict())

    return newUser

