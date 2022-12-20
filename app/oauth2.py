from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel
from fastapi import status, HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY=settings.secret_key
ALGORITM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes

class TokenData(BaseModel):
    id:Optional[str] = None


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITM)
    return encoded_jwt

def verify_access_token(token:str, credential_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
        id:str=payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data=TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme), db:Session= Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credential_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user
