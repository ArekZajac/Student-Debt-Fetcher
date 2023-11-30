import fastapi
from DebtFetcher import DebtFetcher

api = fastapi.FastAPI()

@api.get("/debtinfo")
def debtinfo(username: str, password:str, secret:str):
    fetcher = DebtFetcher()
    debt, rate, asof = fetcher.get_debt_info(username, password, secret)
    return {
        "debt": debt,
        "rate": rate,
        "updated": asof 
    }