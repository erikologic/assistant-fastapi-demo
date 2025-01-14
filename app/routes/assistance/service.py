from pydantic import BaseModel


class Notification(BaseModel):
    description: str


class AssistanceRequest(BaseModel):
    topic: str
    description: str


class AssistantRequestDispatcher:
    def __init__(self, channels):
        self.channels = channels

    async def notify(self, request: AssistanceRequest):
        channel = self.channels.get(request.topic)
        if channel is None:
            raise ValueError("Invalid topic")

        await channel.send(Notification(description=request.description))
