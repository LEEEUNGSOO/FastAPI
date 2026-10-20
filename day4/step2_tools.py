from finance_tools import get_balance, get_summary, get_transactions

print("===== 1. get_balance — 잔액 =====")
print(get_balance("A001"))

print("===== 2. get_transactions — 최근 거래 2건 =====")
print(get_transactions("A001", 2))

print("===== 3. get_summary — 유형별 합계 =====")
print(get_summary("A001"))

print("===== 4. 없는 계좌 =====")
print(get_balance("A999"))                          # 에러 대신 error dict