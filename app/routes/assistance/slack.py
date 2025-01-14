from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from app.config import get_settings
from app.routes.assistance.models import AssistanceRequest, ExternalError


class SlackChannel:
    def __init__(self, channel: str):
        self.config = get_settings()
        self.client = AsyncWebClient(token=self.config.slack_token)
        self.channel = channel

    async def send(self, request: AssistanceRequest) -> None:
        try:
            await self.client.chat_postMessage(
                channel=self.channel,
                text=f"New assistance request: {request.description}",
            )
        except SlackApiError as e:
            # TODO improve logging
            print(str(e))
            print(e.__class__.__name__)
            raise ExternalError(f"Failed to send message to Slack: {str(e)}")
