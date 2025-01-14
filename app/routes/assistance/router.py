from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.middlewares.auth import VerifyToken
from app.routes.assistance.channels.mail import MailChannel
from app.routes.assistance.channels.slack import SlackChannel
from app.routes.assistance.models import (
    AssistanceRequest,
    ExternalError,
    IAssistantRequestDispatcher,
    RequestError,
)
from app.routes.assistance.service import (
    AssistantRequestDispatcher,
)


router = APIRouter(prefix="/assistance")

auth = VerifyToken()

SALES_SLACK_CHANNEL = "C088LDVP40K"


def get_dispatcher() -> IAssistantRequestDispatcher:
    return AssistantRequestDispatcher(
        # TODO read from elsewhere
        channels={
            "Sales": SlackChannel(channel=SALES_SLACK_CHANNEL),
            "Pricing": MailChannel(),
        }
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_assistance_notification(
    request: AssistanceRequest,
    dispatcher: Annotated[IAssistantRequestDispatcher, Depends(get_dispatcher)],
    auth_result=Security(auth.verify, scopes=["request-assistance"]),
):
    try:
        await dispatcher.notify(request)
    except RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ExternalError as e:
        raise HTTPException(status_code=503, detail=str(e))
