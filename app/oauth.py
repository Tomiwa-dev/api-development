from jose import JWTError, jwt # to authnticate users
from datetime import datetime, timedelta
from app import schema,  model
from app.database import get_db

from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# creating jwt tokens so only authorized users can interact with the api


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exceptions

        token_data = schema.TokenData(id=id) # token_data is the user id

    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'could not validate credentials', headers={"WWW-AUTHENTICATE":"BEARER"})

    token = verify_access_token(token, credentials_exceptions)
    
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user