from fastapi import APIRouter, Depends
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