from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status
from domain.comment import comment_crud, comment_schema
from domain.board import board_crud

from database import get_db
from domain.user.user_router import get_current_user
from models import User


router = APIRouter(prefix="/api/comments")


# 댓글 등록 api
@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def create_comment(
    comment_create: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 게시글 가져오기
    board = board_crud.get_board_detail(db=db, board_id=comment_create.board_id)
    if not board:
        raise HTTPException(status_code=404, detail="존재하지 않는 게시글입니다.")

    # 댓글 등록
    comment_crud.create_comment(
        db=db, comment_create=comment_create, board=board, user=current_user
    )


# 댓글 상세조회 api
@router.get("/{comment_id}", response_model=comment_schema.Comment)
def get_comment_detail(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment_detail(db, comment_id=comment_id)
    return comment


# 댓글 수정 api
@router.put("", status_code=status.HTTP_204_NO_CONTENT)
def update_comment(
    comment_update: comment_schema.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 수정할 댓글 가져오기
    comment = comment_crud.get_comment_detail(db, comment_id=comment_update.id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 댓글입니다."
        )
    if current_user.id != comment.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."
        )

    # 댓글 수정하기
    comment_crud.update_comment(db, comment=comment, comment_update=comment_update)


# 댓글 삭제 api
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 삭제할 댓글 가져오기
    comment = comment_crud.get_comment_detail(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 댓글입니다."
        )
    if current_user.id != comment.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."
        )
    
    # 댓글 삭제하기
    comment_crud.delete_comment(db, comment=comment)
