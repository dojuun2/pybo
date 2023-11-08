from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from domain.board import board_schema, board_crud
from starlette import status
from domain.user.user_router import get_current_user

from models import User


router = APIRouter(prefix="/api/board")


# 게시글 등록 api
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_board(
    board_create: board_schema.BoardCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board_crud.create_board(board_create, db, user)


# 게시글 목록 api
@router.get("/list", response_model=board_schema.BoardList)
def get_board_list(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 10,
):
    total, board_list = board_crud.get_board_list(db, skip=page * size, limit=size)

    return {"total": total, "board_list": board_list}


# 게시글 상세조회 api
@router.get("/detail/{board_id}", response_model=board_schema.Board)
def get_board_detail(board_id: int, db: Session = Depends(get_db)):
    board_detail = board_crud.get_board_detail(board_id=board_id, db=db)

    return board_detail


# 게시글 수정 api
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
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

    # 게시글 수정
    board_crud.update_board(
        db=db, board=board, board_update=board_update, user=current_user
    )
