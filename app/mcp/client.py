import httpx

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from app.config.settings import settings


class MCPClient:

    def __init__(self):

        self.session: ClientSession | None = None

        self.http_client: httpx.AsyncClient | None = None

        self._connection = None

    async def connect(self) -> ClientSession:

        if self.session is not None:
            return self.session

        self.http_client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {settings.github_pat}"
            }
        )

        self._connection = streamable_http_client(
            settings.github_mcp_server_url,
            http_client=self.http_client,
        )

        read, write, _ = await self._connection.__aenter__()

        self.session = ClientSession(read, write)

        await self.session.__aenter__()

        await self.session.initialize()

        print("✅ Connected to GitHub MCP")

        return self.session

    async def close(self):

        if self.session is not None:
            await self.session.__aexit__(None, None, None)

        if self._connection is not None:
            await self._connection.__aexit__(None, None, None)

        if self.http_client is not None:
            await self.http_client.aclose()