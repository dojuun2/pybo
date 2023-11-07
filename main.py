from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware    # CORS 예외 처리 관련 라이브러리
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router     # 질문 라우터
from domain.answer import answer_router     # 답변 라우터
from domain.user import user_router     # 회원 라우터
from domain.board import board_router     # 자유게시판 라우터
from domain.comment import comment_router     # 댓글 라우터

app = FastAPI()

# CORS 예외 처리
origins = [
    "http://localhost:5173"     # 또는 "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(board_router.router)
app.include_router(comment_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets")) # frontend/dist/assets 디렉터리를 /assets 경로로 매핑할 수 있도록 하는 설정


# / 경로로 접속하면 frontend/dist/index.html 파일을 읽어서 서비스 할 수 있도록 하는 index 함수
@app.get("/")
def index():
    # FileResponse는 FastAPI가 정적인 파일을 출력할 때 사용한다
    return FileResponse("frontend/dist/index.html")