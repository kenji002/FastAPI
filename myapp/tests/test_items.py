
from fastapi import status
# --------------------------
# Item作成テスト
# --------------------------
def test_client_create_item(client, auth_headers_A):
    response = client.post("/items",
    headers=auth_headers_A,
    json={
        "name": "test item",
        "description": "test description"
    }
    )
    assert response.status_code == 200  

# --------------------------
# Item所有者テスト
# --------------------------
def test_item_owner(
    client, 
    auth_headers_A,
    auth_headers_B
    ):
    response = client.post(
        "/items",
        json={"name": "secret", "description": "xxx"},
        headers=auth_headers_A
    )
    item_id = response.json()["id"]
    # 他人は見えない
    response = client.get(f'/item/{item_id}', headers=auth_headers_B)
    assert response.status_code == 404