from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    return db.query(models.Blog).all()

def create(request: schemas.Blog, db: Session, user_id: int):
    new_blog = models.Blog(
        title=request.title, 
        body=request.body, 
        user_id=user_id 
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available"
        )
    return blog

def destroy(id: int, db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    
    blog_query.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted successfully"}

def update(id: int, request: schemas.Blog, db: Session):

    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    

    blog_query.update(request.model_dump())
    
    db.commit()
    return {"detail": "Updated successfully"}