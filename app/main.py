from fastapi import FastAPI, status

app = FastAPI()

@app.get("/heartbeat", status_code=status.HTTP_204_NO_CONTENT)
async def heartbeat():
    return None
