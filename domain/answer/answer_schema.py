import datetime
from pydantic import BaseModel, validator

from domain.user.user_schema import User


# 답변 등록 입력 스키마
class AnswerCreate(BaseModel):
    question_id: int
    content: str
    
    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


# 답변 조회 출력 스키마
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None   # 답변 작성자
    modify_date: datetime.datetime | None = None
    question_id: int    # 답변 수정 후, 질문으로 돌아가기 위한 question_id
    voter: list[User] = []


# 답변 수정 입력 스키마
class AnswerUpdate(BaseModel):
    id: int
    content: str