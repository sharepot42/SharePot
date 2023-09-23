from sqlalchemy.orm import Session

from fastapi import  HTTPException
from dataclasses import dataclass
from . import crud, schemas
from .Logger import logger
from .Checker import Checker

@dataclass
class GroupFactory:


    def createGroup(self, db: Session, group: schemas.GroupCreate):
        groupDb = Checker.existsGroup(db, group.name)
        Checker.checkGroup(groupDb)

        userDb = Checker.existsUser(db, group.admin)
        Checker.checkUser(userDb)

        userIds = Checker.existsUserList(db, group.user_list)
        Checker.checkUserList(userIds)

        groupDb = crud.createGroup(db, group, userDb.id)
        if groupDb is None:
            raise HTTPException(status_code=400, detail="Error: Group creation failed")

        logger.logger.debug(userIds)
        crud.connecUserListWithGroup(db, groupDb.id, userIds)