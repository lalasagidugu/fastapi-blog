from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
 
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
    
    return blog.create(request, db, user.id)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show_blog(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    return blog.show(id, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_blog(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)