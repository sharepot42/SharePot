from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, params
from .Logger import logger
from .GroupFactory import GroupFactory

import time

def deleteUserFromGroup(db: Session, userId: int, groupId: int) -> bool:
    user = db.query(models.UserGroup).filter(
        models.UserGroup.user_id == userId,
        models.UserGroup.group_id == groupId
    ).first()
    try:
        if user:
            db.delete(user)
            db.commit()
            createUserMoveRecord(db, userId, groupId, params.EXIT)
    except Exception as err:
        logger.logger.error("Delete user from group")
        logger.logger.error(err)
        raise HTTPException(status_code=400, detail="Error: delete user from group failed")

def deleteUserByName(db: Session, user: models.User) -> bool:
    try:
        db.delete(user)
        db.commit()
    except Exception as err:
        logger.logger.error("Delete user")
        logger.logger.error(err)

def createUserMoveRecord(db: Session, userId: int, groupId: int, state: int):
    logger.logger.debug("Create new record")
    currTime = int(time.time())
    record = GroupFactory.createRecord(db, userId, groupId, currTime, state)
    logger.logger.debug(record)
    try:
        logger.logger.debug(record)
        logger.logger.debug(record.__dict__)
        db.add(record)
        db.commit()
    except Exception as err:
        logger.logger.error("Create record from user movement")
        logger.logger.error(err)
        raise HTTPException(status_code=400, detail="Error: record creation failed")

def addUserListToGroup(db: Session, group: int, users: List[str]):

    for user in users:

        userId = getSimpleUserByName(db, user)
        #async
        if getUserInGroup(db, userId[0], group.id):
            continue

        addUserToGroup(db, userId[0], group.id)
        #not wait, just at the end
        createUserMoveRecord(db, userId[0], group.id, params.ENTRY)

def addUserToGroup(db: Session, userId: int, groupId: int) -> bool:
    association = models.UserGroup(user_id=userId, group_id=groupId, state=params.STATE_ACTIVATE)
    try:

        db.add(association)
        db.commit()
    except Exception as err:
        logger.logger.error("Add user to group")
        logger.logger.error(err)

def getUserList(db: Session, users: List[str]) -> List[models.User]:
    return db.query(models.User.id).filter(models.User.username.in_(users)).all()

def getSimpleUserByName(db: Session, username: str) -> models.User:
    return db.query(models.User.id).filter(models.User.username == username).first()

def getUserByName(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

def getGroupByName(db: Session, name: str) -> models.Group:
    return db.query(models.Group).filter(models.Group.name == name).first()

def getSimpleGroupByName(db: Session, name: str) -> models.Group:
    return db.query(models.Group.id).filter(models.Group.name == name).first()

def getUserInGroup(db: Session, userId: int, groupId: int):
    return db.query(models.UserGroup).filter(
        models.UserGroup.user_id == userId,
        models.UserGroup.group_id == groupId
    ).first()

def setUserState(db: Session, userId: int, groupId: int, state: bool):
    userGroupDb = db.query(models.UserGroup).filter(
        models.UserGroup.user_id == userId,
        models.UserGroup.group_id == groupId
    ).first()
    userGroupDb.state = state
    db.commit()

#TODO handle if the user already exists
def createUser(
        db: Session,
        user: schemas.User
        ) -> schemas.User:

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as err:
        logger.logger.error("Create new user")
        logger.logger.error(err)
    return user

def createGroup(
        db: Session,
        group: models.Group,
        ) -> models.Group.id:

    try:
        db.add(group)
        db.commit()
        db.refresh(group)
    except Exception as err:
        logger.logger.error("Group creation failed because of: ")
        logger.logger.error(err)
    return group