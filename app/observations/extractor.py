import json


def extract_observation(result) -> str:
    """
    Extract a short, readable observation from an MCP tool result.

    This helper is currently designed for the `actions_get`
    tool response only.

    Later, when we support more tools, we can refactor this
    into a proper observation framework.
    """

    try:
        # MCP returns a list of content blocks.
        if not result.content:
            return "No content returned from MCP tool."

        # First content block contains JSON as text.
        raw_json = result.content[0].text

        # Convert JSON string into Python dictionary.
        data = json.loads(raw_json)

        workflow_name = data.get("name", "Unknown")
        status = data.get("status", "Unknown")
        conclusion = data.get("conclusion", "Unknown")
        workflow_file = data.get("path", "Unknown")

        logs_available = "Yes" if data.get("logs_url") else "No"
        jobs_available = "Yes" if data.get("jobs_url") else "No"

        observation = f"""
Workflow Name : {workflow_name}
Status        : {status}
Conclusion    : {conclusion}
Workflow File : {workflow_file}
Logs Available: {logs_available}
Jobs Available: {jobs_available}
"""

        return observation.strip()

    except json.JSONDecodeError:
        return "Failed to parse MCP response."

    except Exception as e:
        return f"Observation extraction failed: {str(e)}"