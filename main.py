from fastapi import FastAPI, APIRouter
from app.api.webhook import router as webhook
from app.config.settings import settings
from app.mcp.manager import mcp_manager

app = FastAPI(
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    """
    await mcp_manager.start()

@app.on_event("shutdown")
async def shutdown():
    await mcp_manager.client.close()

@app.get("/")
def health_check():
    """
    Basic health endpoint.
    """
    return {
        "status": "healthy",
        "application": settings.app_name,
    }

app.include_router(webhook)