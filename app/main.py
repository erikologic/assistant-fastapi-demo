from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class AssistanceRequest(BaseModel):
    topic: str
    description: str

@app.get("/heartbeat", status_code=status.HTTP_204_NO_CONTENT)
async def heartbeat():
    return None

@app.post("/assistance", status_code=status.HTTP_204_NO_CONTENT)
async def request_assistance(request: AssistanceRequest):
    return None
