from os import access
from _contextvars import Token
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    name: str
    discription: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)