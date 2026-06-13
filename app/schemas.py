from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# Pydantic Model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
        
    title: str
    content: str
    published: bool = True

class UserOut(BaseModel):
    id:int
    email:EmailStr

    
    class Config:
        from_attributes = True 
    

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id:int
    owner:UserOut

    class Config:
        from_attributes = True  

class Postout(PostBase):
    Post: Post
    votes: int

    class Config:
        from_attributes = True 


class PostOut(BaseModel):
    post: Post
    votes: int

class UserCreate(BaseModel):
    email:EmailStr  
    password:str  

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str   

class TokenData(BaseModel):
    id: Optional[int] = None    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)