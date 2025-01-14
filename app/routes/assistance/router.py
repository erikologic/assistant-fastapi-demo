from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.middlewares.auth import VerifyToken
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


def get_dispatcher() -> IAssistantRequestDispatcher:
    return AssistantRequestDispatcher(channels={})


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
