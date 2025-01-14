from app.routes.assistance.models import Notification


class MailChannel:
    async def send(self, notification: Notification) -> None:
        # I'm just a stub!
        print(f"Sending mail: {notification.description}")
