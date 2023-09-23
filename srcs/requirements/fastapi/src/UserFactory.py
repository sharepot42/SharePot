from sqlalchemy.orm import Session
from dataclasses import dataclass
from fastapi import HTTPException

from . import schemas, crud, auth
from .Checker import Checker

@dataclass
class UserFactory:

    async def create_user(self, db: Session, user: schemas.UserCreate):

        _ = Checker.existsUser(db, user.username)
        hashedPassword = auth.getPasswordHash(user.password)
        user.setPassword(hashedPassword)
        return crud.createUser(db, user)
