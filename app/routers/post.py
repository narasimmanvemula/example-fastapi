

from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import  List,Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# Get all posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user),
            limit: int =10, skip : int = 0, search : Optional[str]=""):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all
    
    # Get all posts (returns posts with vote counts)
    # print(search)
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(
    #         models.Post.title.contains(search)
    #     ).group_by(models.Post.id).limit(limit).offset(skip).all()/
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Map SQLAlchemy tuples (Post, votes) -> dict matching PostOut schema
    return [{"post": post, "votes": votes} for post, votes in results]

# Create post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES( %s, %s,%s) RETURNING
    # * """,
    #             (post.title, post.content, post.published ))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post=models.Post(
        **post.dict(),
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    
# Get post by ID
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT *FROM posts WHERE id = %s""",(id))
    # post=cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post, votes = result
    return {"post": post, "votes": votes}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    #find the index  in the array  that has  requried id
    #  my_data .pop(index)
    # cursor.execute(""" DELETE  FROM posts WHERE id =%s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first()  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exits')
    post.delete(synchronize_session=False)
    db.commit()
    return{
        "message": 'post was succesfull deleted'
    }

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title,post.content,post.published,id))
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()