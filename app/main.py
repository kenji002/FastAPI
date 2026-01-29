from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.database import get_db
from app.auth import (create_access_token,verify_password,SECRET_KEY,ALGORITHM)
from app.crud import crud_user

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# --------------------
# LOGIN
# --------------------
@app.post("/login", response_model=schemas.TokenSchema)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(db, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# --------------------
# AUTH DEPENDENCY
# --------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)

        user = (
            db.query(models.User)
            .filter(models.User.id == int(user_id))  # ← int化
            .first()
        )
        if not user:
            raise HTTPException(status_code=401)

        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

# --------------------
# PROTECTED TEST
# --------------------
@app.get("/protected")
def protected(user: models.User = Depends(get_current_user)):
    return {"message": f"Hello {user.username}"}

# --------------------
# ITEM CRUD
# --------------------
@app.post("/create_item", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate,db: Session = Depends(get_db),user: models.User = Depends(get_current_user),):
    return crud.create_item(db, item)

@app.get("/read_all", response_model=list[schemas.Item])
def read_all_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/read_item/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return crud.get_item_or_404(db, item_id)

@app.put("/update_item/{item_id}", response_model=schemas.Item)
def update_item(item_id: int,item: schemas.ItemCreate,db: Session = Depends(get_db),user: models.User = Depends(get_current_user),):
    db_item = crud.get_item_or_404(db, item_id)
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/delete_item/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int,db: Session = Depends(get_db),user: models.User = Depends(get_current_user),):
    db_item = crud.get_item_or_404(db, item_id)
    db.delete(db_item)
    db.commit()
    return db_item
