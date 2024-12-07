from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional, Union


   
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    

class PostCreate(PostBase):
    pass



class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
    
class Userout(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class config :
        orm_mode = True
       
       
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str
    

class TokenData(BaseModel):
    id: Union[str, int]  # Accepts both string and integer types



class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : Userout
    
    class config :
        orm_mode = True


class Vote(BaseModel):
    id : int
    dir : conint(le=1) # type: ignore