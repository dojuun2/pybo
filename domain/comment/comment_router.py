from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from domain.comment import comment_crud, comment_schema
from domain.board import board_crud

from database import get_db
from domain.user.user_router import get_current_user
from models import User


router = APIRouter(prefix="/api/comment")


# 댓글 등록 api
@router.post("/create/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def create_comment(
    board_id: int,
    comment_create: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 게시글 가져오기
    board = board_crud.get_board_detail(db=db, board_id=board_id)
    if not board:
        raise HTTPException(status_code=404, detail="존재하지 않는 게시글입니다.")

    # 댓글 등록
    comment_crud.create_comment(
        db=db, comment_create=comment_create, board=board, user=user
    )
