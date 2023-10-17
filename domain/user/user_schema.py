from pydantic import BaseModel, EmailStr, validator


# 회원가입 입력 스키마
class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @validator("username", "password1", "password2", "email")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    @validator("password2")
    def passwords_match(cls, v, values):
        """비밀번호 유효성 검사를 수행하는 함수

        Args:
            v (str): _password2의 속성값
            values (dict): _다른 속성들의 값

        Raises:
            ValueError: 비밀번호가 일치하지 않는 것에 대한 에러
        """
        if "password1" in values and v != values["password1"]:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v


# 로그인 입력 스키마
# fastapi의 security 패키지에 있는 OAuth2PasswordRequestForm 클래스를 사용하기 때문에 따로 만들 필요가 없음


# 로그인 출력 스키마
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str