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


# 게시글 목록 조회
def get_board_list(db: Session, skip: int, limit: int):
    # 게시글 목록 조회
    board_list = db.query(Board)
    
    total = board_list.count()  # 전체 게시물 수
    board_list = board_list.order_by(Board.id.desc()).limit(limit).offset(skip).all()   # 페이징 처리
    
    return total, board_list


# 게시글 상세조회
def get_board_detail(db: Session, board_id: int):
    board_detail = db.query(Board).get(board_id)
    return board_detail