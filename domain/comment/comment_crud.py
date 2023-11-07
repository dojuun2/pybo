from datetime import datetime
from sqlalchemy.orm import Session
from domain.comment import comment_schema

from models import Board, Comment, User


# 댓글 등록
def create_comment(
    db: Session, comment_create: comment_schema.CommentCreate, board: Board, user: User
):
    db_comment = Comment(
        content=comment_create.content,
        create_date=datetime.now(),
        board=board,
        user=user,
    )
    db.add(db_comment)
    db.commit()
