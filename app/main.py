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

@app.get("/testing")
def test_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
    #
    #How to use SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()
    #
    #How to use ORM
    posts = db.query(models.Post).all()
    return{"data":posts}

 
@app.post("/posts",status_code=status.HTTP_201_CREATED )
def create_posts( post:Post, db:Session = Depends(get_db)):
    ###############################################
    #How to use SQL
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s , %s , %s)RETURNING* """ ,
                #    (post.title, post.content, post.published))
    # new_post =cursor.fetchone()
    # conn.commit()
    #################################################
    #How to use ORM
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    #
    #How to use SQL
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    #post=cursor.fetchone()
    #
    #How to use ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")   
    print(post)
    return{"post_detail":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    #
    #Using SQL
    #cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING * """,(str(id),))
    #deleted_post=cursor.fetchone()
   # conn.commit()
   
   #
   #Using ORM  
   post = db.query(models.Post).filter(models.Post.id == id)
   if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
         
   post.delete(synchronize_session = False) 
   db.commit()  
   return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,updated_post:Post,db:Session = Depends(get_db)):
    #
    #How to do it using SQL
    #cursor.execute(""" UPDATE posts SET title =%s, content= %s, published= %s WHERE id=%s RETURNING*""",
    #              (post.title, post.content, post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    
    #
    #how to do it using ORM
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return{"data": post_query.first()}    