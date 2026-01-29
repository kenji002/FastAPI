from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import secrets


# JWT設定
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --------------------------
# パスワードハッシュ設定（argon2）
# --------------------------
pwd_context = CryptContext(
    schemes=["argon2"],  # bcrypt から変更
    deprecated="auto"
)

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
# JWT作成
# --------------------------
def create_access_token(data: dict)->str:
    """
    JWTを作成する
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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

