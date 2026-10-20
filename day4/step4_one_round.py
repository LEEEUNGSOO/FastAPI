import json

from finance_tools import TOOLS, run_tool
from llm import MODEL, get_client

client = get_client()
messages = [{"role": "user", "content": "A001 잔액 얼마야?"}]

# ① 질문 + 메뉴판 → ② LLM 은 부탁만 한다
first = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
msg = first.choices[0].message
if not msg.tool_calls:
    raise SystemExit("LLM 이 도구를 고르지 않았습니다. 다시 실행해 보세요: " + str(msg.content))
call = msg.tool_calls[0]

print("===== 1. LLM 의 부탁 (tool_calls) =====")
print("id       :", call.id)
print("name     :", call.function.name)
print("arguments:", call.function.arguments)

# ③ 실행은 우리 코드가 한다
result = run_tool(call.function.name, call.function.arguments)
print("===== 2. 우리 코드가 실행한 결과 =====")
print(result)

# ④ 부탁과 결과를 같은 번호표(tool_call_id)로 기록에 쌓는다
messages.append(msg.model_dump(exclude_none=True))
messages.append({"role": "tool", "tool_call_id": call.id,
                 "content": json.dumps(result, ensure_ascii=False)})

# ⑤ LLM 을 한 번 더 불러 사람 말로 답을 받는다
second = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
print("===== 3. 최종 답 =====")
print(second.choices[0].message.content)

print("===== 4. messages 에 쌓인 역할 =====")
print([m["role"] for m in messages])