from .. import models
from ..database import get_db,engine
from datetime import datetime
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from fastapi import status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router=APIRouter(prefix="/users", tags=['user'])
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
    hashed_password=pwd_context.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    return user
