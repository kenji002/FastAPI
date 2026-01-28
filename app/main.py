from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import schemas, crud
from app.schemas import Token, UserLogin
from app.database import get_db
from app.auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    SECRET_KEY,
    ALGORITHM,
)

app = FastAPI(title="FastAPI", version="0.0.1")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 仮ユーザー（bcrypt済み）
fake_user = {
    "id": 1,
    "username": "admin",
    "hashed_password": get_password_hash("password"),
}

@app.post("/login", response_model=Token)
def login(data: UserLogin):
    if data.username != fake_user["username"]:
        raise HTTPException(status_code=401, detail="Incorrect username")

    if not verify_password(data.password, fake_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": fake_user["username"]})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}"}

@app.post("/create_item", response_model=schemas.Item)
def create(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/read_all", response_model=list[schemas.Item])
def read_all(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/read_item/{item_id}", response_model=schemas.Item)
def read(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/update_item/{item_id}", response_model=schemas.Item)
def update(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/delete_item/{item_id}", response_model=schemas.Item)
def delete(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item