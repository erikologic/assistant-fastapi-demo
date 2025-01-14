from cache import AsyncTTL
from app.routes.assistance.channels.mail import MailChannel
from app.routes.assistance.channels.slack import SlackChannel
from app.routes.assistance.models import IChannel

import structlog

logger = structlog.get_logger()

SALES_SLACK_CHANNEL = "C088LDVP40K"

MOCKED_CONFIG_PAYLOAD = {
    "Sales": {
        "type": "slack",
        "channel": SALES_SLACK_CHANNEL,
    },
    "Pricing": {
        "type": "mail",
    },
}


async def mocked_fetch_conf_service():
    return MOCKED_CONFIG_PAYLOAD


class CachedChannelConfiguration:
    """
    A simple example on how to to create a class which will pull a configuration
    and cache it for a certain amount of time.
    Ideally, the fetching operation would be non-blocking e.g. using something
    like stale while revalidated (SWR) or a similar approach.

    This class is not tested for sake of time, it would probably benefit from some
    testing. I spiked it just to showcase the concept.
    This could be unrequired, or there could be other ways to achieve the same
    result, e.g. push-based, by having a webhook to notify when the configuration
    changes, or by having a POST endpoint receiving the configuration.
    """

    async def get(self, topic):
        channels = await self._fetch_conf()
        if topic not in channels:
            return None

        return channels[topic]

    @AsyncTTL(time_to_live=60)
    async def _fetch_conf(self) -> dict[str, IChannel]:
        logger.info("Fetching configuration")
        payload = await mocked_fetch_conf_service()
        conf = {}
        for topic, data in payload.items():
            if data["type"] == "slack":
                conf[topic] = SlackChannel(channel=data["channel"])
            elif data["type"] == "mail":
                conf[topic] = MailChannel()
        return conf
