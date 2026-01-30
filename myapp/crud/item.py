from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from myapp.schemas.item import ItemCreate
from myapp.models.user import User
from myapp.models.item import Item

# --------------------------
# Create
# --------------------------
def create_item(
    db: Session, 
    item: ItemCreate,
    user: User,
    )->Item:
    """
    アイテムを作成する
    """
    db_item = Item(
        name=item.name, 
        description=item.description, 
        owner_id=user.id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --------------------------
# Read
# --------------------------
def get_my_items_by_user(
    db: Session, 
    user: User
    )->list[Item]:
    """
    ログインユーザーのアイテムのみ取得
    """
    return (
        db.query(Item)
        .filter(Item.owner_id == user.id)
        .all()
    )

def get_my_item_by_id(
    db: Session, 
    item_id: int,
    user: User
    )->Item:
    """
    ログインユーザーのアイテムを取得する
    """
    return (
        db.query(Item)
        .filter(
            Item.id == item_id,
            Item.owner_id == user.id
        )
        .first()
    )

# --------------------------
# Update
# --------------------------
def update_item(
    db: Session, 
    item_id: int, 
    item: ItemCreate,
    user: User,
    )->Item:
    """
    アイテムを更新する
    """
    db_item = get_item_or_404(db, item_id, user)
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

# --------------------------
# Delete
# --------------------------
def delete_item(
    db: Session, 
    item_id: int,
    user: User,
    )->Item:
    """
    アイテムを削除する
    """
    db_item = get_item_or_404(db, item_id, user)
    db.delete(db_item)
    db.commit()
    return db_item

# --------------------------
# 例外処理
# --------------------------
def get_item_or_404(
    db:Session, 
    item_id: int, 
    user: User
    )->Item:
    """
    存在しない場合は404を返す
    """
    item = (
        db.query(Item)
        .filter(
            Item.id == item_id,
            Item.owner_id == user.id
        )
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item