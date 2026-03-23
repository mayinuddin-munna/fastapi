from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import BlogPostCreate, BlogPostUpdate


def list_posts(db: Session, published: bool | None = None, tag: str | None = None) -> list[Post]:
    statement: Select[tuple[Post]] = select(Post).order_by(Post.created_at.desc())

    if published is not None:
        statement = statement.where(Post.published == published)

    if tag:
        statement = statement.where(Post.tags.contains([tag]))

    return list(db.scalars(statement).all())


def get_post(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def create_post(db: Session, payload: BlogPostCreate) -> Post:
    post = Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, payload: BlogPostUpdate) -> Post | None:
    post = db.get(Post, post_id)
    if not post:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int) -> bool:
    post = db.get(Post, post_id)
    if not post:
        return False

    db.delete(post)
    db.commit()
    return True
