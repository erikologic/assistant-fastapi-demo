from fastapi import FastAPI
from app.routes.heartbeat import router as heartbeat_router

app = FastAPI()

app.include_router(heartbeat_router)
