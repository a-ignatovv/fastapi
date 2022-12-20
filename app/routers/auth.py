from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import BaseModel,EmailStr
from passlib.context import CryptContext
from typing import Optional


pwd_context=CryptContext(schemes=['bcrypt'], deprecated="auto")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

router=APIRouter(tags=["Authentication"])

@router.post('/login',response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    #will return username and password in user_credentials
    user= db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Wrong credentials ")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
    #create token
    #return token
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}