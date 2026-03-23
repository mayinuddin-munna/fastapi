from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.post import create_post, delete_post, get_post, list_posts, update_post
from app.db.database import get_db
from app.schemas.post import BlogPostCreate, BlogPostRead, BlogPostUpdate

router = APIRouter()


@router.get("", response_model=list[BlogPostRead])
def read_posts(
    published: Optional[bool] = Query(default=None),
    tag: Optional[str] = Query(default=None, min_length=1, max_length=50),
    db: Session = Depends(get_db),
) -> list[BlogPostRead]:
    return list_posts(db=db, published=published, tag=tag)


@router.get("/{post_id}", response_model=BlogPostRead)
def read_post(post_id: int, db: Session = Depends(get_db)) -> BlogPostRead:
    post = get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("", response_model=BlogPostRead, status_code=status.HTTP_201_CREATED)
def create_new_post(payload: BlogPostCreate, db: Session = Depends(get_db)) -> BlogPostRead:
    return create_post(db=db, payload=payload)


@router.put("/{post_id}", response_model=BlogPostRead)
def update_existing_post(
    post_id: int, payload: BlogPostUpdate, db: Session = Depends(get_db)
) -> BlogPostRead:
    post = update_post(db=db, post_id=post_id, payload=payload)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db)) -> dict[str, str | int]:
    deleted = delete_post(db=db, post_id=post_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"message": "Post deleted", "post_id": post_id}
