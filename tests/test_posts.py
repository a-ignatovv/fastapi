import pytest
from app.oauth2 import create_access_token
from fastapi.testclient import TestClient
from app.main import app
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

class PostReply(BaseModel):
    title:str
    content:str
    published:bool
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode=True


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:ai1234@localhost:5432/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    yield TestClient(app)



@pytest.fixture
def token():
    t=create_access_token({"user_id":"4"})
    print("Access token:", t)
    return t

@pytest.fixture
def authorized_client(client, token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

def test_get_all_posts(client):
    res=client.get("/posts/")
    #print(res.json())
    assert res.status_code==200

def test_get_one_post(authorized_client):
    res=authorized_client.get("/posts/1")
    print(res.json())

@pytest.mark.parametrize("title, content, published", [
    ("new title1", "new content1", True),
    ("new title2", "new content2", True)
])
def test_create_post(authorized_client, title, content, published):
    res=authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})
    print (res.json())
    #created_post=PostReply(**res.json())
    #assert created_post.title==title

