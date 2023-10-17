from sqlalchemy.orm import Session
from models import User
from domain.user import user_schema
from passlib.context import CryptContext

# bcrypt 알고리즘을 사용하는 pwd_context 객체 생성
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 회원 등록
def user_create(db: Session, user_create: user_schema.UserCreate):
    user = User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),  # 암호화해서 저장
        email=user_create.email,
    )
    db.add(user)
    db.commit()


# 이미 존재하는 회원 가져오기
def get_existing_user(db: Session, user_create: user_schema.UserCreate):
    existing_user = db.query(User).filter(
        (User.username == user_create.username) | (User.password == user_create.password1)
    ).first()
    
    return existing_user


# 회원 조회
# 로그인 시에 회원의 비밀번호를 비교하기 위해 사용될 get_user 함수
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# 로그인
def user_login(db: Session):
    pass