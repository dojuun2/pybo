from datetime import datetime
from sqlalchemy.orm import Session
from domain.comment import comment_schema

from models import Board, Comment, User, comment_voter


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


# 댓글 상세조회
def get_comment_detail(db: Session, comment_id: id):
    db_comment = db.query(Comment).get(comment_id)
    return db_comment


# 댓글 수정
def update_comment(
    db: Session, comment: Comment, comment_update: comment_schema.CommentUpdate
):
    comment.content = comment_update.content
    comment.modify_date = datetime.now()
    db.add(comment)
    db.commit()


# 댓글 삭제
def delete_comment(db: Session, comment: Comment):
    db.delete(comment)
    db.commit()


# 댓글 추천
def recommend_comment(db: Session, comment: Comment, user: User):
    comment.voter.append(user)
    db.commit()


# 추천 정보 가져오기
def get_comment_vote_info(db: Session, comment_id: int, user_id: int):
    vote_info = (
        db.query(comment_voter)
        .filter(
            comment_voter.c.comment_id == comment_id, 
            comment_voter.c.user_id == user_id
        )
        .first()
    )

    return vote_info
