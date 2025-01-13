from fastapi import APIRouter, status

router = APIRouter(prefix="/heartbeat")


@router.get("/", status_code=status.HTTP_204_NO_CONTENT)
async def heartbeat():
    return None
