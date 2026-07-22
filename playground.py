import asyncio
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from app.mcp.tool_registry import (
    ToolDefinition,
    ToolRegistry
)
from app.mcp.tool_filter import ToolFilter
from app.config.settings import settings
from app.planner.planner import Planner
from app.prompts.builder import PromptBuilder
from app.agents.state import AgentState
from app.mcp.executor import MCPExecutor
async def main():
    registry = ToolRegistry()
    tool_filter = ToolFilter()
    builder = PromptBuilder()
    print("Connecting to GitHub MCP Server...\n")
    http_client = httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {settings.github_pat}"
        }
    )
    url = settings.github_mcp_server_url
    if url is None:
        raise ValueError("github_mcp_server_url must be set in settings")

    async with streamable_http_client(url,http_client=http_client,) as (read, write, _):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("Connected Successfully\n")
            executor = MCPExecutor(session)
            tools = await session.list_tools()

            # print("\n========== ACTION DETAILS ==========\n")
            # print(result)

            print("\n==============================")
            print("ACTIONS_GET TOOL DETAILS")
            print("==============================")

            for tool in tools.tools:
                registry.register(

                    ToolDefinition(
                        name=tool.name,
                        description=tool.description,
                        input_schema=tool.inputSchema
                    )
                )

            actions_tool = registry.get("actions_get")
            print(actions_tool)
            filtered = tool_filter.filter(
                registry.list()
            )
            print("\nFiltered Tools\n")
            for tool in filtered:
                print(tool.name)

            state = AgentState(
                goal="Fix failed GitHub Action",
                owner="amanwb",
                repository="demo-react",
                run_id="28163499398",
                available_tools=[]
            )

            prompt = builder.build(
                state,
                filtered
            )

            print(prompt)

            result = await executor.execute(
                "actions_get",
                {
                    "method": "get_workflow_run",
                    "owner": "amanwb",
                    "repo": "demo-react",
                    "resource_id": "28163499398"
                }
            )

            print(result)

if __name__ == "__main__":
    asyncio.run(main())







