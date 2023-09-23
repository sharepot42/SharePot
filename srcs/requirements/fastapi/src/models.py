from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    adminOf = relationship('Group', back_populates='administrator')
    groups = relationship('Group', secondary='user_group', back_populates='users')

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    tax = Column(Integer)
    pot = Column(Integer)
    admin_user_id = Column(Integer, ForeignKey('users.id'))

    administrator = relationship('User', back_populates='adminOf')
    users = relationship('User', secondary='user_group', back_populates='groups')

class UserGroup(Base):
    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    state = Column(Boolean)