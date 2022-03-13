from fastapi import FastAPI

from app.database import engine
from app import model
from .routers import post, user, auth, votes
from app.config import Settings
from fastapi.middleware.cors import CORSMiddleware

#model.Base.metadata.create_all(bind=engine)   # command to create tables. not needed sine we are using almebic


app = FastAPI()
origins = ["*"]  # domains that can interact with our api "*" all domains

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(votes.router)





