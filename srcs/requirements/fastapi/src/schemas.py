from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str
    description: str

class GroupCreate(GroupBase):
    pass

class Group(UserBase):
    id: int

    class Config:
        from_attributes = True