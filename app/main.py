from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models
from .database import engine
from .routers import post,user,outh,vote
from .config import Settings 


#models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origins = ["*"]
#which domain can talk to our api
app.add_middleware(
    CORSMiddleware,
    
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(outh.router)
app.include_router(vote.router)
#request get method url : "/".
@app.get("/")
def root():
    return {"message": "hello world"}


