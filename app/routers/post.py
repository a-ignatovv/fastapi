from .. import models, oauth2
from ..database import get_db
from datetime import datetime
from fastapi import FastAPI,status,Response,HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr

router=APIRouter(prefix="/posts", tags=['post'])

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

class PostOut(BaseModel):
    Post: PostReply
    votes: int

    class Config:
        orm_mode=True


class Post(BaseModel):
    title:str
    content:str
    published:bool=True



@router.get("/", response_model=List[PostOut])
def get_posts(db:Session = Depends(get_db), limit:int=2, skip:int=0, search:Optional[str]=''):
   # cursor.execute("select * from posts")
   # posts=cursor.fetchall()
   ##posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostReply)
def create_posts(post: Post, db:Session = Depends(get_db), user:models.User=Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values(%s, %s, %s) returning *""",
    # (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(user.email)
    new_post=models.Post(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=PostOut)
def get_post(id:int, db: Session=Depends(get_db)):
    # cursor.execute("select * from posts where id = %s", (str(id),))
    # post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db), user:models.User=Depends(oauth2.get_current_user)):
    # cursor.execute("delete from posts where id= %s returning *", (str(id),))
    # post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist.")
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete.")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostReply)
def update_post(id:int, updated_post:Post, db:Session = Depends(get_db), user:models.User=Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content=%s, published=%s where id = %s RETURNING *",
    # (post.title, post.content, post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete.")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
