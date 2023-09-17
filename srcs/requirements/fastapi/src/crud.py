from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.logger import logger

def getUser(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def getGroup(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()

#TODO handle if the user already exists
def createUser(
        db: Session,
        user: schemas.UserCreate
        ) -> schemas.User:
    fake_password = user.password
    dbUser = models.User(username=user.username, password=fake_password)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

def createGroupp(db: Session, group: schemas.GroupCreate):
    dbGroup = models.Group(name=group.name, description=group.description)
    db.add(dbGroup)
    db.commit()
    db.refresh(dbGroup)
    return dbGroup