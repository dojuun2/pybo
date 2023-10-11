from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from models import Answer

router = APIRouter(prefix="/api/answer")


# 답변 등록 api
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    answer_create: answer_schema.AnswerCreate,
    question_id: int,
    db: Session = Depends(get_db),
):
    # 답변에 대한 질문 가져오기
    question = question_crud.question_detail(db, question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # 답변 등록
    answer_crud.answer_create(db, answer_create, question)


# # 답변 목록 조회 api
# @router.get("/list/{question_id}", response_model=list[answer_schema.Answer])
# def answer_list(question_id: int, db: Session = Depends(get_db)):
#     # 질문 가져오기
#     question = question_crud.question_detail(db, question_id)

#     if not question:
#         raise HTTPException(status_code=404, detail="존재하지 않는 질문입니다.")
    
#     # 질문에 대한 답변 가져오기
#     answer = answer_crud.answer_list(db, question)
#     return answer
