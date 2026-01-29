from pydantic import BaseModel, ConfigDict

class UserLogin(BaseModel):
    """
    ログイン用スキーマ
    """
    username: str
    password: str

class UserBase(BaseModel):
    """
    ユーザー情報用スキーマ
    """
    username: str

class UserCreate(UserBase):
    """
    ユーザー作成用スキーマ
    """
    password: str

class User(BaseModel):
    """
    ユーザー情報用スキーマ
    """
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

class TokenSchema(BaseModel):
    """
    トークン用スキーマ
    """
    access_token: str
    token_type: str = "bearer"