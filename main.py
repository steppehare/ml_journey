from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from json import dumps


app = FastAPI()


class Pair(BaseModel):
    id: int
    name: str
    date_time: str
    open: float
    high: float
    low: float
    close: float

engine = create_async_engine(
    "sqlite+aiosqlite:///data.sqlite",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
sessionmaker = async_sessionmaker(engine)

async def get_pair(id: int) -> Pair | None:
    async with sessionmaker() as session:
        result = await session.execute(text("SELECT * FROM historical_data WHERE id = :id"), {"id": id})
        raw_pair = result.fetchone()
        await session.commit()
        if not raw_pair:
            return None
    return Pair(**raw_pair._asdict())


# -----[ Endpoints ]-----

@app.get("/", status_code=200)
async def get_pairs() -> list:
    pairs = None
    async with sessionmaker() as session:
        result = await session.execute(text("SELECT * FROM historical_data"))
        raw_pairs = result.fetchall()
        await session.commit()
        pairs = [Pair(**c_pair._asdict()) for c_pair in raw_pairs]
        print(f"Pairs: {pairs}")
    return pairs

@app.get("/pair/{id}", status_code=200)
async def get_pair_by_id(id: int) -> str:
    if id <= 0:
        raise HTTPException(status_code=400, detail="Id must be greater than 0")
    pair = await get_pair(id)
    if not pair:
        raise HTTPException(status_code=404, detail=f"Item not found by id {id}")
    return pair.model_dump_json()

@app.put("/pair", status_code=200)
async def update_pair(pair: Pair) -> str:
    async with sessionmaker() as session:
        await session.execute(text("UPDATE historical_data SET name = :name, date_time = :date_time, open = :open, high = :high, low = :low, close = :close WHERE id = :id"),
                              {"id": pair.id, "name": pair.name, "date_time": pair.date_time, "open": pair.open, "high": pair.high, "low": pair.low, "close": pair.close})
        await session.commit()
    return f"Pair with id {pair.id} was updated"

@app.delete("/pair/{id}", status_code=204)
async def delete_pair(id: int) -> None:
    if id <= 0:
        raise HTTPException(status_code=400, detail="Id must be greater than 0")
    res = await get_pair(id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Item not found by id {id}")
    # Delete item by ID
    async with sessionmaker() as session:
        await session.execute(text("DELETE FROM historical_data WHERE id = :id"), {"id": id})
        await session.commit()

@app.post("/pair", status_code=201)
async def create_pair(pair: Pair) -> str:
    print(f"Creating pair {pair.name}")
    async with sessionmaker() as session:
        await session.execute(text("INSERT INTO historical_data (name, date_time, open, high, low, close) VALUES (:name, :date_time, :open, :high, :low, :close)"), 
                              {"name": pair.name, "date_time": pair.date_time, "open": pair.open, "high": pair.high, "low": pair.low, "close": pair.close})
        await session.commit()
    return f"Pair {pair.name} was created"

@app.post("/pairs", status_code=201)
async def create_pairs(pairs: list[Pair]) -> str:
    async with sessionmaker() as session:
        for pair in pairs:
            await session.execute(text("INSERT INTO historical_data (name, date_time, open, high, low, close) VALUES (:name, :date_time, :open, :high, :low, :close)"), 
                                      {"name": pair.name, "date_time": pair.date_time, "open": pair.open, "high": pair.high, "low": pair.low, "close": pair.close})
        await session.commit()
    return f"Pairs were created"
