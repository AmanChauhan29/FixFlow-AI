from fastapi import APIRouter, Request
from app.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from app.mcp.manager import mcp_manager
router = APIRouter(
    prefix="/webhooks/github",
    tags=["GitHub Webhooks"],
)


@router.post("")
async def github_webhook(request: Request):
    """
    Receives GitHub webhook events.
    """
    
    payload = await request.json()
    orchestrator = WorkflowOrchestrator(executor=mcp_manager.get_executor(),available_tools=mcp_manager.get_filtered_tools())
    print(payload)
    await orchestrator.handle_github_workflow(payload)

    return {
        "status": "accepted"
    }