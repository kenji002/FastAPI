from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import secrets

# JWT設定
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワードハッシュ設定（argon2）
pwd_context = CryptContext(
    schemes=["argon2"],  # bcrypt から変更
    deprecated="auto"
)

# パスワードハッシュ化
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# パスワード検証
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT作成
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
