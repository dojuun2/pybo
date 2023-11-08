import datetime
from pydantic import BaseModel, validator

from domain.user.user_schema import User
from domain.comment.comment_schema import Comment



# 출력 스키마
# 게시글
class Board(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    modify_date: datetime.datetime | None = None
    user: User | None  # 게시글 작성자
    voter: list[User] = []  # 게시글 추천인
    hits: int = 0
    comments: list[Comment] = []     # 댓글
    

# 게시글 목록
class BoardList(BaseModel):
    total: int = 0
    board_list: list[Board] = []


# 입력 스키마
# 게시글 등록
class BoardCreate(BaseModel):
    subject: str
    content: str
    
    @validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v