from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BlogPostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=2, max_length=60)
    tags: list[str] = Field(default_factory=list)
    published: bool = False


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    content: str | None = Field(default=None, min_length=10)
    author: str | None = Field(default=None, min_length=2, max_length=60)
    tags: list[str] | None = None
    published: bool | None = None


class BlogPostRead(BlogPostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
