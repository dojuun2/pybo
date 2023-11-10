from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from domain.board import board_schema, board_crud
from starlette import status
from domain.user.user_router import get_current_user

from models import User


router = APIRouter(prefix="/api/boards")


# 게시글 등록 api
@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def create_board(
    board_create: board_schema.BoardCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board_crud.create_board(board_create, db, user)


# 게시글 목록 api
@router.get("", response_model=board_schema.BoardList)
def get_board_list(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 10,
):
    total, board_list = board_crud.get_board_list(db, skip=page * size, limit=size)

    return {"total": total, "board_list": board_list}


# 게시글 상세조회 api
@router.get("/{board_id}", response_model=board_schema.Board)
def get_board_detail(board_id: int, db: Session = Depends(get_db)):
    board_detail = board_crud.get_board_detail(board_id=board_id, db=db)

    return board_detail


# 게시글 수정 api
@router.put("", status_code=status.HTTP_204_NO_CONTENT)
def update_board(
    board_update: board_schema.BoardUpdate,  # 수정 스키마
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 수정할 게시글 가져오기
    board = board_crud.get_board_detail(db=db, board_id=board_update.id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 게시글입니다."
        )
    if current_user.id != board.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )

    # 게시글 수정
    board_crud.update_board(db=db, board=board, board_update=board_update)


# 게시글 삭제 api
@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 삭제할 게시글 가져오기
    board = board_crud.get_board_detail(db, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 게시글입니다."
        )
    if current_user.id != board.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )

    # 게시글 삭제
    board_crud.delete_board(db, board=board)


# 게시물 추천 api
@router.post("/recommendations", status_code=status.HTTP_204_NO_CONTENT)
def vote_board(
    board_recommendation: board_schema.BoardRecommendation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 추천할 게시물 가져오기
    board_id = board_recommendation.board_id
    board = board_crud.get_board_detail(db=db, board_id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 게시글입니다."
        )

    # 추천 정보 가져오기
    vote_info = board_crud.get_board_vote_info(
        db, user_id=current_user.id, board_id=board_id
    )
    if vote_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 추천한 게시물입니다."
        )

    # 게시물 추천하기
    board_crud.vote_board(db=db, board=board, user=current_user)


# 게시물 추천 취소 api
@router.delete("/{board_id}/recommendations", status_code=status.HTTP_204_NO_CONTENT)
def unvote_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 추천 취소할 게시물 가져오기
    board = board_crud.get_board_detail(db=db, board_id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 게시글입니다."
        )

    # 추천 정보 가져오기
    vote_info = board_crud.get_board_vote_info(db, user_id=current_user.id, board_id=board_id)
    if not vote_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="추천하지 않은 게시물입니다.")

    # 게시물 추천 취소
    board_crud.unvote_board(db=db, board=board, user=current_user)