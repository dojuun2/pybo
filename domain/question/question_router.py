from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_crud, question_schema
from starlette import status
from domain.user.user_router import get_current_user

from models import User


router = APIRouter(prefix="/api/question")


# 질문 목록 조회
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, question_list = question_crud.question_list(db, skip=page * size, limit=size)
    return {"total": total, "question_list": question_list}


# 질문 상세 조회
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.question_detail(db=db, question_id=question_id)
    return question


# 질문 등록
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 질문 등록하기
    question_crud.question_create(db, question_create, user=current_user)
