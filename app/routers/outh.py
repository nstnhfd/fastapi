from fastapi import  APIRouter,FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import database,models,utils,schemas,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
#create endpoint in api related to authenticated
router = APIRouter(tags=['Authentication'])
#a request to login in endpoint after log in return json response
@router.post('/login',response_model=schemas.Token)
#function to login user 
#OAuth2PasswordRequestForm include username and password and related to database session in get_db
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),db:Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email== user_credentials.username).first()  
    #if we have no user by that username  
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    #check password by hashed pasword in database 
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    #create token
    #return token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})

    return {"access_token" : access_token,"token_type":"bearer"}
