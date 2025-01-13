import typing
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

router = APIRouter()


class Body(BaseModel):
    topic: str
    description: str


class Notification(BaseModel):
    description: str


class Channel(typing.Protocol):
    def send(self, request: Notification):
        raise NotImplementedError()


ChannelsLookup = typing.Dict[str, Channel]


def channels() -> ChannelsLookup:
    return {}


@router.post("/assistance", status_code=status.HTTP_201_CREATED)
async def create_assistance_notification(
    body: Body,
    channels: typing.Annotated[ChannelsLookup, Depends(channels)],
):
    channel = channels.get(body.topic)
    channel.send(Notification(description=body.description))
    return channel
