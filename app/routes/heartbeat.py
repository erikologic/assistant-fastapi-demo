from fastapi import APIRouter, Security, status

from app.middlewares.auth import VerifyToken


router = APIRouter(prefix="/heartbeat")

auth = VerifyToken()


@router.get("", status_code=status.HTTP_204_NO_CONTENT)
async def heartbeat():
    return None


@router.get("/private", status_code=status.HTTP_204_NO_CONTENT)
async def private(auth_result=Security(auth.verify)):
    return None


@router.get("/scoped", status_code=status.HTTP_204_NO_CONTENT)
async def scoped(auth_result=Security(auth.verify, scopes=["ping"])):
    return None
