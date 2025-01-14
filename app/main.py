import os
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from app import otel
from app.middlewares.logging.middleware import LoggingMiddleware
from app.routes.heartbeat import router as heartbeat_router
from app.routes.assistance.router import router as assistance_router

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)


app.include_router(heartbeat_router)
app.include_router(assistance_router)

if os.environ.get("ENABLE_OTEL") == "true":
    otel.instrument(app)
