import typing
from fastapi import APIRouter, Depends, HTTPException, status

from app.routes.assistance.models import Body
from app.routes.assistance.models import Notification
from app.routes.assistance.models import ChannelsLookup

router = APIRouter(prefix="/assistance")


def channels() -> ChannelsLookup:
    return {}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_assistance_notification(
    body: Body,
    channels: typing.Annotated[ChannelsLookup, Depends(channels)],
):
    channel = channels.get(body.topic)
    if channel is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid topic",
        )

    try:
        await channel.send(Notification(description=body.description))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to send the notification",
        )
    return channel
