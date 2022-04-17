from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import model, schema, oauth
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(tags=['Posts'])  # APIRouter(tags = ['Posts']) tags to group apis in doccumentations

# apis for interacting with the post table in postgres


@router.get('/sqlalchemy', response_model=List[schema.VoteResponse])  # list because the function returnss a list of posts
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # limit to set the number of posts to be returned
    # skip to skip some post
    # search to search for specific post containing a given key word
    # they are called query parameters to use them start with ? followed by the query parameter(limit, search,skip)
    # to use more than on at  tie use &

    post = db.query(model.Posts, func.count(model.Votes.post_id).label("votes")).join(
        model.Votes, model.Votes.post_id == model.Posts.id, isouter=True).group_by(model.Posts.id).filter(
        model.Posts.title.contains(search)).limit(limit).offset(skip).all()
    # to get posts and total number of posts
    return post


@router.post('/sqlalchemy', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # new_post = model.Posts(title=post.title, content=post.content, publish=post.publish)
    # better method is to convert the dictionary and unpacking the dictionary i.e **post.dict()
    new_post = model.Posts(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/sqlalchemy/{id}', response_model=schema.VoteResponse)
def get_specific_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    # post = db.query(model.Posts).filter(model.Posts.id == id).first()
    post = db.query(model.Posts, func.count(model.Votes.post_id).label("votes")).join(
        model.Votes, model.Votes.post_id == model.Posts.id, isouter=True).group_by(model.Posts.id).filter(
        model.Posts.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f'{id} was not found')
    return post


@router.delete('/sqlalchemy/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    post_query = db.query(model.Posts).filter(model.Posts.id == id)  # returns sql query

    post = post_query.first()  # returns result of sql query
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'NOT ALLOWED!!!!!!')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/sqlalchemy/{id}', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    post_query = db.query(model.Posts).filter(model.Posts.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} was not found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'NOT ALLOWED!!!!!!')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {'data': post_query.first()}
