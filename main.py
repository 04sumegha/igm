from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config.database import connect_to_mongo, close_mongo
from urls.test import router as test_router
from urls.issue import router as issue_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client, app.mongodb = await connect_to_mongo()
    print("Mongodb connected")
    yield
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