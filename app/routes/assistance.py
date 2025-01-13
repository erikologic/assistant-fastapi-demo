import typing
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

router = APIRouter()

class AssistanceNotification(BaseModel):
    topic: str
    description: str

class AssistanceRequest(BaseModel):
    description: str

class Channel(typing.Protocol):
    def send(self, request: AssistanceRequest):
        raise NotImplementedError()

class ChannelResolver(typing.Protocol):
    def get(self, topic: str) -> Channel:
        raise NotImplementedError()

def get_channel_resolver() -> ChannelResolver:
    return ChannelResolver()

@router.post("/assistance", status_code=status.HTTP_201_CREATED)
async def create_assistance_notification(notification: AssistanceNotification, channel_resolver: typing.Annotated[ChannelResolver, Depends(get_channel_resolver)]):
    channel = channel_resolver.get(notification.topic)
    channel.send(AssistanceRequest(description=notification.description))
    return channel
    