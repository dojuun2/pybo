from pydantic import BaseModel, validator


# 댓글 등록 스키마
class CommentCreate(BaseModel):
    content: str
    
    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v