from app.mcp.tool_registry import ToolDefinition


class ToolFilter:
    """
    Sirf relevant MCP tools LLM ko dega.
    """

    DEFAULT_TOOLS = {
        "actions_get",
        "get_job_logs",
        "get_file_contents",
        "create_branch",
        "create_or_update_file",
        "create_pull_request",
        "actions_run_trigger"
    }

    def filter(
        self,
        tools: list[ToolDefinition]
    ) -> list[ToolDefinition]:

        return [
            tool
            for tool in tools
            if tool.name in self.DEFAULT_TOOLS
        ]