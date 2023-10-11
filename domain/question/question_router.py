from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_crud, question_schema


router = APIRouter(prefix="/api/question")


# 질문 목록 조회
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.question_list(db)
    return _question_list


# 질문 상세 조회
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.question_detail(db=db, question_id=question_id)
    return question