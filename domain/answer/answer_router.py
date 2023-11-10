from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud
from models import Answer, User
from domain.user.user_router import get_current_user

router = APIRouter(prefix="/api/answers")


# 답변 등록 api
@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    answer_create: answer_schema.AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 답변에 대한 질문 가져오기
    question = question_crud.get_question(db=db, question_id=answer_create.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="존재하지 않는 질문입니다.")

    # 답변 등록
    answer_crud.answer_create(db, answer_create, question, user=current_user)


# 답변 한건 조회 api
@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    # 답변 가져오기
    answer = answer_crud.answer_detail(db, answer_id)
    return answer


# 답변 수정 api
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(
    answer_update: answer_schema.AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 수정할 답변 가져오기
    answer = answer_crud.answer_detail(db, answer_update.id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 답변입니다."
        )
    if current_user.id != answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."
        )

    # 답변 수정하기
    answer_crud.answer_update(db, answer, answer_update)


# 답변 삭제 api
@router.delete("/delete/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 삭제할 답변 가져오기
    answer = answer_crud.answer_detail(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 답변입니다."
        )
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )

    answer_crud.answer_delete(db, answer)


# 답변 추천 api
@router.post("/vote/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 추천할 답변 가져오기
    answer = answer_crud.answer_detail(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 답변입니다."
        )

    # 추천 정보 가져오기
    voter_information = answer_crud.get_answer_voter(db, current_user.id, answer_id)
    if voter_information:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="추천 정보가 이미 존재합니다."
        )

    # 답변 추천
    answer_crud.answer_vote(db, answer, current_user)


# 답변 추천취소 api
@router.post("/unvote/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 추천 취소할 답변 가져오기
    answer = answer_crud.answer_detail(db, answer_id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 답변입니다."
        )

    # 추천 정보 가져오기
    voter_information = answer_crud.get_answer_voter(db, current_user.id, answer_id)
    if not voter_information:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="추천 정보가 존재하지 않습니다."
        )

    # 답변 추천 취소
    answer_crud.answer_unvote(db, answer, current_user)


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
