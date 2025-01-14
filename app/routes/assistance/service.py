from typing import Protocol
from pydantic import BaseModel


class Notification(BaseModel):
    description: str


class AssistanceRequest(BaseModel):
    topic: str
    description: str

class ExternalError(Exception):
    pass

class RequestError(Exception):
    pass

class IAssistantRequestDispatcher(Protocol):
    async def notify(self, request: AssistanceRequest):
        raise NotImplementedError()
    
class AssistantRequestDispatcher:
    def __init__(self, channels):
        self.channels = channels

    async def notify(self, request: AssistanceRequest):
        channel = self.channels.get(request.topic)
        if channel is None:
            raise RequestError("Invalid topic")

        try:
            await channel.send(Notification(description=request.description))
        except Exception:
            raise ExternalError("Failed to send the notification")
