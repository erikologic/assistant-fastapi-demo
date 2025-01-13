import typing
from pydantic import BaseModel


class Body(BaseModel):
    topic: str
    description: str


class Notification(BaseModel):
    description: str


class Channel(typing.Protocol):
    async def send(self, request: Notification):
        raise NotImplementedError()


ChannelsLookup = typing.Dict[str, Channel]