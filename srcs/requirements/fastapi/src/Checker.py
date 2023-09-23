from typing import List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session
from dataclasses import dataclass
from . import crud, models
from .Logger import logger

@dataclass
class Checker:

    @staticmethod
    def checkTax(db: Session, tax: int, groupTax: int):
        if tax != groupTax:
            raise HTTPException(status_code=400, detail="Error: Bad tax request")

    @staticmethod
    def userInGroup(db: Session, userId: int, groupId: int):
        userDb = crud.getUserInGroup(db, userId, groupId)
        logger.logger.debug(userDb)
        if userDb:
            raise HTTPException(status_code=400, detail="Error: User is already in the group")

    def userNotInGroup(db: Session, userId: int, groupId: int):
        userDb = crud.getUserInGroup(db, userId, groupId)
        logger.logger.debug(userDb)
        if userDb is None:
            raise HTTPException(status_code=400, detail="Error: User is not in the group")

    @staticmethod
    def checkUserList(userList: models.User, list: List):
        if userList is None:
            raise HTTPException(status_code=400, detail="Error: Empty user list")
        if len(userList) != len(list):
            raise HTTPException(status_code=400, detail="Error: one user or more, not found")

    @staticmethod
    def checkUser(user: models.User):
        if user is None:
            raise HTTPException(status_code=400, detail="Error: User doesn't exist")

    @staticmethod
    def checkGroup(group: models.User):
        if group is None:
            raise HTTPException(status_code=400, detail="Error: Group already exists")

    @staticmethod
    def isAdmin(user_id: str, group_admin_id: str) -> bool:
        return user_id == group_admin_id

    @staticmethod
    def existsGroup(db: Session, name: str) -> models.Group:
        groupDB = crud.getGroupByName(db, name)
        return groupDB

    @staticmethod
    def existsUser(db: Session, name: str) -> models.User:
        userDB = crud.getUserByName(db, name)
        return userDB

    @staticmethod
    def existsUserList(db: Session, users: List[str]) -> Tuple[int,None]:
        userIds = crud.getUserList(db, users)
        return userIds

    @staticmethod
    def deleteUserFromGroup(db: Session, username: str, groupname: str) -> bool:
        userDb = Checker.existsUser(db, username)
        Checker.checkUser(userDb)

        groupDb = Checker.existsGroup(db, groupname)
        Checker.checkGroup(groupDb)

        Checker.userNotInGroup(db, userDb.id, groupDb.id)
        if Checker.isAdmin(userDb.id, groupDb):
            raise HTTPException(status_code=400, detail="Cannot delete a admin")

        return crud.deleteUserFromGroup(db, userDb.id, groupDb.id)

    @staticmethod
    def addUserToGroup(db: Session, username: str, groupname: str, tax: int):
        userDb = Checker.existsUser(db, username)
        Checker.checkUser(userDb)

        groupDb = Checker.existsGroup(db, groupname)
        Checker.checkGroup(groupDb)
        #Checker.checkTax(tax, groupDb.tax)

        Checker.userNotInGroup(db, userDb.id, groupDb.id)
        crud.connecUserWithGroup(db, groupDb.id, userDb.id)
        db.commit()

    @staticmethod
    def setUserState(db: Session, username: str, groupname: str, state: bool):
        userDb = Checker.existsUser(db, username)
        Checker.checkUser(userDb)

        groupDb = Checker.existsGroup(db, groupname)
        Checker.checkGroup(groupDb)

        Checker.userNotInGroup(db, userDb.id, groupDb.id)
        crud.setUserState(db, userDb.id, groupDb.id, state)