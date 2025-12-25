import json
from aiokafka import AIOKafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, ORDER_TOPIC

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        # Simple retry logic inline to avoid relative import complexities with shared_utils if not packaged
        import asyncio
        for i in range(10):
            try:
                await producer.start()
                break
            except Exception as e:
                print(f"Waiting for Kafka... ({e})")
                await asyncio.sleep(2)
    return producer

async def send_order_created(order_data: dict):
    kafka_producer = await get_producer()
    message = json.dumps(order_data).encode("utf-8")
    await kafka_producer.send_and_wait(ORDER_TOPIC, message)
