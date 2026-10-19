from fastapi import FastAPI

app = FastAPI(title="금융 분석 서버")    # 서버 객체. /docs 맨 위에 이 title이 나온다

@app.get("/")                            # GET / 요청이 오면 아래 함수를 실행한다
def hello():
    return {"message": "안녕하세요, 금융 분석 서버입니다."}   # dict를 돌려주면 JSON으로 나간다

@app.get("/health")                      # 서버가 살아 있나 확인하는 주소
def health():
    return {"status": "ok"}