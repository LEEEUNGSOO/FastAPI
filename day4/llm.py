import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent / ".env")  # ① 현재 폴더의 .env 읽기
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # ② 모델 이름 읽기


# API 키를 확인하고 클라이언트 생성
def get_client():
    key = os.getenv("OPENAI_API_KEY")  # ③ 키 읽기
    if not key or key.startswith("여기에"):
        raise RuntimeError("day4/.env 의 OPENAI_API_KEY를 확인하세요.")
    return OpenAI(api_key=key)  # ④ 클라이언트 객체 반환


# 파일을 직접 실행할 때 연결 설정 확인
if __name__ == "__main__":
    client = get_client()
    print("OpenAI 클라이언트 생성 성공!")
    print("모델:", MODEL)