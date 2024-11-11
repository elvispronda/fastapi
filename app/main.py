#HERE WE USE FASTAPI WITH SQLALCHEMY :USING ORM
from typing import Optional
from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from  psycopg2.extras  import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind = engine)

app = FastAPI()        
        
class Post(BaseModel):
    title :str
    content: str 
    published: bool = True
    #rating :Optional[int ] = None
    
while True:    
    try:
        conn =psycopg2.connect(host='localhost',database='fastapi',user='postgres',
                            password='elvispro1993',cursor_factory=RealDictCursor)
        cursor =conn.cursor()
        print("database connection was successfully")
        break
    except Exception as error:
        print("Connection to the database failed")
        print("Error :",error)
        time.sleep(3)
    
   
           
@app.get("/")
def root():
    return {"Hello": "world this is my first fastapi project !"}

@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    return {"status ": " success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts=cursor.fetchall()
    return{"data":posts}

 
@app.post("/posts",status_code=status.HTTP_201_CREATED )
def create_posts( post:Post):
    cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s , %s , %s)RETURNING* """ ,
                   (post.title, post.content, post.published))
    new_post =cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int ):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post=cursor.fetchone()
    #print(post)
    #post =find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    print(post)
    return{"post_detail":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING * """,(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()  
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
       
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute(""" UPDATE posts SET title =%s, content= %s, published= %s WHERE id=%s RETURNING*""",
                   (post.title, post.content, post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    return{"data": updated_post}    