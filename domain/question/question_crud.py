from datetime import datetime
from domain.question import question_schema
from sqlalchemy.orm import Session
from models import Question, User


# 질문 목록 조회
def question_list(db: Session, skip: int = 0, limit: int = 10):
    """
    Args:
        - skip: 조회한 데이터의 시작 위치
        - limit: 시작 위치부터 가져올 데이터 건수

    Returns:
        total, question_list
    """
    question_list_query = db.query(Question).order_by(Question.id.desc())  # 쿼리문
    total = question_list_query.count()  # 전체 건수

    question_list = question_list_query.offset(skip).limit(limit).all()  # 페이징 처리된 질문 목록

    return total, question_list


# 질문 상세 조회
def question_detail(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


# 질문 등록
def question_create(
    db: Session, question_create: question_schema.QuestionCreate, user: User
):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_question)
    db.commit()


# 질문 수정
def question_update(db: Session, question: Question, question_update: question_schema.QuestionUpdate):
    question.subject = question_update.subject
    question.content = question_update.content
    question.modify_date = datetime.now()
    
    db.add(question)
    db.commit()
