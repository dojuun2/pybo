import datetime
from domain.board import board_schema
from sqlalchemy.orm import Session

from models import Board, Comment, User, board_voter


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
def get_board_list(db: Session, skip: int, limit: int, keyword: str):
    # 게시글 목록 조회
    board_list = db.query(Board)

    # 검색을 했다면
    if keyword:
        search = f"%%{keyword}%%"
        sub_query = (
            db.query(Comment.board_id, Comment.content, User.username)
            .outerjoin(User, Comment.user_id == User.id)
            .subquery()
            # '댓글'과 그 댓글을 작성한 '댓글 작성자'도 같이 검색
            # SELECT comment.board_id, comment.content, user.username
            # FROM answer
            # LEFT OUTER JOIN user
            # ON comment.user_id = user.id
        )

        board_list = (
            board_list.outerjoin(User)
            .outerjoin(sub_query, sub_query.c.board_id == Board.id)
            .filter(
                Board.subject.ilike(search)  # 게시글 제목
                | Board.content.ilike(search)  # 게시글 내용
                | User.username.ilike(search)  # 게시글 작성자
                | sub_query.c.content.ilike(search)  # 댓글 내용
                | sub_query.c.username.ilike(search)  # 댓글 작성자
            )
        )

    total = board_list.count()  # 전체 게시물 수
    board_list = (
        board_list.order_by(Board.id.desc()).offset(skip).limit(limit).distinct().all()
    )  # 페이징 처리

    return total, board_list


# 게시글 상세조회
def get_board_detail(db: Session, board_id: int):
    board_detail = db.query(Board).get(board_id)
    return board_detail


# 게시글 수정
def update_board(db: Session, board: Board, board_update: board_schema.BoardUpdate):
    board.subject = board_update.subject
    board.content = board_update.content
    db.add(board)
    db.commit()


# 게시글 삭제
def delete_board(db: Session, board: Board):
    db.delete(board)
    db.commit()


# 게시글 추천
def vote_board(db: Session, board: Board, user: User):
    board.voter.append(user)
    db.commit()


# 게시글 추천 취소
def unvote_board(db: Session, board: Board, user: User):
    board.voter.remove(user)
    db.commit()


# 추천 정보 가져오기
def get_board_vote_info(db: Session, user_id: int, board_id: int):
    vote_info = (
        db.query(board_voter)
        .filter(
            board_voter.c.user_id == user_id,
            board_voter.c.board_id == board_id,
        )
        .first()
    )

    return vote_info
