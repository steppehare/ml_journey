from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


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

# engine = create_async_engine("sqlite+aiosqlite:///database.db")

# async with async_sessionmaker(engine) as session:
#     await session.execute("CREATE TABLE IF NOT EXISTS pairs (id INTEGER PRIMARY KEY, name TEXT, values TEXT)")
#     await session.commit()


async def get_all_pairs() -> list[Pair]:
    # TODO: fix fake async function with real DB data
    pairs = [
        Pair(id=1, name="EURUSD", values=(PairValue.eur, PairValue.usd)),
        Pair(id=2, name="GBPJPY", values=(PairValue.gbp, PairValue.jpy)),
        Pair(id=3, name="USDJPY", values=(PairValue.usd, PairValue.jpy)),
        Pair(id=4, name="USDGBP", values=(PairValue.usd, PairValue.gbp))
    ]
    return pairs

async def get_pair(id: int) -> Pair | None:
    # TODO: fix function to get all data from real DB
    pairs = await get_all_pairs()
    pair = None
    for cur_pair in pairs:
        if cur_pair.id == id:
            pair = cur_pair
    return pair


# -----[ Endpoints ]-----

@app.get("/", status_code=200)
async def get_pairs() -> list:
    return await get_all_pairs()

@app.get("/pairs/{id}", status_code=200)
async def get_pair_by_id(id: int) -> str:
    if id <= 0:
        raise HTTPException(status_code=400, detail="Id must be greater than 0")
    pair = await get_pair(id)
    if not pair:
        raise HTTPException(status_code=404, detail=f"Item not found by id {id}")
    return f"Pair with id {id} was found"

@app.put("/pairs/{id}", status_code=200)
async def update_pair(id: int) -> str:
    return f"Pair with id {id} was updated"

@app.delete("/pairs/{id}", status_code=204)
async def delete_pair(id: int) -> None:
    pass
    # return f"Pair with id {id} was deleted"

@app.post("/pairs", status_code=201)
async def create_pair(pair: Pair) -> str:
    return f"Pair {pair.name} was created"
