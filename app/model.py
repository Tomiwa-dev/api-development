from .database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
# creates a table if it doesnt exist in postgres


class Posts(Base):
    __tablename__ = 'Post'
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    publish = Column(Boolean, nullable=False, server_default='False')
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('User')

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'), primary_key= True, nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id', ondelete='CASCADE'), primary_key= True, nullable=False)
