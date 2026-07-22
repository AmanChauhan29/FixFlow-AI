from app.agents import state
from app.agents.state import AgentState
from app.mcp.tool_registry import ToolDefinition


class PromptBuilder:
    """
    LLM ke liye prompt banata hai.
    """

    def build(
        self,
        state: AgentState,
        tools: list[ToolDefinition]
    ) -> str:

        prompt = f"""
    Goal

    {state.goal}

    Repository

    {state.owner}/{state.repository}

    Run ID

    {state.run_id}

    Previous Tool Executions

    """

        if not state.history:

            prompt += "None\n"

        else:

            for item in state.history:

                prompt += f"""

    ----------------------------------------

    Thought

    {item["thought"]}

    Tool

    {item["tool"]}

    Arguments

    {item["arguments"]}

    Result

    {item["result"]}

    """

        prompt += """

    IMPORTANT

    Use ONLY the tool names listed above.

    Never invent tool names.

    If a tool supports multiple methods,
    keep the tool name unchanged
    and put the selected method
    inside the arguments object.

    Return ONLY valid JSON.

    Do not wrap JSON inside markdown.

    Available MCP Tools

    """

        for tool in tools:

            prompt += f"""

    Tool Name

    {tool.name}

    Description

    {tool.description}

    Input Schema

    {tool.input_schema}

    """

        return prompt