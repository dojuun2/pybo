# PYBO
`FastAPI`를 활용한 간단한 게시판 프로젝트

## API 문서
- Swagger: http://127.0.0.1:8000/docs

## 요구사항
- Python3
- FastAPI
- Node.js
- Svelte
- Sqlite3

## 프로젝트 구조
### 파일
- main.py: 프로젝트 설정 파일
- database.py: 데이터베이스 설정 파일
- models.py: 모델 관리 파일

### 디렉터리
- domain: API 구성 디렉터리
- frontend: Svelte 프레임워크 디렉터리

## 필요 라이브러리 설치 명령어(계속 추가 예정)
```bash
# Backend
# fastapi 프레임워크 설치 명령어
pip install fastapi

# uvicorn
pip install "uvicorn[standard]"

# SQLAlchemy
pip install sqlalchemy

# alembic
pip install alembic

# email_validator
pip install "pydantic[email]"

# passlib
# 비밀번호를 암호화하기위한 라이브러리
pip install "passlib[bcrypt]"

# 인증 관련 라이브러리
pip install python-multipart
pip install "python-jose[cryptography]"


# Frontend
# Svelte 프레임워크 설치 명령어
npm create vite@latest frontend -- --template svelte

# svelte-spa-router 설치 명령어
npm install svelte-spa-router

# 부트스트랩
npm install bootstrap

# moment
npm install moment

# qs 패키지
npm install qs
```

## Commands
```bash
# 가상환경 생성
python -m venv .pybo

# 가상환경 접속 (필수)
. .pybo/Scripts/activate

# venv 실행이 안될 시 Powershell 관리자 권한 주기
Set-ExecutionPolicy RemoteSigned

# 가상환경 연결해제
deactivate

# 프로젝트 실행
python ./src/app.py

# pip 업그레이드
python -m pip install --upgrade pip

# FastAPI 서버 실행
# C:\projects\myapi>
uvicorn main:app --reload

# Svlete 서버 실행하기
# C:\projects\myapi\frontend>
npm run dev


# 모델 관련 명령어
# 1. alembic 초기화 작업
alembic init migrations

# 1-1. alembic.ini 파일 > `sqlalchemy.url = sqlite:///./pybo.db`로 수정
# 1-2. env.py 파일 > `import models` 해주고, `target_metadata = models.Base.metadata` 코드 추가

# 2. 리비전 파일 생성하기
# 리비전 파일에는 테이블을 생성 또는 변경하는 실행문들이 들어있음
alembic revision --autogenerate

# 3. 리비전 파일 실행
# 테이블이 생성됨
alembic upgrade head
```