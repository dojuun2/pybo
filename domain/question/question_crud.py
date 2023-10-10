from sqlalchemy.orm import Session
from models import Question


# 질문 목록 조회
def question_list(db: Session):
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list