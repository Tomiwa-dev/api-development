from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import model, schema, oauth
from typing import List, Optional

router = APIRouter(tags=['VOTE'])


@router.post('/votes', status_code=status.HTTP_201_CREATED)
def votes(vote: schema.Votes, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post = db.query(model.Posts).filter(model.Posts.id == vote.post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{vote.post_id} was not found')

    vote_query = db.query(model.Votes).filter(model.Votes.post_id == vote.post_id, model.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on the post"
                                                                             f"{vote.post_id}")
        new_vote = model.Votes(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return "Successfully Added Votes"
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return "Successfully Added Votes"


