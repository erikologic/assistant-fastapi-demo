from app.routes.assistance.models import (
    AssistanceRequest,
    ExternalError,
    Notification,
    RequestError,
)


class AssistantRequestDispatcher:
    def __init__(self, channels):
        self.channels = channels

    async def notify(self, request: AssistanceRequest):
        channel = self.channels.get(request.topic)
        if channel is None:
            raise RequestError("Invalid topic")

        try:
            await channel.send(Notification(description=request.description))
        except Exception:
            raise ExternalError("Failed to send the notification")
