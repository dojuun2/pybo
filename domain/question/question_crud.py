from datetime import datetime
from domain.question import question_schema
from sqlalchemy.orm import Session
from models import Answer, Question, User, question_voter


# 질문 목록 조회
def question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ""):
    """
    Args:
        - skip: 조회한 데이터의 시작 위치
        - limit: 시작 위치부터 가져올 데이터 건수

    Returns:
        total, question_list
    """
    question_list = db.query(Question)      # 쿼리문

    # 검색을 했는지
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = (
            db.query(Answer.question_id, Answer.content, User.username)
            .outerjoin(User, Answer.user_id == User.id)
            .subquery()
            # SELECT answer.question_id, answer.content, "user".username FROM answer LEFT OUTER JOIN "user" ON answer.user_id = "user".id
        )
        question_list = (
            question_list.outerjoin(User)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(
                Question.subject.ilike(search)              # 질문 제목
                | Question.content.ilike(search)            # 질문 내용
                | User.username.ilike(search)               # 질문 작성자
                | sub_query.c.content.ilike(search)         # 답변 내용
                | sub_query.c.username.ilike(search)    # 답변 작성자
            )
        )

    total = question_list.count()  # 전체 건수
    question_list = question_list.order_by(Question.id.desc()).offset(skip).limit(limit).distinct().all()  # 페이징 처리된 질문 목록

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
def question_update(
    db: Session, question: Question, question_update: question_schema.QuestionUpdate
):
    question.subject = question_update.subject
    question.content = question_update.content
    question.modify_date = datetime.now()

    db.add(question)
    db.commit()


# 질문 삭제
def question_delete(db: Session, question: Question):
    db.delete(question)
    db.commit()


# 질문 추천
def question_vote(db: Session, question: Question, user: User):
    question.voter.append(user)
    db.commit()


# 질문 추천취소
def question_unvote(db: Session, question: Question, user: User):
    question.voter.remove(user)
    db.commit()


# 추천 정보 가져오기
def get_question_voter(db: Session, user_id: int, question_id: int):
    voter_information = (
        db.query(question_voter)
        .filter(
            question_voter.c.user_id == user_id,
            question_voter.c.question_id == question_id,
        )
        .first()
    )
    return voter_information
