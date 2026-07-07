from sqlalchemy.orm import Session
import schemas,models

def get_posts(db:Session,skip:int =0,limit:int=10):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db:Session,post_id:int):
    return db.query(models.Post).filter(models.Post.id ==post_id).first()


def create_post(db:Session,post:schemas.PostCreate):

    new_post = models.Post(title = post.title,content = post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def delete_post(db:Session,post_id:int):
    db_post = get_post(db,post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post

def create_comment(db:Session,comment:schemas.CommentCreate,post_id:int):
    new_comment = models.Comment(**comment.model_dump(),post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
