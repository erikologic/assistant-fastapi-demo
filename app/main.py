from fastapi import FastAPI
from app.routes.heartbeat import router as heartbeat_router
from app.routes.assistance import router as assistance_router

app = FastAPI()

app.include_router(heartbeat_router)
app.include_router(assistance_router)
