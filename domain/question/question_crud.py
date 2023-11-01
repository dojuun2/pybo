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
    question_list = db.query(Question)  # 쿼리문

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
                Question.subject.ilike(search)  # 질문 제목
                | Question.content.ilike(search)  # 질문 내용
                | User.username.ilike(search)  # 질문 작성자
                | sub_query.c.content.ilike(search)  # 답변 내용
                | sub_query.c.username.ilike(search)  # 답변 작성자
            )
        )

    total = question_list.count()  # 전체 건수
    question_list = (
        question_list.order_by(Question.id.desc())
        .offset(skip)
        .limit(limit)
        .distinct()
        .all()
    )  # 페이징 처리된 질문 목록

    return total, question_list


# 질문 상세 조회
def question_detail(db: Session, question_id: int, limit: int = 10, method: str = ""):
    """
    Args:
        - question_id (int): 질문 번호
        - skip (int, optional): 조회한 데이터의 시작 인덱스
        - limit (int, optional): 시작 인덱스부터 가져올 데이터 건수
    
    Returns
        - total (int): 답변 건수
        - question (Question): 질문 select 값
    """
    # 질문 가져오기
    question = db.query(Question).get(question_id)

    # 답변 등록 요청일 경우
    if method == "answer_create":
        return question
    
    # 질문 상세조회 요청일 경우
    else:  
        # 질문에 달린 답변 가져오기
        answer_list = db.query(Answer).filter(Answer.question_id == question_id)

        answer_total = answer_list.count()  # 답변 건수
        answer_list = answer_list.order_by(Answer.id.desc()).limit(limit).all()    # 답변 목록 페이징 처리
        
        # 페이징 처리된 답변 목록 세팅
        question.answers = answer_list

        return answer_total, question   # (답변 건수, 정렬된 답변 목록, 답변) 반환


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
