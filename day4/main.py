import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import run_agent

app = FastAPI(title="금융 AI 비서")  # API 서버 생성


# 채팅 요청 데이터 구조
class ChatRequest(BaseModel):
    message: str


# 요청 내용을 Agent로 전달하고 결과 반환
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        return run_agent(req.message)
    except Exception:
        raise HTTPException(status_code=503, detail="AI 호출에 실패했습니다. 서버 설정과 터미널 로그를 확인하세요.")


# 파일 직접 실행 시 FastAPI 서버 시작
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)