from datetime import datetime
from domain.answer import answer_schema
from models import Answer, Question, User
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


# # 답변 조회
# def answer_list(db: Session, question: Question):
#     answer = db.query(Answer).filter(Question.id==question.id).all()
#     return answer
