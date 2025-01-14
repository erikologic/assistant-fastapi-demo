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
    """
    This test will create a notification for the Sales channel.
    """
    # arrange
    sales_channel = AsyncMock()
    channels_configuration = AsyncMock()
    channels_configuration.get.side_effect = [sales_channel]
    dispatcher = AssistantRequestDispatcher(channels_configuration)

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
async def test_create_assistance_notification_invalid_topic():
    """
    This test will simulate a request with an invalid topic requested getting a 400 response and an error message.
    """
    # arrange
    channels_configuration = AsyncMock()
    channels_configuration.get.side_effect = [None]
    dispatcher = AssistantRequestDispatcher(channels_configuration)

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
async def test_can_route_notifications():
    """
    This test showcase how to create a simple routing mechanism for notifications.
    """
    # arrange
    channels = {
        "Sales": AsyncMock(),
        "Pricing": AsyncMock(),
    }

    class MockedChannelsConfiguration:
        """ A quick implementation of IChannelsConfiguration """
        async def get(self, topic):
            return channels.get(topic)

    dispatcher = AssistantRequestDispatcher(MockedChannelsConfiguration())

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
async def test_failing_channel():
    """
    This test simulate a request that fails because of the underlying service.
    """
    # arrange
    failing_channel = AsyncMock()
    failing_channel.send.side_effect = Exception("The underlying API request failed")
    channels_configuration = AsyncMock()
    channels_configuration.get.side_effect = [failing_channel]
    dispatcher = AssistantRequestDispatcher(channels_configuration)

    # act
    request = AssistanceRequest(
        topic="Failing",
        description="I need help with my order #12345",
    )

    # assert
    with pytest.raises(ExternalError) as exc_info:
        await dispatcher.notify(request)

    assert str(exc_info.value) == "Failed to send the notification"


@pytest.mark.asyncio
async def test_updating_channel_conf():
    """
    This test showcase different channels being hit when configuration changes
    """
    # GIVEN an initial configuration pointing to a channel
    sales_channel = AsyncMock()
    channels_configuration = AsyncMock()
    channels_configuration.get.side_effect = [sales_channel]
    dispatcher = AssistantRequestDispatcher(channels_configuration)

    # WHEN we hit the service for a sales request
    sales_request = AssistanceRequest(
        topic="Sales",
        description="I need help with my order #12345",
    )
    await dispatcher.notify(sales_request)

    # THEN we will send the notification to the channel
    sales_channel.send.assert_called_once_with(
        Notification(description="I need help with my order #12345")
    )
    sales_channel.reset_mock()

    # GIVEN the channel configuration is updated
    new_sales_channel = AsyncMock()
    channels_configuration.get.side_effect = [new_sales_channel]

    # WHEN we hit the service for a sales request again
    await dispatcher.notify(sales_request)

    # THEN we will send the notification to the new channel
    sales_channel.send.assert_not_called()
    new_sales_channel.send.assert_called_once_with(
        Notification(description="I need help with my order #12345")
    )
