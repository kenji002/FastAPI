from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    """
    アイテム情報用スキーマ
    """
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    """
    アイテム作成用スキーマ
    """
    pass

class Item(ItemBase):
    """
    アイテム情報用スキーマ
    """
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
