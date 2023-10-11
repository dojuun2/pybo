from datetime import datetime
from domain.question.question_schema import QuestionCreate
from sqlalchemy.orm import Session
from models import Question


# 질문 목록 조회
def question_list(db: Session):
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list


# 질문 상세 조회
def question_detail(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


# 질문 등록
def question_create(db: Session, question_create: QuestionCreate):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
    )
    db.add(db_question)
    db.commit()
