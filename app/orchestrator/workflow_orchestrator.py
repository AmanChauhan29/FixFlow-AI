from app.agents import state
from app.mcp.result_formatter import extract_tool_payload
from app.services.github_service import GitHubService
from app.agents.agent import AIAgent
from app.agents.state import AgentState
import os
from app.observations.registry import ObservationRegistry
from app.actions.action_engine import ActionEngine

class WorkflowOrchestrator:
    """
    Coordinates the complete lifecycle of a CI/CD incident.

    The orchestrator does not perform business logic itself.
    Instead, it delegates work to specialized components.
    """
    def __init__(self,executor,available_tools):
        self.agent = AIAgent()
        self.executor = executor
        self.available_tools = available_tools
        self.action_engine = ActionEngine(executor)

    async def _execute_iteration(self,state: AgentState):
        """
        Executes one complete Think -> Act -> Observe cycle.
        """
        decision = await self.agent.think(state)
        print("\n")
        print("=" * 60)
        print("LLM DECISION")
        print("=" * 60)

        print(decision)
        tool_name = decision["tool"]
        arguments = decision["arguments"]

        print()
        print("=" * 60)
        print("EXECUTING MCP TOOL")
        print("=" * 60)

        print(tool_name)

        result = await self.action_engine.execute(
            tool_name,
            arguments
        )
        payload = extract_tool_payload(result)

        state.add_history(
            thought=decision["thought"],
            tool=tool_name,
            arguments=arguments,
            result=payload
        )
        return decision


    async def handle_github_workflow(self, payload: dict) -> None:
        """
        Entry point for GitHub workflow events.
        """

        print("=" * 60)
        print("Workflow Orchestrator")
        print("=" * 60)

        workflow_name = payload.get("workflow_run", {}).get("name")

        conclusion = payload.get("workflow_run", {}).get("conclusion")

        repository = payload.get("repository", {}).get("full_name")
        owner, repo = repository.split("/")

        print(f"Repository : {repository}")
        print(f"Workflow   : {workflow_name}")
        print(f"Conclusion : {conclusion}")
        run_id = str(
            payload["workflow_run"]["id"]
        )

        state = AgentState(

            goal="Investigate and fix the failed GitHub Actions workflow.",

            owner=owner,

            repository=repo,

            run_id=run_id,

            available_tools=self.available_tools

        )
        MAX_STEPS = 5

        for step in range(MAX_STEPS):

            print()
            print("=" * 60)
            print(f"ITERATION {step + 1}")
            print("=" * 60)

            decision = await self._execute_iteration(state)

            # print()
            # print("=" * 60)
            # print("AGENT MEMORY")
            # print("=" * 60)

            if decision.get("goal_completed", False):
                print()
                print("Goal Completed ✅")
                break

            if decision.get("tool") is None:
                print()
                print("No More Tools")
                break