from typing import Optional, Dict
import os


class LLMClient:
    """
    LLM client for AI model integration.

    Supports multiple providers including OpenAI-compatible APIs.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        provider: str = "openai",
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.provider = provider

    async def generate(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate response from LLM.

        Args:
            prompt: The prompt to send to LLM
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response, or None if error
        """
        if not self.api_key:
            return "Error: No API key provided"

        try:
            if self.provider == "openai":
                return await self._generate_openai(prompt, max_tokens)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            print(f"LLM generation error: {e}")
            return f"Error: {str(e)}"

    async def _generate_openai(self, prompt: str, max_tokens: int) -> str:
        """
        Generate using OpenAI API.

        Args:
            prompt: The prompt
            max_tokens: Maximum tokens

        Returns:
            Generated response
        """
        try:
            import openai

            client = openai.AsyncOpenAI(api_key=self.api_key)

            response = await client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7,
            )

            return response.choices[0].message.content
        except ImportError:
            print("OpenAI library not installed. Install with: pip install openai")
            return "Error: OpenAI client not available"
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"Error: {str(e)}"

    def set_api_key(self, api_key: str) -> None:
        """
        Update API key.

        Args:
            api_key: New API key
        """
        self.api_key = api_key

    def set_model(self, model: str) -> None:
        """
        Update model.

        Args:
            model: New model name
        """
        self.model = model
