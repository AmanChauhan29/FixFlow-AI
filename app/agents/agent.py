import json
from app.agents.state import AgentState
from app.llm.clients import LLMClient
from app.prompts.planner_prompts import SYSTEM_PROMPT
from app.prompts.builder import PromptBuilder

class AIAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.PromptBuilder = PromptBuilder()

    async def think(
        self,
        state: AgentState
    ):
        user_prompt = self.PromptBuilder.build(state, state.available_tools)
        print("=" * 80)
        print("PROMPT SENT TO LLM")
        print("=" * 80)
        print(user_prompt)
        print("=" * 80)
        response = await self.llm.ask(
            SYSTEM_PROMPT,
            user_prompt
        )
        
        if response is None:
            raise RuntimeError(
                "LLM returned no response."
            )
        else:
            response = response.strip()
            if response.startswith("```json"):
                response = response.replace("```json", "", 1)
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            return json.loads(response)