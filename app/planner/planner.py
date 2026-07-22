class Planner:

    def plan(
        self,
        goal: str,
        context: dict,
        available_tools: list[str]
    ):

        print("=" * 60)
        print("Planner Started")
        print("=" * 60)

        print(f"Goal : {goal}")

        print("\nContext")

        for key, value in context.items():
            print(f"{key} : {value}")

        print("\nAvailable Tools")

        for tool in available_tools:
            print(f"- {tool}")