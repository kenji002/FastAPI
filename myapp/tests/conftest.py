import pytest
from fastapi.testclient import TestClient

from myapp.main import app

# ---------------------
# データベースリセット
# ---------------------
@pytest.fixture(autouse=True)
def reset_db():
    from myapp.database import Base, engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# ---------------------
# テストクライアント
# ---------------------
@pytest.fixture
def client():
    return TestClient(app)

# --------------------------
# テストユーザー(userA,userB)
# --------------------------
@pytest.fixture
def userA():
    return {
        "username": "userA",
        "password": "passwordA"
    }

@pytest.fixture
def userB():
    return {
        "username": "userB",
        "password": "passwordB"
    }

# --------------------------
# サインアップ(1回のみ)
# --------------------------
@pytest.fixture
def create_userA(client, userA):
    client.post("/signup", json=userA)
    return userA

@pytest.fixture
def create_userB(client, userB):
    client.post("/signup", json=userB)
    return userB

# --------------------------
# ログインからトークン取得
# --------------------------
@pytest.fixture
def tokenA(client, create_userA, userA):
    response = client.post("/login", json=userA)
    return response.json()["access_token"]

@pytest.fixture
def tokenB(client, create_userB, userB):
    response = client.post("/login", json=userB)
    return response.json()["access_token"]

# --------------------------
# 認証ヘッダー
# --------------------------
@pytest.fixture
def auth_headers_A(tokenA):
    return {"Authorization": f"Bearer {tokenA}"}

@pytest.fixture
def auth_headers_B(tokenB):
    return {"Authorization": f"Bearer {tokenB}"}
