from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import close_mongo, connect_to_mongo
from urls.issue import router as issue_router
from urls.test import router as test_router
from utils.cache import cache_manager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client, app.mongodb = await connect_to_mongo()
    print("Mongodb connected")
    await cache_manager.initialize()
    yield
    await cache_manager.redis.close()
    await close_mongo(app.mongodb_client)
    print("Mongodb disconnected")

app = FastAPI(lifespan = lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(test_router)
app.include_router(issue_router)