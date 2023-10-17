from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.user import user_schema
from starlette import status
from domain.user import user_crud

router = APIRouter(
    prefix="/api/user"
)


# 회원 등록
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 존재하는 회원인지 체크
    existing_user = user_crud.get_existing_user(db=db, user_create=user_create)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 회원입니다.")
    
    # 회원 등록하기
    user_crud.user_create(db=db, user_create=user_create)
    