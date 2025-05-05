import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://sumeghagupta455:sumeghagupta@cluster0.hu9qblj.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = "igm"
MIN_POOL_SIZE = 1

async def connect_to_mongo():
    client = AsyncIOMotorClient(MONGODB_URL, MIN_POOL_SIZE)
    db = client[DB_NAME]
    return client, db

async def close_mongo(client):
    client.close()