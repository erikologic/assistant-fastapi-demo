from fastapi import APIRouter, status

router = APIRouter()

@router.get("/heartbeat", status_code=status.HTTP_204_NO_CONTENT)
async def heartbeat():
    return None 