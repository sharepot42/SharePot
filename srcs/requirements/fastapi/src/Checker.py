from typing import List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session
from dataclasses import dataclass
from . import crud, models, params
from .Logger import logger

@dataclass
class Checker:

    @staticmethod
    def userInGroup(db: Session, userId: int, groupId: int):
        userDb = crud.getUserInGroup(db, userId, groupId)
        if userDb is not None:
            raise HTTPException(status_code=400, detail="Error: User is already in the group")
        return userDb

    def userNotInGroup(db: Session, userId: int, groupId: int):
        userDb = crud.getUserInGroup(db, userId, groupId)
        if userDb is None:
            raise HTTPException(status_code=400, detail="Error: User is not in the group")
        return userDb

    def userInGroup(db: Session, userId: int, groupId: int):
        userDb = crud.getUserInGroup(db, userId, groupId)
        if userDb is not None:
            raise HTTPException(status_code=400, detail="Error: User already in the group")
        return userDb

    @staticmethod
    def getUser(db: Session, name: str):
        userDb = crud.getUserByName(db, name)
        Checker.userNotExists(db, userDb)
        return userDb

    @staticmethod
    def getSimpleUser(db: Session, name: str):
        userId = crud.getSimpleUserByName(db, name)
        Checker.userNotExists(db, userId)
        return userId

    @staticmethod
    def getGroup(db: Session, name: str):
        groupDb = crud.getGroupByName(db, name)
        Checker.groupNotExists(db, groupDb)
        return groupDb

    @staticmethod
    def userExists(db: Session, name: str) -> int:
        userId = crud.getSimpleUserByName(db, name)
        logger.logger.debug(userId)
        if userId is not None:
            raise HTTPException(status_code=400, detail="Error: User exists")
        return userId[0]

    @staticmethod
    def userNotExists(db: Session, name: str) -> int:
        userId = crud.getSimpleUserByName(db, name)
        if userId is None:
            raise HTTPException(status_code=400, detail="Error: User does not exist")
        return userId[0]

    @staticmethod
    def groupExists(db: Session, name: str) -> int:
        groupId = crud.getSimpleGroupByName(db, name)
        if groupId is not None:
            raise HTTPException(status_code=400, detail="Error: Group already exists")
        return groupId[0]

    @staticmethod
    def groupNotExists(db: Session, name: str) -> int:
        groupId = crud.getSimpleGroupByName(db, name)
        if groupId is None:
            raise HTTPException(status_code=400, detail="Error: Group does not exist")
        return groupId[0]

    @staticmethod
    def isAdmin(user_id: str, group_admin_id: str) -> bool:
        return user_id == group_admin_id

    @staticmethod
    def getUserList(db: Session, users: List[str]) -> Tuple[int,None]:
        userIds = crud.getUserList(db, users)
        if userIds is None:
            raise HTTPException(status_code=400, detail="Error: there are not users")
        if len(userIds) != len(users):
            raise HTTPException(status_code=400, detail="Error: one user or more, not found")
        return userIds

    @staticmethod
    def deleteUserFromGroup(db: Session, username: str, groupname: str) -> bool:
        userId = Checker.userNotExists(db, username)
        groupId = Checker.groupNotExists(db, groupname)

        Checker.userNotInGroup(db, userId, groupId)
        if Checker.isAdmin(userId, groupId):
            raise HTTPException(status_code=400, detail="Cannot delete a admin")

        return crud.deleteUserFromGroup(db, userId, groupId)

    @staticmethod
    def addUserToGroup(db: Session, username: str, groupname: str, paymentReference: str):
        userId = Checker.userNotExists(db, username)
        groupId = Checker.groupNotExists(db, groupname)

        #Checker.checkPaymentReference(paymentReference)

        Checker.userInGroup(db, userId, groupId)
        crud.addUserToGroup(db, userId, groupId)
        crud.createUserMoveRecord(db, userId, groupId, params.ENTRY)

    @staticmethod
    def setUserState(db: Session, username: str, groupname: str, state: bool):
        logger.logger.debug("CHECKER")
        userId = Checker.userNotExists(db, username)
        groupId = Checker.groupNotExists(db, groupname)

        logger.logger.debug("1")
        userGroup = Checker.userNotInGroup(db, userId, groupId)
        logger.logger.debug("2")
        if userGroup.state == state:
            raise HTTPException(status_code=400, detail="Error: user has the same state")

        logger.logger.debug("3")
        crud.setUserState(db, userId, groupId, state)

        logger.logger.debug("4")
        if state == params.STATE_ACTIVATE:
            crud.createUserMoveRecord(db, userId, groupId, params.ACTIVATE)
        crud.createUserMoveRecord(db, userId, groupId, params.DEACTIVATE)

    @staticmethod
    def createUser(db: Session, user: models.User) -> models.User.id:
        return crud.createUser(db, user)

    @staticmethod
    def createGroup(db: Session, group: models.Group, userList: List[str]):
        groupDb = crud.createGroup(db, group)

        if groupDb is None:
            raise HTTPException(status_code=400, detail="Error: Group creation failed")

        return crud.addUserListToGroup(db, groupDb, userList)