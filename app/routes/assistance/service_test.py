from unittest.mock import AsyncMock
import pytest

from app.routes.assistance.models import (
    AssistanceRequest,
    ExternalError,
    Notification,
    RequestError,
)
from app.routes.assistance.service import (
    AssistantRequestDispatcher,
)


@pytest.mark.asyncio
async def test_create_sales_assistance_notification():
    # arrange
    sales_channel = AsyncMock()
    dispatcher = AssistantRequestDispatcher(channels={"Sales": sales_channel})

    # act
    request = AssistanceRequest(
        topic="Sales",
        description="I need help with my order #12345",
    )
    await dispatcher.notify(request)

    # assert
    sales_channel.send.assert_called_once_with(
        Notification(description="I need help with my order #12345")
    )


@pytest.mark.asyncio
async def test_can_route_notifications():
    # arrange
    channels = {
        "Sales": AsyncMock(),
        "Pricing": AsyncMock(),
    }
    dispatcher = AssistantRequestDispatcher(channels=channels)

    # act
    request = AssistanceRequest(
        topic="Pricing",
        description="I need help with my order #12345",
    )
    await dispatcher.notify(request)

    # assert
    channels["Pricing"].send.assert_called_once_with(
        Notification(description="I need help with my order #12345")
    )
    channels["Sales"].send.assert_not_called()


@pytest.mark.asyncio
async def test_create_assistance_notification_invalid_topic():
    # arrange
    dispatcher = AssistantRequestDispatcher(channels={})

    # act
    request = AssistanceRequest(
        topic="Invalid",
        description="I need help with my order #12345",
    )

    # assert
    with pytest.raises(RequestError) as exc_info:
        await dispatcher.notify(request)

    assert str(exc_info.value) == "Invalid topic"


@pytest.mark.asyncio
async def test_failing_channel():
    # arrange
    failing_channel = AsyncMock()
    failing_channel.send.side_effect = Exception("The underlying API request failed")
    dispatcher = AssistantRequestDispatcher(channels={"Failing": failing_channel})

    # act
    request = AssistanceRequest(
        topic="Failing",
        description="I need help with my order #12345",
    )

    # assert
    with pytest.raises(ExternalError) as exc_info:
        await dispatcher.notify(request)

    assert str(exc_info.value) == "Failed to send the notification"
