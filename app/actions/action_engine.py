from app.mcp.executor import MCPExecutor


class ActionEngine:

    def __init__(self, executor: MCPExecutor):
        self.executor = executor
        
    async def execute(
        self,
        decision: dict,
        state
    ):
        tool = decision["tool"]
        arguments = decision["arguments"]

        # V1
        # Abhi direct execute karenge.
        # Safety rules next commit mein add karenge.

        return await self.executor.execute(
            tool,
            arguments
        )