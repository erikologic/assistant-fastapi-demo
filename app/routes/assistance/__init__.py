from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.routes.assistance.service import (
    AssistanceRequest,
    AssistantRequestDispatcher,
    ExternalError,
    IAssistantRequestDispatcher,
    RequestError,
)


router = APIRouter(prefix="/assistance")


def get_dispatcher() -> IAssistantRequestDispatcher:
    return AssistantRequestDispatcher(channels={})


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_assistance_notification(
    request: AssistanceRequest,
    dispatcher: Annotated[IAssistantRequestDispatcher, Depends(get_dispatcher)],
):
    try:
        await dispatcher.notify(request)
    except RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ExternalError as e:
        raise HTTPException(status_code=503, detail=str(e))
