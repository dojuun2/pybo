from datetime import datetime, timedelta
from email import header
from os import access
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
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

# 사용자 조회를 할 때 사용 될 'token'이 자동으로 매핑됨
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

router = APIRouter(prefix="/api/users")


# 회원 등록
@router.post("", status_code=status.HTTP_204_NO_CONTENT)
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
            headers={"WWW-Authenticate": "Bearer"},  # 인증 방식에 대한 추가 정보
        )

    # 토큰 생성
    data = {
        "sub": user.username,  # 사용자 이름
        "exp": datetime.utcnow()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # 토큰 유효기간
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }


# 로그인 사용자 정보 조회
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """헤더 정보의 토큰값으로 사용자 정보를 조회하는 함수
    
    Args:
        token (str): 헤더 정보에 포함된 토큰값.
    
        db (Session): 데이터베이스 세션 객체. 

    Returns:
        user: 로그인한 사용자 정보 객체
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 토큰을 복호화하여 토큰에 담겨 있는 사용자명을 얻어낼수 있음
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        # 사용자 가져오기
        user = user_crud.get_user(db=db, username=username)
        
        if user is None:
            raise credentials_exception
        
        return user