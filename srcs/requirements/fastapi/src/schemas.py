from typing import List
from fastapi import Query
from pydantic import BaseModel

class Card(BaseModel):
    pass

class User(BaseModel):
    username: str = Query(min_length=3,
                      max_length=16,
                      regex="^[a-zA-Z0-9_-]+$",
                      description="Nombre de usuario")

    password: str = Query(min_length=8,
                          max_length=16,
                          regex="^[a-zA-Z0-9_-]+$",
                          description="Contrasena de usuario")

    email: str = Query(regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                       description="Email address")

    def setPassword(self, password):
        self.password = password

class UserCreate(User):
    card_information: Card | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "Crash Bandicoot",
                    "password": "Nefario",
                    "email": "apple@terra.org"
                }
            ]
        }
    }

class AuthUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class Group(BaseModel):
    name: str = Query(min_length=3, max_length=12,regex="^[a-zA-Z0-9_-]+$")
    description: str = Query(max_length=30, regex="^[a-zA-Z0-9 ]+$")
    user_list: List[str] | None = None
    tax: int
    admin: str

class GroupCreate(Group):

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "sudo",
                    "description": "Night Club group",
                    "user_list": ["Jimmy", "William"],
                    "tax": 10
                }
            ]
        }
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str