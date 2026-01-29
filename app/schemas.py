from os import access
from _contextvars import Token
from pydantic import BaseModel, ConfigDict

# --------------------------
# Item Schemas
# --------------------------
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    class Config:
        model_config = ConfigDict(from_attributes=True)

# --------------------------
# Token Schema
# --------------------------
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --------------------------
# User Schemas
# --------------------------
class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)