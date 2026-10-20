import json

from finance_tools import FUNCTIONS, TOOLS, run_tool

print("===== 1. 메뉴판(TOOLS) 도구 이름 =====")
print([t["function"]["name"] for t in TOOLS])

print("===== 2. get_balance 메뉴판 한 칸 =====")
print(json.dumps(TOOLS[0], ensure_ascii=False, indent=2))

print("===== 3. 연결표(FUNCTIONS) =====")
print(list(FUNCTIONS))

print("===== 4. run_tool — LLM 의 부탁을 흉내 =====")
print(run_tool("get_balance", '{"account_id": "A001"}'))   # 인자는 JSON 글자
print(run_tool("delete_all", "{}"))                        # 연결표에 없는 이름