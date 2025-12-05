
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas
from .deps import get_current_user

router = APIRouter(prefix="/feed", tags=["feed"])

@router.get("/", response_model=list[schemas.FeedPostRead])
def get_feed(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    posts = (
        db.query(models.FeedPost)
        .order_by(models.FeedPost.created_at.desc())
        .all()
    )
    return posts

@router.post("/", response_model=schemas.FeedPostRead)
def create_post(
    payload: schemas.FeedPostCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    post = models.FeedPost(
        user_id=user.id,
        title=payload.title,
        content=payload.content,
        tag=payload.tag,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
