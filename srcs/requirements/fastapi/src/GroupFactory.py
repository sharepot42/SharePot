from sqlalchemy.orm import Session

from fastapi import  HTTPException
from dataclasses import dataclass
from . import schemas, models
from .Logger import logger
from .Checker import Checker

@dataclass
class GroupFactory:

    @staticmethod
    def createGroup(db: Session, group: schemas.GroupCreate):

        Checker.groupExists(db, group.name)

        userId = Checker.userNotExists(db, group.admin)

        _ = Checker.getUserList(db, group.user_list)

        groupDb = models.Group(
            name=group.name,
            description=group.description,
            admin_user_id=userId,
            tax=group.tax,
            balance=0
            )

        return groupDb

    def createRecord(db: Session, userId: int, groupId: int, date: int, state: int):
        return models.HistoryMoves(
            date =  date,
            user_id = userId,
            group_id = groupId,
            state = state
        )