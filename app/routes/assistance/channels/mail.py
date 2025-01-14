from app.routes.assistance.models import Notification


class MailChannel:
    """
    A simple example on how to create a channel which will send a notification
    """
    async def send(self, notification: Notification) -> None:
        print(f"Sending mail: {notification.description}")
