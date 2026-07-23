from app.mcp.result_formatter import extract_tool_payload
from app.agents.agent import AIAgent
from app.agents.state import AgentState
from app.actions.action_engine import ActionEngine


class WorkflowOrchestrator:
    """
    Coordinates the lifecycle of a CI/CD incident.

    Responsibilities:
    - Ask the LLM what to do.
    - Execute MCP tools.
    - Store observations.
    - Stop when goal is completed.
    """

    def __init__(self, executor, available_tools):
        self.agent = AIAgent()
        self.executor = executor
        self.available_tools = available_tools
        self.action_engine = ActionEngine(executor)

    async def _execute_iteration(self, state: AgentState):
        """
        Executes one Think -> Validate -> Act -> Observe cycle.
        """

        decision = await self.agent.think(state)

        print()
        print("=" * 60)
        print("LLM DECISION")
        print("=" * 60)
        print(decision)

        # -------------------------------
        # Validate LLM response
        # -------------------------------

        if not isinstance(decision, dict):
            raise ValueError(
                f"LLM returned invalid response: {decision}"
            )

        tool_name = decision.get("tool")
        arguments = decision.get("arguments", {})

        # If the goal is complete OR there is no tool,
        # simply return the decision.
        if decision.get("goal_completed", False):
            return decision

        if not tool_name:
            return decision

        print()
        print("=" * 60)
        print("EXECUTING MCP TOOL")
        print("=" * 60)
        print(tool_name)

        result = await self.action_engine.execute(
            decision,
            state,
        )

        payload = extract_tool_payload(result)

        state.add_history(
            thought=decision.get("thought", ""),
            tool=tool_name,
            arguments=arguments,
            result=payload,
        )

        return decision

    async def handle_github_workflow(self, payload: dict):

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
            available_tools=self.available_tools,
        )

        MAX_STEPS = 10

        for step in range(MAX_STEPS):

            print()
            print("=" * 60)
            print(f"ITERATION {step + 1}")
            print("=" * 60)

            try:
                decision = await self._execute_iteration(state)

            except Exception as e:

                print()
                print("=" * 60)
                print("ITERATION FAILED")
                print("=" * 60)
                print(e)

                raise

            if decision.get("goal_completed", False):
                print()
                print("Goal Completed ✅")
                break

            if not decision.get("tool"):
                print()
                print("No More Tools")
                break

        else:
            print()
            print("=" * 60)
            print("Maximum iterations reached.")
            print("=" * 60)