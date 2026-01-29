from sqlalchemy.orm import Session
from app import models, schemas

# --------------------------
# Create
# --------------------------
def create_item(db: Session, item: schemas.ItemCreate)->models.Item:
    """
    アイテムを作成する
    """
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --------------------------
# Read
# --------------------------
def get_items(db: Session)->list[models.Item]:
    """
    アイテムを取得する
    """
    return db.query(models.Item).all()

def get_item(db: Session, item_id: int)->models.Item:
    """
    アイテムを取得する
    """
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_item_or_404(db:Session, item_id: int)->models.Item:
    """
    存在しない場合は404を返す
    """
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --------------------------
# Update
# --------------------------
def update_item(db: Session, item_id: int, item: schemas.ItemCreate)->models.Item:
    """
    アイテムを更新する
    """
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

# --------------------------
# Delete
# --------------------------
def delete_item(db: Session, item_id: int)->models.Item:
    """
    アイテムを削除する
    """
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item