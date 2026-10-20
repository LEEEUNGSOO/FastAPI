import requests
import streamlit as st

st.title("금융 AI 비서")  # 채팅 화면 제목
st.caption("A001 잔액을 물어보세요.")

# 채팅 기록을 세션에 저장 (messages 저장공간이 없으면 만든다)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장된 대화를 화면에 다시 출력
# 예) [{"role": "user", "content": "안녕하세요"}, {"role": "assistant", "content": "무엇을 도와드릴까요?"}]
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

question = st.chat_input("질문을 입력하세요")  # 사용자 질문 입력
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):  # 이 영역 안에 출력
        st.write(question)

    try:  # FastAPI 서버에 질문 전송
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": question},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()  # 서버 응답 읽기
        answer = data["answer"]  # AI가 만든 답변
        steps = data["steps"]
    except requests.RequestException as e:
        answer, steps = f"서버 요청에 실패했습니다: {e}", []

    # "user" → 사용자 아이콘, "assistant" → AI 아이콘 자동 표시
    with st.chat_message("assistant"):
        st.write(answer)
        if steps:  # 실행한 도구 기록 표시
            with st.expander("사용한 도구 보기"):
                st.json(steps)
    st.session_state.messages.append({"role": "assistant", "content": answer})  # 답변 기록