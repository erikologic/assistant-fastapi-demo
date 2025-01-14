from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from app.config import get_settings
from app.routes.assistance.models import ExternalError, Notification


class SlackChannel:
    """
    This class can send a notification to a Slack channel.
    It requires inviting the bot to the channel before it can send messages.
    """

    def __init__(self, channel: str):
        self.config = get_settings()
        self.client = AsyncWebClient(token=self.config.slack_token)
        self.channel = channel

    async def send(self, notification: Notification) -> None:
        try:
            await self.client.chat_postMessage(
                channel=self.channel,
                text=f"New assistance request: {notification.description}",
            )
        except SlackApiError as e:
            # TODO improve logging
            print(str(e))
            print(e.__class__.__name__)
            raise ExternalError(f"Failed to send message to Slack: {str(e)}")
