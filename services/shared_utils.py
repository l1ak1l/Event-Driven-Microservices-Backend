import asyncio
from aiokafka.errors import KafkaConnectionError, KafkaError

async def retry_kafka_connect(connect_func, retries=5, delay=2):
    for i in range(retries):
        try:
            return await connect_func()
        except (KafkaConnectionError, KafkaError, OSError) as e:
            print(f"B Connection failed: {e}. Retrying {i+1}/{retries}...")
            await asyncio.sleep(delay)
    raise Exception("Could not connect to Kafka after multiple retries")
