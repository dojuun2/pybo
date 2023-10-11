import datetime
from pydantic import BaseModel, validator


# 답변 등록 입력 스키마
class AnswerCreate(BaseModel):
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