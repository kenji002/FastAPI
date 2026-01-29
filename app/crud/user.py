from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

# --------------------------
# Create
# --------------------------
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    ユーザーを作成する
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --------------------------
# Read
# --------------------------
def get_user(db: Session, user_id: int) -> models.User:
    """
    ユーザーを取得する
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> models.User:
    """
    ユーザー名でユーザーを取得する
    """
    return db.query(models.User).filter(models.User.username == username).first()

# --------------------------
# Update
# --------------------------
def update_user(db: Session, user_id: int, user: schemas.UserCreate) -> models.User:
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
def delete_user(db: Session, user_id: int) -> models.User:
    """
    ユーザーを削除する
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user