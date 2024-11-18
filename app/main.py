#HERE WE USE FASTAPI WITH SQLALCHEMY :USING ORM
from typing import Optional, List
from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from  psycopg2.extras  import RealDictCursor
import time
from . import models ,schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user
models.Base.metadata.create_all(bind = engine)

app = FastAPI()        

    
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
    
   
app.include_router(post.router)
app.include_router(user.router)

           
@app.get("/")
def root():
    return {"Hello": "world!"}



































































































