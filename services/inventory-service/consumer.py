import json
import asyncio
from aiokafka import AIOKafkaConsumer
from config import KAFKA_BOOTSTRAP_SERVERS, ORDER_CREATED_TOPIC
from database import engine, get_session
from models import Inventory
from producer import send_inventory_updated
from sqlmodel import select, Session
from sqlalchemy.ext.asyncio import AsyncSession

async def consume_orders():
    consumer = AIOKafkaConsumer(
        ORDER_CREATED_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="inventory-group"
    )
    async def start_consumer():
        for i in range(10):
            try:
                await consumer.start()
                return
            except Exception as e:
                print(f"Kafka consumer connection failed, retrying... {e}")
                await asyncio.sleep(2)
        raise Exception("Failed to connect to Kafka")

    await start_consumer()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            print(f"Consumed order: {data}")
            
            # Simple logic: create or update inventory
            # And then send inventory updated
            # Ideally use a session
            async with AsyncSession(engine) as session:
                 # Check if item exists (mock logic for simpler demo: just log and publish)
                 # Real logic: decrement stock
                 
                 # Publish update
                 update_data = {
                     "order_id": data.get("id"),
                     "item_id": data.get("item_id"),
                     "status": "stock_reserved"
                 }
                 await send_inventory_updated(update_data)
                 print(f"Sent inventory update: {update_data}")
    finally:
        await consumer.stop()
