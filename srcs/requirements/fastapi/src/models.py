from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    phone_number = Column(BigInteger, unique=True)
    password = Column(String)

    admin_of = relationship('Group', back_populates='administrator')
    groups = relationship('Group', secondary='user_group', back_populates='users')
    payment_history = relationship('HistoryPayments', back_populates='user')
    move_history = relationship('HistoryMoves', back_populates='user')

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    tax = Column(Integer)
    balance = Column(Integer)
    admin_user_id = Column(Integer, ForeignKey('users.id'))

    administrator = relationship('User', back_populates='admin_of')
    users = relationship('User', secondary='user_group', back_populates='groups')
    payment_history = relationship('HistoryPayments', back_populates='group')
    move_history = relationship('HistoryMoves', back_populates='group')

class UserGroup(Base):
    __tablename__ = 'user_group'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    state = Column(Boolean)

class HistoryPayments(Base):
    __tablename__ = 'history_payments'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    user = relationship('User', back_populates='payment_history')
    group = relationship('Group', back_populates='payment_history')

class HistoryMoves(Base):
    __tablename__ = 'history_moves'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    state = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

    user = relationship('User', back_populates='move_history')
    group = relationship('Group', back_populates='move_history')