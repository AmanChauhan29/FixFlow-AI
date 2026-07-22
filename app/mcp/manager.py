from app.mcp.client import MCPClient
from app.mcp.tool_registry import ToolRegistry, ToolDefinition
from app.mcp.tool_filter import ToolFilter
from app.mcp.executor import MCPExecutor


class MCPManager:

    def __init__(self):

        self.client = MCPClient()

        self.registry = ToolRegistry()

        self.tool_filter = ToolFilter()

        self.executor = None

        self.filtered_tools = []

    async def start(self):
        print("=" * 60)
        print("Initializing MCP Infrastructure")
        print("=" * 60)

        #
        # STEP-1
        # Connect to GitHub MCP
        #
        session = await self.client.connect()

        print("✓ MCP Session Ready")

        #
        # STEP-2
        # Discover available tools
        #
        tools = await session.list_tools()

        print(f"✓ Discovered {len(tools.tools)} tools")

        #
        # STEP-3
        # Populate registry
        #
        for tool in tools.tools:

            self.registry.register(
                ToolDefinition(
                    name=tool.name,
                    description=tool.description,
                    input_schema=tool.inputSchema,
                )
            )

        print(f"✓ Registered {len(self.registry.list())} tools")

        #
        # STEP-4
        # Filter tools
        #
        self.filtered_tools = self.tool_filter.filter(
            self.registry.list()
        )

        print(f"✓ Filtered {len(self.filtered_tools)} tools")

        #
        # STEP-5
        # Create executor
        #
        self.executor = MCPExecutor(session)

        print("✓ MCP Executor Ready \n")
        print("MCP Infrastructure Ready 🚀")

    def get_registry(self):
        return self.registry

    def get_executor(self):
        return self.executor

    def get_filtered_tools(self):
        return self.filtered_tools
    

mcp_manager = MCPManager()