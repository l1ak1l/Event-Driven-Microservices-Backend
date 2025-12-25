from fastapi import FastAPI, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from database import init_db, get_session
from models import Order
from producer import send_order_created, get_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # No explicit shutdown for producer handled here for simplicity, 
    # but good practice to stop it. app.state could be used.

app = FastAPI(title="Order Service", lifespan=lifespan)

@app.post("/orders", response_model=Order)
async def create_order(order: Order, session: AsyncSession = Depends(get_session)):
    session.add(order)
    await session.commit()
    await session.refresh(order)
    
    # Publish event
    order_dict = order.dict()
    await send_order_created(order_dict)
    
    return order
