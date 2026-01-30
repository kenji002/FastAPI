from sqlalchemy.orm import Session

from myapp.auth.dependencies import get_password_hash
from myapp.schemas.user import UserCreate
from myapp.models.user import User

# --------------------------
# Create
# --------------------------
def create_user(
    db: Session, 
    user: UserCreate
    ) -> User:
    """
    ユーザーを作成する
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------------------------
# Read
# --------------------------
def get_user(
    db: Session,
    user_id: int
    ) -> User:
    """
    ユーザーを取得する
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(
    db: Session, 
    username: str
    ) -> User:
    """
    ユーザー名でユーザーを取得する
    """
    return db.query(User).filter(User.username == username).first()

# --------------------------
# Update
# --------------------------
def update_user(
    db: Session, 
    user_id: int, 
    user: UserCreate
    ) -> User:
    """
    ユーザーを更新する
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db_user.username = user.username
    db_user.hashed_password = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------------------------
# Delete
# --------------------------
def delete_user(
    db: Session, 
    user_id: int
    ) -> User:
    """
    ユーザーを削除する
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user