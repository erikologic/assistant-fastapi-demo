import pytest
from app.routes.assistance.channels.slack import SlackChannel
from app.routes.assistance.models import Notification


TEST_CHANNEL = "C088LDVP40K"


@pytest.mark.asyncio
async def test_slack_channel_integration():
    """
    This test will send a message to a Slack channel.
    """
    slack_channel = SlackChannel(channel=TEST_CHANNEL)
    await slack_channel.send(Notification(description="Test message"))
