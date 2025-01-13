from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class AssistanceNotification(BaseModel):
    topic: str
    description: str

@router.post("/assistance", status_code=status.HTTP_201_CREATED)
async def create_assistance_notification(notification: AssistanceNotification):
    return None