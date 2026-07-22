from dataclasses import dataclass, field

@dataclass
class AgentState:

    goal: str
    owner: str
    repository: str
    run_id: str

    available_tools: list

    history: list[dict] = field(default_factory=list)

    goal_completed: bool = False

    def add_history(
        self,
        thought: str,
        tool: str,
        arguments: dict,
        result: str
    ):
        self.history.append(
            {
                "thought": thought,
                "tool": tool,
                "arguments": arguments,
                "result": result
            }
        )