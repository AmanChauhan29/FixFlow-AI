from openai import AsyncOpenAI

from app.config.settings import settings


class   LLMClient:

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = "google/gemma-4-26b-a4b-it"
    async def ask(
        self,
        system_prompt: str,
        user_prompt: str
    ):

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format={
                "type": "json_object"
            }
        )

        return response.choices[0].message.content