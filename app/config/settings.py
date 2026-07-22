from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded automatically from environment variables.
    """
    # Just declare the types and optional default values. 
    # Pydantic will look for "APP_NAME", "GITHUB_MCP_SERVER_URL", etc. in your .env file automatically.
    app_name: Optional[str] = None
    github_mcp_server_url: str = "https://api.githubcopilot.com/mcp/x/all"
    github_pat: str = ""
    openrouter_api_key: Optional[str] = None

    # If a variable is optional and can be missing/None, use Optional or | None:
    # github_pat: Optional[str] = None 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore" # Good practice to ignore extra env vars
    )

# This will automatically read your .env file now!
settings = Settings()