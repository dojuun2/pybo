from datetime import datetime, timedelta
from os import access
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from database import get_db
from domain.user import user_schema
from starlette import status
from domain.user import user_crud
from domain.user.user_crud import pwd_context

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
# SECRET_KEY 생성하기
# import secrets
# secrets.token_hex(32)
SECRET_KEY = "d8ef910d62c71eb1fe7117f9fc623f863a06b9a07c86a53c1550bc6a963a92d5"
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/user")


# 회원 등록
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 존재하는 회원인지 체크
    existing_user = user_crud.get_existing_user(db=db, user_create=user_create)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 회원입니다."
        )

    # 회원 등록하기
    user_crud.user_create(db=db, user_create=user_create)


# 로그인
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # 회원 체크
    user = user_crud.get_user(db, username=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 맞지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},     # 인증 방식에 대한 추가 정보
        )
    
    # 토큰 생성
    data = {
        "sub": user.username,   # 사용자 이름
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)   # 토큰 유효기간
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
