from sqlalchemy.orm import Session
from dataclasses import dataclass
from fastapi import HTTPException

from . import schemas, models, auth
from .Checker import Checker

@dataclass
class UserFactory:

    async def create_user(self, db: Session, user: schemas.UserCreate) -> models.User:

        Checker.userExists(db, user.username)
        _ = Checker.existsUser(db, user.username)
        hashedPassword = auth.getPasswordHash(user.password)
        user.setPassword(hashedPassword)

        return models.User(
            username=user.username,
            password=hashedPassword,
            email=user.email,
            phone_number=int(user.phone_number),
        )