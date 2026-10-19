from datetime import date  #datae Type

import pandas as pd #csv읽기 ,필터 , group by
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

app = FastAPI(title="금융 분석 서버")   # /docs 맨 위에 나오는 이름


# ===== STEP 1. 첫 서버 =====
@app.get("/")
def hello():
    return {"message": "안녕하세요, 금융 분석 서버입니다."}


@app.get("/health")
def health():
    return {"status": "ok"}


# ===== STEP 2. 라우팅 연습 =====
@app.get("/accounts/{account_id}")
def get_account(account_id: str):                 # 경로 값 (@PathVariable)
    return {"account_id": account_id}


@app.get("/rates/{year}")
def get_rate(year: int):                          # "2026" → 2026, "abc" → 422
    return {"year": year, "rate": 3.5}


@app.get("/search")
def search(category: str, min_amount: int = 0, limit: int = 10):   # 쿼리 값 (@RequestParam)
    return {"category": category, "min_amount": min_amount, "limit": limit}


# ===== STEP 3. Pydantic =====
class CamelModel(BaseModel):                      # JSON에서는 account_id ↔ accountId
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FeeRequest(CamelModel):                     # 요청 DTO
    amount: int = Field(gt=0)
    fee_rate: float = Field(default=0.0015, ge=0, le=0.01)


class FeeResponse(CamelModel):                    # 응답 DTO
    amount: int
    fee: int


@app.post("/fee", response_model=FeeResponse)
def calc_fee(req: FeeRequest):                   # 요청 본문 (@RequestBody)
    return FeeResponse(amount=req.amount, fee=round(req.amount * req.fee_rate))


# ===== STEP 4. 금융 조회 API =====
def load_transactions() -> pd.DataFrame:
    df = pd.read_csv("data/transactions.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_accounts() -> pd.DataFrame:
    return pd.read_csv("data/accounts.csv")


TRANSACTIONS = load_transactions()               # 서버 켜질 때 한 번만 읽음
ACCOUNTS = load_accounts()


class Balance(CamelModel):
    account_id: str
    owner_name: str
    balance: int


class Transaction(CamelModel):
    tx_id: str
    date: date
    category: str
    amount: int


class CategorySummary(CamelModel):
    category: str
    count: int
    total: int


def find_account(account_id: str) -> pd.Series:
    rows = ACCOUNTS[ACCOUNTS["account_id"] == account_id]
    if rows.empty:
        raise HTTPException(status_code=404, detail=f"계좌를 찾을 수 없습니다: {account_id}")
    return rows.iloc[0]


@app.get("/accounts/{account_id}/balance", response_model=Balance)
def get_balance(account_id: str):
    row = find_account(account_id)
    return Balance(account_id=row["account_id"], owner_name=row["owner_name"],
                   balance=int(row["balance"]))


@app.get("/accounts/{account_id}/transactions", response_model=list[Transaction])
def get_transactions(account_id: str,
                     start: date | None = None,
                     end: date | None = None,
                     category: str | None = None,
                     limit: int = Query(default=20, le=100)):
    find_account(account_id)
    df = TRANSACTIONS[TRANSACTIONS["account"] == account_id]
    if start:
        df = df[df["date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["date"] <= pd.Timestamp(end)]
    if category:
        df = df[df["category"] == category]
    df = df.sort_values("date", ascending=False).head(limit)
    return [Transaction(tx_id=r.tx_id, date=r.date.date(), category=r.category, amount=int(r.amount))
            for r in df.itertuples()]


@app.get("/accounts/{account_id}/summary", response_model=list[CategorySummary])
def get_summary(account_id: str):
    find_account(account_id)
    df = TRANSACTIONS[TRANSACTIONS["account"] == account_id]
    g = df.groupby("category")["amount"].agg(["count", "sum"]).reset_index()
    return [CategorySummary(category=r.category, count=int(r.count), total=int(r.sum))
            for r in g.itertuples()]