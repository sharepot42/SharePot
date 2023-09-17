from typing import Annotated
from fastapi import FastAPI, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.logger import logger

from . import crud, models, schemas
from .database import engine, SessionLocal

#HASH
from jose import JWTError, jwt
from passlib.context import CryptContext

import os

SECRET = os.environ["HASH_SECRET"]
ALGORITHM = "HS256"
JWT_EXPIRE_TIME = 30

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authUser(db: Session, username: str, password: str) -> bool:
    user = crud.getUser(db, username)
    if not User or\
        not verifyPassword(password, user.password):
        return False
    return user

import datetime

def createAccesstToken(data: dict, expireDelta: datetime.timedelta | None = None):
    toEncode = data.copy()
    if expireDelta:
        expire = datetime.datetime.utcnow() + expireDelta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    toEncode.update({"exp":expire})
    encodedJWT = jwt.encode(toEncode, SECRET, algorithm=ALGORITHM)
    return encodedJWT

class Token(BaseModel):
    accessToken: str
    tokenType: str

class TokenData(BaseModel):
    username: str

#dependency
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    username: str = Query(min_length=3,
                      max_length=12,
                      regex="^[a-zA-Z0-9_-]+$",
                      description="Nombre de usuario")

    password: str = Query(min_length=8,
                          max_length=16,
                          regex="^[a-zA-Z0-9_-]+$",
                          description="Contrasena de usuario")

class TestUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class Group(BaseModel):
    name: str = Query(min_length=3, max_length=12,regex="^[a-zA-Z0-9_-]+$")
    description: str

app = FastAPI()

@app.get("/")
async def root() -> dict:
    return {"message": "test"}

#@app.get("/security")
#async def getSecurity(token: Annotated[str, Depends(oauth2_scheme)]):
#    return {"testing" : token}

@app.get("/newGroup")
async def newGroup(group: Group) -> dict:
    return {"message": "new group created"}

def fake_decode_token(token: str) -> str:
    return TestUser(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def getCurrUser(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(getDB),
        ) -> TestUser:

    credentialException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer "},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username in None:
            raise credentialException
        tokenData = TokenData(username=username)
    except JWTError:
        raise credentialException
    user = crud.getUser(db, username=tokenData.username)
    if user is None:
        raise credentialException
    return TestUser(username=user.username)

def verifyPassword(plainPassword: str, hashedPassword: str):
    return pwdContext.verify(plainPassword, hashedPassword)

async def getCurrActiveUser(currUser: Annotated[TestUser, Depends(getCurrUser)]):
    if currUser.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return currUser

def getPasswordHash(password: str):
    return pwdContext.hash(password)

@app.post("/token", response_model=Token)
async def loginForAccessToken(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(getDB)
    ):
    user = authUser(db, formData.username, formData.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNATHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessTokenExpires = datetime.timedelta(JWT_EXPIRE_TIME)
    accessToken = createAccesstToken(
        data={"sub": user.username},
        expireDelta=accessTokenExpires
    )
    return {"accessToken": accessToken, "tokenType": "Bearer"}

@app.get("/users/me", response_model=TestUser)
async def pathGetCurrUser(currUser: Annotated[TestUser, Depends(getCurrActiveUser)]):
    logger.info("USERS ME")
    return currUser

@app.post("/newUser")
async def newUser(
    user: User, 
    _: Annotated[TestUser, Depends(getCurrActiveUser)],
    db: Session = Depends(getDB)) -> dict:
    
    hashedPassword = getPasswordHash(user.password)
    userDB = crud.getUser(db, user.username)
    if userDB:
        raise HTTPException(status_code=400, detail="username already registered")

    createUser = schemas.UserCreate(username=user.username, password=hashedPassword)
    userDB = crud.createUser(db, createUser)
    if userDB:
        return {"message": "User create succesfully"}
    return {"messag": "Something went wrong"}