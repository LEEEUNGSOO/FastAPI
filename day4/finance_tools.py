import json
from pathlib import Path
import pandas as pd

# 현재 파일이 있는 폴더 아래의 data 경로 설정
DATA = Path(__file__).parent / "data"

# 계좌 CSV를 DataFrame으로 읽기
ACCOUNTS = pd.read_csv(DATA / "accounts.csv")

# 거래 CSV를 읽고 date 컬럼을 날짜 타입으로 변환
TRANSACTIONS = pd.read_csv(DATA / "transactions.csv", parse_dates=["date"])


# ② 계좌번호에 해당하는 잔액 조회
def get_balance(account_id: str) -> dict:
    rows = ACCOUNTS[ACCOUNTS["account_id"] == account_id]  # 조건에 맞는 행 선택
    if rows.empty:
        return {"error": f"계좌를 찾을 수 없습니다: {account_id}"}
    row = rows.iloc[0]
    return {"account_id": str(row["account_id"]),
            "owner_name": str(row["owner_name"]),
            "balance": int(row["balance"])}


# ② 계좌별 최근 거래 조회
def get_transactions(account_id: str, limit: int = 5) -> dict:
    # account_id 값 하나가 Set 전체에 포함되어 있는지 검사
    if account_id not in set(ACCOUNTS["account_id"]):
        return {"error": f"계좌를 찾을 수 없습니다: {account_id}"}
    df = TRANSACTIONS[TRANSACTIONS["account"] == account_id]
    df = df.sort_values("date", ascending=False)  # 최신 거래부터 정렬
    total_count = len(df)
    # 각 행을 꺼내 딕셔너리로 변환한 뒤 리스트 생성
    items = [
        {"date": r.date.strftime("%Y-%m-%d"),
         "category": str(r.category), "amount": int(r.amount)}
        for r in df.head(limit).itertuples()
    ]
    return {"account_id": account_id, "total_count": total_count,
            "transactions": items}


# ② 거래 종류별 건수·금액 합계
def get_summary(account_id: str) -> dict:
    if account_id not in set(ACCOUNTS["account_id"]):
        return {"error": f"계좌를 찾을 수 없습니다: {account_id}"}
    df = TRANSACTIONS[TRANSACTIONS["account"] == account_id]
    grouped = df.groupby("category")["amount"].agg(["count", "sum"])
    items = [
        {"category": str(category), "count": int(row["count"]),
         "total": int(row["sum"])}
        for category, row in grouped.iterrows()
    ]
    return {"account_id": account_id, "categories": items}


# ③ LLM에 전달할 함수 설명서 구성
def tool_spec(name, description, extra=None):
    props = {"account_id": {"type": "string", "description": "계좌번호, 예: A001"}}
    if extra:
        props.update(extra)
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object", "properties": props,
                       "required": ["account_id"], "additionalProperties": False}
    }}


# ③ AI가 선택할 수 있는 도구 목록 (메뉴판)
TOOLS = [
    tool_spec("get_balance", "계좌 잔액을 조회한다."),
    tool_spec("get_transactions", "계좌의 최근 거래내역을 조회한다.",
              {"limit": {"type": "integer", "description": "최대 표시 건수", "minimum": 1, "maximum": 20}}),
    tool_spec("get_summary", "계좌의 거래 카테고리별 건수와 금액 합계를 조회한다.")
]
# ③ 도구 이름과 실제 실행 함수 연결표
FUNCTIONS = {"get_balance": get_balance,
             "get_transactions": get_transactions,
             "get_summary": get_summary}


# ③ 요청받은 이름과 인자로 실제 함수 실행
def run_tool(name: str, arguments: str) -> dict:
    if name not in FUNCTIONS:
        return {"error": f"허용되지 않은 도구: {name}"}
    try:
        return FUNCTIONS[name](**json.loads(arguments))
    except (TypeError, ValueError, KeyError) as e:
        return {"error": f"도구 실행 오류: {e}"}


# 파일 단독 실행 시 잔액 조회 테스트
if __name__ == "__main__":
    print("===== A001 계좌 조회 =====")
    print(get_balance("A001"))