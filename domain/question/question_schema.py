from pydantic import BaseModel
import datetime

from domain.answer.answer_schema import Answer


# 출력 스키마
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []  # 답변 조회에 사용될 속성