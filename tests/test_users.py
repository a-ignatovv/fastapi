from fastapi.testclient import TestClient
from app.main import app
from app.routers.user import UserOut
import pytest


#client=TestClient(app)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# def test_root(client):
#     res=client.get("/")
#     print(res)
#     assert "bind" in res.json().get('message')
#     assert res.status_code==200

# def test_create_user(client):
#     res = client.post("/users", json={"email":"test5@gmail.com", "password":"pass5"})
#     print(res.json())
#     new_user=UserOut(**res.json())
#     assert res.status_code==201

def test_login(client):
    res=client.post("/login", data={"username":"test5@gmail.com", "password":"pass5"})
    print(res.json())

@pytest.mark.parametrize("username, password, status_code", [
    ("wrong@gmail.com","password5", 403),
    ("test5@gmail.com","wrong", 403)
    ])
def test_incorrect_login(client, username, password, status_code):
    res=client.post("/login", data={"username":username, "password":password})
    assert res.status_code==status_code
    