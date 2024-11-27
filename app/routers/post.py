from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from typing import  List
from sqlalchemy.orm import Session
from .. import models ,schemas, utils,oauth2
from ..database import  get_db

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model = List [schemas.Post])
def get_posts(db:Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
    #
    #How to use SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()
    #
    #How to use ORM
    posts = db.query(models.Post).all()
    return posts

 
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post )
def create_posts( post:schemas.PostCreate, db:Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
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
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db:Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
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
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
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

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user)):
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
    return post_query.first()   
