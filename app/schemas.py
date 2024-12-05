from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime
from typing import Optional
#from pydantic.types import conint
MyModelConfig = ConfigDict(arbitrary_types_allowed=True)

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass
class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    model_config = MyModelConfig
    #class Config:
    #    from_attributes = True
    #model_config = ConfigDict(
    #    from_attributes = True
    #)
class Post(PostBase):
    id : int    
    created_at: datetime
    owner_id: int
    owner : UserOut
    model_config = MyModelConfig
    #class config:
     #   orm_mode = True
    #model_config = ConfigDict(
    #    from_attributes = True              
    #)
    #class Config:
    #    from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    #class config:
    #    orm_mode = True
    #class Config:
     #   from_attributes = True
    #model_config = ConfigDict(
    #    from_attributes = True 
    #)
    model_config = MyModelConfig
class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str   

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional [str] = None

class Vote(BaseModel):
    post_id : int
    dir : int #conint(le=1)