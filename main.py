from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PairValue(str, Enum):
    usd = "USD"
    eur = "EUR"
    gbp = "GBP"
    jpy = "JPY"

class Pair(BaseModel):
    id: int
    name: str
    values: tuple[PairValue, PairValue]


async def get_all_pairs():
    # TODO: fix fake async function with real DB data
    pairs = [
        Pair(id=1, name="EURUSD", values=(PairValue.eur, PairValue.usd)),
        Pair(id=2, name="GBPJPY", values=(PairValue.gbp, PairValue.jpy)),
        Pair(id=3, name="USDJPY", values=(PairValue.usd, PairValue.jpy)),
        Pair(id=4, name="USDGBP", values=(PairValue.usd, PairValue.gbp))
    ]
    return pairs


# -----[ Endpoints ]-----

@app.get("/", response_model=list[Pair])
async def get_pairs():
    return await get_all_pairs()
