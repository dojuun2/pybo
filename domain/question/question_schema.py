from pydantic import BaseModel
import datetime


# 출력 스키마
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
