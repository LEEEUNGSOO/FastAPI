from llm import MODEL, get_client

QUESTION = "A001 계좌 잔액 얼마야?"
response = get_client().chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": QUESTION}],   # 도구 없이 질문만
)

print("===== 1. 질문 =====")
print(QUESTION)
print("===== 2. 도구 없이 LLM 답 =====")
print(response.choices[0].message.content)