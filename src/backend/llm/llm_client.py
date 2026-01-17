from typing import Optional


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        return ""
