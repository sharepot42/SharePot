#HASH

from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas, database, params
from .Logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def checkAdmin() -> None:
    db: Session = next(database.getDB())
    dbUser = crud.getUserByName(db, params.APP_CREDENTIALS["username"])
    if dbUser is None:
        dbUser = schemas.User(
            username=params.APP_CREDENTIALS["username"],
            password=params.APP_CREDENTIALS["password"],
            email=params.APP_CREDENTIALS["email"]
        )
        dbUser.password = getPasswordHash(dbUser.password)
        crud.createUser(db, dbUser)
    db.close()

def authUser(db: Session, username: str, password: str) -> bool:
    user = crud.getUserByName(db, username)
    if not user or\
        not verifyPassword(password, user.password):
        return False
    return user

def createAccesstToken(data: dict, expireDelta: timedelta | None = None):
    toEncode = data.copy()
    if expireDelta:
        expire = datetime.utcnow() + expireDelta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)
    toEncode.update({"exp":expire})
    encodedJWT = jwt.encode(toEncode, params.AUTH_SECRET, algorithm=params.AUTH_ALGORITHM)
    return encodedJWT

async def getCurrUser(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(database.getDB),
        ) -> schemas.AuthUser:

    credentialException = HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer "},
    )
    try:
        payload = jwt.decode(token, params.AUTH_SECRET, algorithms=[params.AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentialException
        tokenData = schemas.TokenData(username=username)
    except JWTError:
        raise credentialException
    user = crud.getUserByName(db, username=tokenData.username)
    if user is None:
        raise credentialException
    return schemas.AuthUser(username=user.username)

def verifyPassword(plainPassword: str, hashedPassword: str):
    return pwdContext.verify(plainPassword, hashedPassword)

async def getCurrActiveUser(currUser: Annotated[schemas.AuthUser, Depends(getCurrUser)]):
    if currUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return currUser

def getPasswordHash(password: str):
    return pwdContext.hash(password)