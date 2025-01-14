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
    async def notify(self, request: AssistanceRequest) -> None:
        raise NotImplementedError()


class IChannel(Protocol):
    async def send(self, notification: Notification) -> None:
        raise NotImplementedError()


class IChannelsConfiguration(Protocol):
    async def get(self, topic: str) -> IChannel | None:
        raise NotImplementedError()
