from mcp import ClientSession


class MCPExecutor:
    def __init__(self, session: ClientSession):
        self.session = session
    async def execute(
        self,
        tool_name: str,
        arguments: dict
    ):
        result = await self.session.call_tool(
            tool_name,
            arguments
        )

        return result