from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import model, schema, utils

router = APIRouter(tags=['Users'])  # APIRouter(tags = ['Users']) tags to group apis in documentations

# apis for interacting with the user table in postgres


@router.post('/createuser_sqlalchemy',status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user: schema.User, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/user/{id}', response_model=schema.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} was not found')
    return user