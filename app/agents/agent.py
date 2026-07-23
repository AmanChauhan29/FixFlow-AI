import json
import re
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
        print("=" * 80)
        print("RAW LLM RESPONSE")
        print("=" * 80)
        print(repr(response))
        print("=" * 80)
        if response is None:
            raise RuntimeError(
                "LLM returned no response."
            )
        
        response = response.strip()

        # Remove markdown code fences if present
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

        # Extract the first JSON object
        match = re.search(r"\{.*\}", response, re.DOTALL)

        if not match:
            raise RuntimeError(
                f"No valid JSON found in LLM response:\n{response}"
            )

        json_text = match.group()

        print("=" * 80)
        print("JSON EXTRACTED")
        print("=" * 80)
        print(json_text)
        print("=" * 80)

        try:
            decision = json.loads(json_text)
        except json.JSONDecodeError as e:
            print("=" * 80)
            print("FAILED TO PARSE JSON")
            print("=" * 80)
            print(json_text)
            raise RuntimeError(f"Invalid JSON returned by LLM: {e}")

        return decision