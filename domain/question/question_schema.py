from pydantic import BaseModel, validator
import datetime

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


# 출력 스키마
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []  # 답변 조회에 사용될 속성
    user: User | None   # 질문 작성자
    modify_date: datetime.datetime | None = None
    voter: list[User] = []  # 질문 추천인
    hits: int = 0   # 질문 조회수
    

# 질문 등록 입력 스키마
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


# 질문 목록 스키마
class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


# 질문 수정 입력 스키마
class QuestionUpdate(QuestionCreate):
    id: int


# 질문 상세보기 출력 스키마 (답변 페이징 처리 된 질문)
class QuestionDetail(BaseModel):
    total: int = 0
    question: Question = None


# 질문 추천 스키마
class QuestionRecommendation(BaseModel):
    question_id: int