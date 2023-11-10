from datetime import datetime
from pydantic import BaseModel, validator

from domain.user.user_schema import User


# 댓글 등록 스키마
class CommentCreate(BaseModel):
    board_id: int
    content: str
    
    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


# 댓글 상세조회
class Comment(BaseModel):
    id: int
    content: str
    user: User
    create_date: datetime
    modify_date: datetime | None = None
    board_id: int
    voter: list[User] = []
   

# 댓글 수정
class CommentUpdate(BaseModel):
    id: int
    content: str