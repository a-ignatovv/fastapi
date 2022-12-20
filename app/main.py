from typing import Optional, List
from fastapi import FastAPI,status,Response,HTTPException, Depends
#from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from random import randrange
from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .config import settings
from .database import engine, get_db
from datetime import datetime
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"hello world"}
print(settings.database_password)

class Post(BaseModel):
    title:str
    content:str
    published:bool=True

class PostReply(BaseModel):
    title:str
    content:str
    published:bool
    class Config:
        orm_mode=True
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

try:
    conn=psycopg2.connect(host='localhost', database='fastapi',user='postgres',password='ai1234',
    cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("DB connection succesfull")
except Exception as err:
    print("Error", err)


