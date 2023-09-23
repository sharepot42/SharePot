from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .Logger import logger

def deleteUserFromGroup(db: Session, userId: int, groupId: int) -> bool:
    user = db.query(models.UserGroup).filter(
        models.UserGroup.user_id == userId,
        models.UserGroup.group_id == groupId
    ).first()
    if user:
        db.delete(user)
        db.commit()
        return False
    return True

def deleteUserByName(db: Session, user: models.User) -> bool:
    db.delete(user)
    db.commit()
    return False

def connecUserListWithGroup(db: Session, groupId: int, userIds: List[int]) -> bool:
    logger.logger.debug(userIds)
    logger.logger.debug(groupId)
    for userId in userIds:
        connecUserWithGroup(db, userId[0], groupId)
    db.commit()
    return False

def connecUserWithGroup(db: Session, groupId: int, userId: int) -> bool:
    association = models.UserGroup(user_id=userId, group_id=groupId, state=True)
    db.add(association)

def getUserList(db: Session, users: List[str]) -> List[models.User]:
    logger.logger.debug(users)
    return db.query(models.User.id).filter(models.User.username.in_(users)).all()

def getUserByName(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

def getGroupByName(db: Session, name: str) -> models.Group:
    return db.query(models.Group).filter(models.Group.name == name).first()

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
    logger.logger.debug(userId)
    logger.logger.debug(groupId)
    logger.logger.debug(userGroupDb)
    userGroupDb.state = state
    db.commit()

#TODO handle if the user already exists
def createUser(
        db: Session,
        user: schemas.UserCreate
        ) -> schemas.User:
    dbUser = models.User(
        username=user.username,
        password=user.password,
        email=user.email)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

def createGroup(
        db: Session,
        group: schemas.GroupCreate,
        user_id: int
        ) -> models.Group:

    dbGroup = models.Group(
        name=group.name,
        description=group.description,
        admin_user_id=user_id,
        tax=group.tax
        )
    db.add(dbGroup)
    db.commit()
    db.refresh(dbGroup)
    return dbGroup