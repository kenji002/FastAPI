from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from myapp.models.user import User
from myapp.database import get_db
from myapp.auth.jwt import SECRET_KEY, ALGORITHM

# --------------------------
# パスワードハッシュ設定（argon2）
# --------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --------------------------
# パスワードハッシュ化
# --------------------------
def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化する
    """
    return pwd_context.hash(password)

# --------------------------
# パスワード検証
# --------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    パスワードを検証する
    """
    return pwd_context.verify(plain_password, hashed_password)

# --------------------------
# 認証
# --------------------------
def authenticate_user(username: str, password: str, user: dict)->str:
    """
    ユーザーを認証する
    """
    if username != user["username"]:
        raise HTTPException(status_code=401, detail="Incorrect username")

    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user["username"]

# --------------------
# 
# --------------------
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db),)->User:
    """
    トークンを検証してユーザーを取得する
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)

        user = (
            db.query(User)
            .filter(User.id == int(user_id))  # ← int化
            .first()
        )
        if not user:
            raise HTTPException(status_code=401)

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
