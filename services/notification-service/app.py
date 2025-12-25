import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import init_db
from consumer import consume_inventory_updates

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    loop = asyncio.get_event_loop()
    task = loop.create_task(consume_inventory_updates())
    yield

app = FastAPI(title="Notification Service", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}
