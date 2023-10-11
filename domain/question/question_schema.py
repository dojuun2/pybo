from pydantic import BaseModel, validator
import datetime

from domain.answer.answer_schema import Answer


# 출력 스키마
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []  # 답변 조회에 사용될 속성


# 질문 등록 입력 스키마
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v