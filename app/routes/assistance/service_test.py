import pytest

from app.routes.assistance.service import (
    AssistanceRequest,
    AssistantRequestDispatcher,
    Notification,
)


class InMemoryChannel:
    def __init__(self):
        self.notifications = []

    async def send(self, notification: Notification):
        self.notifications.append(notification)


@pytest.mark.asyncio
async def test_create_sales_assistance_notification():
    # arrange
    sales_channel = InMemoryChannel()
    dispatcher = AssistantRequestDispatcher(channels={"Sales": sales_channel})

    # act
    request = AssistanceRequest(
        topic="Sales",
        description="I need help with my order #12345",
    )
    await dispatcher.notify(request)

    # assert
    assert sales_channel.notifications == [
        Notification(description="I need help with my order #12345")
    ]


@pytest.mark.asyncio
async def test_can_route_notifications():
    # arrange
    channels = {
        "Sales": InMemoryChannel(),
        "Pricing": InMemoryChannel(),
    }
    dispatcher = AssistantRequestDispatcher(channels=channels)

    # act
    request = AssistanceRequest(
        topic="Pricing",
        description="I need help with my order #12345",
    )
    await dispatcher.notify(request)

    # assert
    assert channels["Pricing"].notifications == [
        Notification(description="I need help with my order #12345")
    ]


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
    with pytest.raises(ValueError) as exc_info:
        await dispatcher.notify(request)

    assert str(exc_info.value) == "Invalid topic"
