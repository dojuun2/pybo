import datetime
from domain.board import board_schema
from sqlalchemy.orm import Session

from models import Board, User


# 게시글 등록
def create_board(board_create: board_schema.BoardCreate, db: Session, user: User):
    db_board = Board(
        subject=board_create.subject,
        content=board_create.content,
        create_date=datetime.datetime.now(),
        user=user,
    )
    db.add(db_board)
    db.commit()
