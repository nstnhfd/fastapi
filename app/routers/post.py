from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
#from . import auth2
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)

#@router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user : int=Depends(oauth2.get_current_user),Limit : int =10,skip :int =0,search: Optional[str]=""):
        #posts=db.query(models.Post)
        posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
            models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
        #left outer join vote and post
        #posts= db.query(models.Post).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
        return  posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db : Session= Depends(get_db),
                 current_user : int=Depends(oauth2.get_current_user)):
#get_current_user force user to be loged in before create a post    
    
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#same of RETURNING in last code
    #get returned to the user
    return new_post
    
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id= %s """,str(id))#convert id to str because of %s
    #test_post=cursor.fetchone()
    #post=db.query(models.Post).filter(models.Post.id ==current_user.id).first()

    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
            models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(
                models.Post.id).filter(models.Post.id == id).first()

   
    #post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Not authorized to perform requested action")    
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message": "post with id : {id} was not found"}
    return post

#@router.get("/posts/latest")
#def get_latest_post():
   # post=my_posts[len(my_posts)-1]
    
    #return post

@router.delete("/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user)):
    
    post_query=db.query(models.Post).filter(models.Post.id == id)

    post= post_query.first()   
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int,updated_post:schemas.PostCreate,db : Session=Depends(get_db),
                current_user: id = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Not authorized to perform requested action")    

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()