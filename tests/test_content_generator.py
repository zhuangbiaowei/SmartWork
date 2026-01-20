import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from llm.llm_client import LLMClient
from llm.content_generator import ContentGenerator


class MockLLMClient(LLMClient):
    """Mock LLM client for testing."""

    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        return f"Mock response for: {prompt[:50]}"


class TestLLMClient:
    """Test LLM client."""

    @pytest.mark.asyncio
    async def test_generate_without_api_key(self):
        """Test generation fails without API key."""
        client = LLMClient(api_key=None)

        result = await client.generate("test prompt")
        assert result is not None
        assert "Error" in result

    @pytest.mark.asyncio
    async def test_generate_with_mock(self):
        """Test generation with mock client."""
        client = MockLLMClient()

        result = await client.generate("test prompt")

        assert result is not None
        assert "Mock response" in result
        assert "test prompt" in result

    def test_set_api_key(self):
        """Test setting API key."""
        client = LLMClient(api_key=None)

        assert client.api_key is None

        client.set_api_key("test-key-123")
        assert client.api_key == "test-key-123"

    def test_set_model(self):
        """Test setting model."""
        client = LLMClient(model="gpt-3.5-turbo")

        assert client.model == "gpt-3.5-turbo"

        client.set_model("gpt-4")
        assert client.model == "gpt-4"


class TestContentGenerator:
    """Test content generator."""

    @pytest.mark.asyncio
    async def test_generate_report(self):
        """Test report generation."""
        mock_client = MockLLMClient()
        generator = ContentGenerator(mock_client)

        result = await generator.generate_report(
            "销售分析", {"january": 1000, "february": 1200}
        )

        assert result is not None
        assert "Mock response" in result
        assert "销售分析" in result

    @pytest.mark.asyncio
    async def test_generate_summary(self):
        """Test summary generation."""
        mock_client = MockLLMClient()
        generator = ContentGenerator(mock_client)

        long_content = (
            "This is a very long piece of content that needs to be summarized. " * 20
        )

        result = await generator.generate_summary(long_content)

        assert result is not None
        assert "Mock response" in result

    @pytest.mark.asyncio
    async def test_generate_email(self):
        """Test email generation."""
        mock_client = MockLLMClient()
        generator = ContentGenerator(mock_client)

        result = await generator.generate_email(
            "张三",
            "项目进度汇报",
            ["项目已完成80%", "剩余2周"],
        )

        assert result is not None
        assert "Mock response" in result
        assert "张三" in result

    @pytest.mark.asyncio
    async def test_generate_meeting_agenda(self):
        """Test meeting agenda generation."""
        mock_client = MockLLMClient()
        generator = ContentGenerator(mock_client)

        result = await generator.generate_meeting_agenda(
            "项目评审会",
            ["张三", "李四", "王五"],
            60,
        )

        assert result is not None
        assert "Mock response" in result
        assert "项目评审会" in result
