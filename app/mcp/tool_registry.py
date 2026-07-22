from dataclasses import dataclass


@dataclass
class ToolDefinition:
    """
    Complete Information about MCP Tools 
    """
    name: str
    description: str | None
    input_schema: dict

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    def register(
        self,
        tool: ToolDefinition
    ):
        self.tools[tool.name] = tool

    def get(
        self,
        tool_name: str
    ):
        return self.tools.get(tool_name)

    def list(self):
        return list(self.tools.values())