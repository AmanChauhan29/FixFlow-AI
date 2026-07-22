from typing import Optional

from app.config.settings import settings


class GitHubMCPClient:
    """
    Handles communication with the remote GitHub MCP server.

    This class owns:
    - MCP connection
    - Session lifecycle
    - Tool discovery
    - Tool execution

    It does NOT contain business logic.
    """

    def __init__(self) -> None:
        self._server_url = settings.github_mcp_server_url
        self._token = settings.github_pat
        self._session: Optional[object] = None