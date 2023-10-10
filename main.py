from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
def test():
    return {"message" : "api 테스트"}