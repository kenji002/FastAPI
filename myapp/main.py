from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from myapp.database import get_db
from myapp.crud import item as crud_item
from myapp.crud import user as crud_user
from myapp.models.user import User as ModelsUser
from myapp.schemas.user import User,UserLogin, UserCreate, TokenSchema
from myapp.schemas.item import Item,ItemCreate
from myapp.service.auth_service import login_user
from myapp.auth.dependencies import get_current_user

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/signup", response_model=User)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
    ):
    """
    ユーザー登録
    """
    return crud_user.create_user(db, user)

# --------------------
# LOGIN
# --------------------
@app.post("/login", response_model=TokenSchema)
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
    ):
    """
    認証 + JWT発行
    """
    token = login_user(db, data.username, data.password)
    return {"access_token": token, "token_type": "bearer"}

# --------------------
# PROTECTED TEST
# --------------------
@app.get("/protected")
def protected(
    user: ModelsUser = Depends(get_current_user)
    ):
    """
    認証済みユーザーのみアクセス可能
    """
    return {"message": f"Hello {user.username}"}

# --------------------
# ITEM CRUD
# --------------------
@app.post("/items", response_model=Item)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    ):
    """
    ユーザーのアイテムを作成する
    """
    return crud_item.create_item(db, item, user)

@app.get("/items", response_model=list[Item])
def read_my_items( 
    db: Session = Depends(get_db),
    user: ModelsUser = Depends(get_current_user),
    ):
    """
    ユーザーのアイテムを取得する
    """
    return crud_item.get_item_by_user(db, user)

@app.put("/items/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item: ItemCreate,
    db: Session = Depends(get_db),
    user: ModelsUser = Depends(get_current_user),
    ):
    """
    ユーザーのアイテムを更新する
    """
    return crud_item.update_item(db, item_id, item, user)

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: ModelsUser = Depends(get_current_user)
    ):
    """
    ユーザーのアイテムを削除する
    """
    return crud_item.delete_item(db, item_id, user)
