from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import model, schema, utils
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth import create_access_token

router = APIRouter()

# authorizing user e.g login


@router.post('/login', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials')

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials')

    access_token = create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}