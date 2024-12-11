from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from typing import Optional,List, Dict 
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models ,schemas,oauth2
from ..database import  get_db

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user : str = Depends(oauth2.get_current_user),
              limit : int = 5, skip : int = 0, search :Optional[str] = ""):
              
    #
    #How to use SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()
    #
    #How to use ORM#
    ## filter all individuals post not for every user
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    ##
    
    ## JOIN TABLES POST AND VOTE TABLES
  
    
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts =db.execute('select posts.* ,COUNT(votes.post_id)as votes from posts LEFT JOIN votes ON posts.id =votes.post_id GROUP BY posts.id')
    # result = []
    
    # for post in posts:
    #     result.append(dict(post))
    #     
        
  
    ##filter all users posts at the same time
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        #models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    #print(results)
    return results

 
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
    new_post = models.Post(owner_id = current_user.id, **post.dict())
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
        
    ##when you want to retrieve posts with its owner   
    ##if post.owner_id != current_user.id :
    ##   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    #print(post)
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
   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()
   
   if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
   ## check if the person to delete the post is the owner     
   #if post.owner_id != current_user.id :
   #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
         
   post_query.delete(synchronize_session = False) 
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
    
    ## if you want to check the person to update has the right of ownership of that post. i mean he created it   
    #if post.owner_id != current_user.id :
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()   
