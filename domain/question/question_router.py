from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_crud, question_schema
from starlette import status
from domain.user.user_router import get_current_user

from models import User


router = APIRouter(prefix="/api/question")


# 질문 목록 조회
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(
    db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ""
):
    total, question_list = question_crud.question_list(
        db, skip=page * size, limit=size, keyword=keyword
    )
    return {"total": total, "question_list": question_list}


# 질문 상세 조회
@router.get("/detail/{question_id}", response_model=question_schema.QuestionDetail)
def question_detail(
    response: Response,
    request: Request,
    question_id: int,
    db: Session = Depends(get_db),
    size: int = 10,
    sort_order: str = "date",
):
    total, question = question_crud.question_detail(
        db=db,
        question_id=question_id,
        limit=size,
        sort_order=sort_order,
    )

    # 조회수 상승
    cookie = request.cookies.get(f"q{question_id}")
    if not cookie:
        response.set_cookie(
            key=f"q{question_id}",
            value=str(question_id),
            max_age=60,     # 만료시간 1분
        )
        question_crud.up_hits(db, question)  # 질문 조회수 상승

    return {"total": total, "question": question}  # {답변 건수, 답변 상세조회}


# 질문 등록
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 질문 등록하기
    question_crud.question_create(db, question_create, user=current_user)


# 질문 수정
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(
    question_update: question_schema.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 수정할 질문 가져오기
    question = question_crud.get_question(db, question_id=question_update.id)

    # 질문이 없는 경우
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 질문입니다."
        )

    # 권한 유무 확인
    if current_user.id != question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."
        )

    # 질문 수정하기
    question_crud.question_update(db, question, question_update=question_update)


# 질문 삭제 api
@router.delete("/delete/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 삭제할 질문 가져오기
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 질문입니다."
        )
    if current_user.id != question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )

    # 삭제하기
    question_crud.question_delete(db, question)


# 질문 추천 api
@router.post("/vote/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 추천할 질문 가져오기
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 질문입니다."
        )

    # 가져온 질문에 대한 추천 정보 가져오기
    voter_information = question_crud.get_question_voter(
        db, current_user.id, question_id
    )

    # 추천 여부 판단해서 추천 or 추천취소
    if not voter_information:
        # 질문 추천
        question_crud.question_vote(db, question, current_user)
    else:
        # 질문 추천취소
        question_crud.question_unvote(db, question, current_user)