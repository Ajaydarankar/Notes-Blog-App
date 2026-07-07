from fastapi import  FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
import schemas,models,crud
from database import engine,get_db

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title= "Blog API")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )



@app.post("/posts",response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db)):
    return crud.create_post(db,post)

@app.post("/posts/{post_id}/comments",response_model=schemas.Comment)
def create_post(comment:schemas.CommentCreate,post_id:int,db:Session=Depends(get_db)):
    return crud.create_comment(db,comment,post_id)

@app.get("/posts",response_model=list[schemas.Post])
def get_all_posts(db:Session = Depends(get_db),skip:int=0,limit:int=10):
    return crud.get_posts(db,skip,limit)

@app.get("/posts/{post_id}",response_model = schemas.Post)
def get_post(post_id:int,db:Session=Depends(get_db)):
    db_post =  crud.get_post(db,post_id)
    if not db_post:
        raise HTTPException(status_code=404,detail="Post not Found")
    return db_post

@app.delete("/posts/{postId",response_model=schemas.Post)
def delete_post(post_id:int,db:Session=Depends(get_db)):
    db_post =  crud.delete_post(db,post_id)
    if not db_post:
        raise HTTPException(status_code=404,detail="Post not Found")
    return db_post