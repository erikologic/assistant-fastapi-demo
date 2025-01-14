import pytest
from app.routes.assistance.models import Notification
from app.routes.assistance.slack import SlackChannel


TEST_CHANNEL = "C088LDVP40K"

@pytest.mark.asyncio
async def test_slack_channel_integration():
    slack_channel = SlackChannel(channel=TEST_CHANNEL)
    await slack_channel.send(Notification(description="Test message"))