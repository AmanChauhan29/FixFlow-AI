def extract_tool_payload(result) -> str:
    """
    Converts MCP CallToolResult into plain text for the LLM.
    """

    if not result.content:
        return ""

    parts = []

    for item in result.content:

        if hasattr(item, "text"):
            parts.append(item.text)

        else:
            parts.append(str(item))

    return "\n".join(parts)