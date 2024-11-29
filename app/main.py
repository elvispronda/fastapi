#HERE WE USE FASTAPI WITH SQLALCHEMY :USING ORM

from fastapi import FastAPI

from . import models 
from .database import engine
from .routers import post, user, auth
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_password : str = "localhost"
    database_username : str = "postgress"
    secret_key : str = "234gdkgjhhfvn2345fc09"

#models.Base.metadata.create_all(bind = engine)

app = FastAPI()        

    
  
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

           
# @app.get("/")
# def root():
    # return {"Hello": "world!"}
# 
# 

































































































