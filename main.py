from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware    # CORS 예외 처리 관련 라이브러리
from domain.question import question_router     # 질문 라우터

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