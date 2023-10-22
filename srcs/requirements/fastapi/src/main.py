import asyncio
from datetime import timedelta
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.logger import logger

from . import models, schemas, database, auth, params, UserFactory, GroupFactory
from .database import engine
from .Logger import logger
from .Checker import Checker

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
auth.checkAdmin()
userFactory = UserFactory.UserFactory()
groupFactory = GroupFactory.GroupFactory()

@app.get("/newGroup")
async def newGroup(
    group: schemas.GroupCreate,
    _: schemas.AuthUser = Depends(auth.getCurrUser)) -> dict:
    return {"message": "new group created"}

@app.post("/token", response_model=schemas.Token, include_in_schema=False)
async def loginForAccessToken(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.getDB)
    ):
    user = auth.authUser(db, formData.username, formData.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessTokenExpires = timedelta(params.AUTH_JWT_TIMEOUT)
    accessToken = auth.createAccesstToken(
        data={"sub": user.username},
        expireDelta=accessTokenExpires
    )
    return {"access_token": accessToken, "token_type": "Bearer"}

@app.get("/users/me", response_model=schemas.AuthUser, include_in_schema=False)
async def pathGetCurrUser(
    currUser: Annotated[schemas.AuthUser,
    Depends(auth.getCurrActiveUser)]
    ):
    return currUser

@app.delete("/group/deleteUser")
async def deleteUserFromGroup(
    username: str,
    groupname: str,
    _: schemas.AuthUser = Depends(auth.getCurrUser),
    db: Session = Depends(database.getDB),
    ):
    Checker.deleteUserFromGroup(db, username, groupname)
    return {"message": "user deleted succesfully"}

@app.patch("/group/addUser")
async def addUserToGroup(
    username: str,
    groupname: str,
    paymentReference: str,
    _: schemas.AuthUser = Depends(auth.getCurrUser),
    db: Session = Depends(database.getDB)
    ):

    Checker.addUserToGroup(db, username, groupname, paymentReference)
    return {"message": "User added succerfully"}

@app.patch("/group/deactivateUser")
async def deactivateUserFromGroup(
    username: str,
    groupname: str,
    _: schemas.AuthUser = Depends(auth.getCurrUser),
    db: Session = Depends(database.getDB)
    ):

    logger.logger.debug("START")
    Checker.setUserState(db, username, groupname, params.STATE_DEACTIVATE)
    return {"message": "User deactivated succerfully"}

@app.patch("/group/activateUser")
async def activateUserFromGroup(
    username: str,
    groupname: str,
    _: schemas.AuthUser = Depends(auth.getCurrUser),
    db: Session = Depends(database.getDB)
    ):

    Checker.setUserState(db, username, groupname, params.STATE_ACTIVATE)
    return {"message": "User activated succerfully"}

@app.post("/newGroup")
async def newGroup(
    group: schemas.GroupCreate,
    _: schemas.AuthUser = Depends(auth.getCurrUser),
    db: Session = Depends(database.getDB)
    ) -> dict:

    groupDb = groupFactory.createGroup(db, group)    

    Checker.createGroup(db, groupDb, group.user_list)
    return {"message": "new group created"}

@app.post("/newUser")
async def newUser(
    user: schemas.UserCreate, 
    _: Annotated[schemas.AuthUser, Depends(auth.getCurrActiveUser)],
    db: Session = Depends(database.getDB)) -> dict:
    
    userDb = await userFactory.create_user(db, user)
    Checker.createUser(db, userDb)
    return {"messag": "user created succesfully"}

@app.post("/newUsers")
async def newUser(
    users: List[schemas.UserCreate], 
    _: Annotated[schemas.AuthUser, Depends(auth.getCurrActiveUser)],
    db: Session = Depends(database.getDB)) -> dict:
    
    tasks = [userFactory.create_user(db, user) for user in users]
    users = await asyncio.gather(*tasks)
    for user in users:
        Checker.userExists(db, user.username)
        Checker.createUser(db, user)
    return {"message": "Users create succesfully"}