# SYSTEM은 LLM에게 주는 근무규칙입니다 ,잔액은 반드시 도구로 조회하고 결과가 없는것을 숫자로 만들지 마~
#run_agent는 오늘의 주인공입니다 질문을 받아서 LLM과 도구 사이를 오가는 매니저입니다
import json
from llm import MODEL, get_client
from finance_tools import TOOLS, run_tool

SYSTEM = "너는 금융 상담 도우미다. 계좌 잔액은 반드시 도구로 조회하고, 결과에 없는 숫자는 만들지 않는다."


# 사용자 질문을 받아 도구 호출과 답변 생성
def run_agent(question: str):
    client = get_client()
    messages = [  # 모델에 전달할 대화 기록
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question}
    ]
    steps = []

    # ⑤ 도구 요청이 끝날 때까지 최대 5단계 반복
    for _ in range(5):
        # ④ 질문과 도구 설명서를 LLM에 전달
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS,
            tool_choice="auto"
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))  # LLM 응답 기록

        if not message.tool_calls:  # 도구 요청이 없으면 최종 답변
            return {"answer": message.content or "", "steps": steps}

        for call in message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            result = run_tool(name, args)  # 실제 금융 함수 실행
            steps.append({"tool": name, "arguments": args, "result": result})
            messages.append({  # 도구 실행 결과를 대화에 추가
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })

    return {"answer": "도구 실행 횟수 한도에 도달했습니다.", "steps": steps}


# 파일을 직접 실행할 때 Agent 동작 테스트
if __name__ == "__main__":
    result = run_agent("A001 잔액 얼마야?")
    print("===== AI 답변 =====")
    print(result["answer"])
    print("===== 사용한 도구 =====")
    for step in result["steps"]:
        print(step["tool"], step["result"])