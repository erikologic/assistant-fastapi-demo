from app.routes.assistance.models import (
    AssistanceRequest,
    ExternalError,
    IChannelsConfiguration,
    Notification,
    RequestError,
)

class AssistantRequestDispatcher:
    """
    This class is the internal Interactor that will handle the notification request.
    It will get from ChannelConfiguration the channel to send the notification to it.
    """
    def __init__(self, channels_configuration: IChannelsConfiguration):
        self.channels_configuration = channels_configuration

    async def notify(self, request: AssistanceRequest):
        channel = await self.channels_configuration.get(request.topic)
        if channel is None:
            raise RequestError("Invalid topic")

        try:
            await channel.send(Notification(description=request.description))
        except Exception:
            raise ExternalError("Failed to send the notification")
