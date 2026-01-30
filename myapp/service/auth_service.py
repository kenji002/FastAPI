from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from myapp.auth.jwt import create_access_token
from myapp.models.user import User
from myapp.auth.dependencies import verify_password

# --------------------------
# パスワードハッシュ設定（argon2）
# --------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def authenticate_user(
    db: Session, 
    username: str, 
    password: str
    )->User:
    """
    認証
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return user

def login_user(db: Session, username: str, password: str)->str:
    """
    認証 + JWT発行
    """
    user = authenticate_user(db, username, password)
    return create_access_token({"sub": str(user.id)})

def get_password_hash(password: str)->str:
    """
    パスワードハッシュ化
    """
    return pwd_context.hash(password)