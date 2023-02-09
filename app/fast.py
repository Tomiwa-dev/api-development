from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg
import time


while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi database', user='postgres', password='tomrules', row_factory=psycopg.rows.dict_row )
        cur = conn.cursor()
        print('Connection successful')
        break
    except Exception as error:
        print('unable to connect to database')
        print(f'the error was {error}')
        time.sleep(10)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    publish: bool = False


my_posts = [{'title' : 'Title of post 1','Content':'content of post 1', 'id':1},
            {'title' : 'Title of post 2','Content':'content of post 2', 'id':2}]


def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None


#path operation
@app.get("/") #decorator
async def root():
    return {"message": "Hello World"}


@app.get('/posts')
def all_get_post():
    cur.execute("""SELECT * FROM social;""")
    posts = cur.fetchall()
    return posts


@app.post('/posts', status_code= status.HTTP_201_CREATED)
def create(post: Post):
    cur.execute("""INSERT INTO social (title, content, publish) VALUES(%s,%s,%s) RETURNING *;""",(post.title, post.content, post.publish))
    new_post = cur.fetchone()
    conn.commit()
    return new_post


@app.get("/posts/{id}")
def get_post(id: int): #response: Response):
    #post = find_posts(int(id))
    id = str(id)
    cur.execute("""SELECT * FROM social WHERE id = %s; """, [id])
    post = cur.fetchone()
    #print(new_post)
    if post is None:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f'{id} was not found'}
    #BETTER METHOD IS TO USE HTTPEXCEPTION
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'{id} was not found')

    return {'Post': f' {post}'}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    id = str(id)
    cur.execute("""DELETE FROM social WHERE id = %s RETURNING *""", [id])
    deleted_post = cur.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'{id} was not found')

    return deleted_post, Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id : int, post: Post):
    id = str(id)
    cur.execute("""UPDATE social SET title = %s, content = %s WHERE id = %s RETURNING * """, (post.title,post.content,id))
    updated_post = cur.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} was not found')

    #cur.execute("""UPDATE social SET %s = %s""")
    return {"message" : f"{updated_post} updated"}



