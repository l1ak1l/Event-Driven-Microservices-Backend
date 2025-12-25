import json
from aiokafka import AIOKafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, INVENTORY_UPDATED_TOPIC

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        import asyncio
        for i in range(10):
            try:
                await producer.start()
                break
            except Exception as e:
                print(f"Waiting for Kafka... ({e})")
                await asyncio.sleep(2)
    return producer

async def send_inventory_updated(data: dict):
    kafka_producer = await get_producer()
    message = json.dumps(data).encode("utf-8")
    await kafka_producer.send_and_wait(INVENTORY_UPDATED_TOPIC, message)
