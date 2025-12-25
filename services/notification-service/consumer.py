import json
from aiokafka import AIOKafkaConsumer
from config import KAFKA_BOOTSTRAP_SERVERS, INVENTORY_UPDATED_TOPIC
from database import engine, get_session
from models import NotificationLog
from sqlalchemy.ext.asyncio import AsyncSession

async def consume_inventory_updates():
    consumer = AIOKafkaConsumer(
        INVENTORY_UPDATED_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="notification-group"
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
            print(f"Received inventory update: {data}")
            
            # Create notification
            async with AsyncSession(engine) as session:
                log = NotificationLog(
                    order_id=data.get("order_id"),
                    content=f"Order {data.get('order_id')} confirmed, stock reserved."
                )
                session.add(log)
                await session.commit()
                print(f"Notification sent/logged for Order {data.get('order_id')}")
    finally:
        await consumer.stop()
