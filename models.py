from sqlalchemy import Column, Integer, String, Table, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 추천 모델
# 다대다(N:N)
# 다대다 관계를 적용하기 위해서는 sqlalchemy의 `Table`을 사용하여 다대다 관계를 의미하는 테이블을 먼저 생성해야됨
question_voter = Table(
    "question_voter",   # 테이블명
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("question.id"), primary_key=True)
)

answer_voter = Table(
    "answer_voter",     # 테이블명
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("answer_id", Integer, ForeignKey("answer.id"), primary_key=True)
)

board_voter = Table(
    "board_voter",     # 테이블명
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("board_id", Integer, ForeignKey("board.id"), primary_key=True)
)


# 질문 모델
class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship("User", secondary=question_voter, backref="question_voters")   # 질문에 대한 추천인
    # secondary 속성
    # secondary 값으로 question_voter 테이블 객체를 지정해주면
    # Question 모델을 통해 추천인을 저장하면 실제 데이터는 question_voter 테이블에 저장되고
    # 저장된 추천인 정보는 Question 모델의 voter 속성을 통해 참조할 수 있다.
    hits = Column(Integer, nullable=False, default=0)


# 답변 모델
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship("User", secondary=answer_voter, backref="answer_voters")   # 답변에 대한 추천인
    # secondary 속성
    # secondary 값으로 answer_voter 테이블 객체를 지정해주면
    # Answer 모델을 통해 추천인을 저장하면 실제 데이터는 answer_voter 테이블에 저장되고
    # 저장된 추천인 정보는 Answer 모델의 voter 속성을 통해 참조할 수 있다.


# 회원 모델
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# 자유게시판 모델
class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="board_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship("User", secondary=board_voter, backref="board_voters")   # 질문에 대한 추천인
    # secondary 속성
    # secondary 값으로 question_voter 테이블 객체를 지정해주면
    # Question 모델을 통해 추천인을 저장하면 실제 데이터는 question_voter 테이블에 저장되고
    # 저장된 추천인 정보는 Question 모델의 voter 속성을 통해 참조할 수 있다.
    hits = Column(Integer, nullable=False, default=0)