from datetime import datetime

from sqlalchemy import select
from domain.answer import answer_schema
from models import Answer, Question, User, answer_voter
from sqlalchemy.orm import Session


# 답변 등록
def answer_create(
    db: Session,
    answer_create: answer_schema.AnswerCreate,
    question: Question,
    user: User,
):
    db_answer = Answer(
        content=answer_create.content,
        create_date=datetime.now(),
        question=question,
        user=user,  # 작성자
    )
    db.add(db_answer)
    db.commit()


# 답변 상세조회
def answer_detail(db: Session, answer_id: int):
    answer = db.query(Answer).get(answer_id)
    return answer


# 답변 수정
def answer_update(
    db: Session, answer: Answer, answer_update: answer_schema.AnswerUpdate
):
    answer.content = answer_update.content
    answer.modify_date = datetime.now()
    db.add(answer)
    db.commit()


# 답변 삭제
def answer_delete(db: Session, answer: Answer):
    db.delete(answer)
    db.commit()


# 답변 추천
def answer_vote(db: Session, answer: Answer, user: User):
    answer.voter.append(user)
    db.commit()


# 답변 추천취소
def answer_unvote(db: Session, answer: Answer, user: User):
    answer.voter.remove(user)
    db.commit()


# 답변 추천정보 가져오기
def get_answer_voter(db: Session, user_id: int, answer_id: int):
    # select 쿼리
    query = select(answer_voter).where(
        (answer_voter.c.user_id == user_id) & (answer_voter.c.answer_id == answer_id)
    )
    
    # 추천정보 조회
    voter_information = db.execute(query).first()
    
    return voter_information


# # 답변 목록 조회
# def answer_list(db: Session, question: Question):
#     answer = db.query(Answer).filter(Question.id==question.id).all()
#     return answer
