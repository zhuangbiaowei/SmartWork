import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from generators.document_generator import MarkdownGenerator
from generators.pdf_generator import PDFGenerator


class TestMarkdownGenerator:
    """Test Markdown document generator."""

    @pytest.mark.asyncio
    async def test_markdown_generation(self):
        """Test generating a Markdown document."""
        generator = MarkdownGenerator()
        content = "# Test Document\n\nThis is a test."

        result = await generator.generate(content, "test.md")

        assert result is True
        assert Path("test.md").exists()

        file_content = Path("test.md").read_text(encoding="utf-8")
        assert file_content == content

        Path("test.md").unlink()

    @pytest.mark.asyncio
    async def test_markdown_creates_directory(self):
        """Test that generator creates necessary directories."""
        generator = MarkdownGenerator()
        content = "# Test"

        result = await generator.generate(content, "subdir/test_output.md")

        assert result is True
        assert Path("subdir/test_output.md").exists()

        Path("subdir/test_output.md").unlink()
        Path("subdir").rmdir()


class TestPDFGenerator:
    """Test PDF document generator."""

    @pytest.mark.asyncio
    async def test_pdf_generation_without_pdfkit(self):
        """Test PDF generation fails gracefully without pdfkit."""
        generator = PDFGenerator()
        content = "# Test Document\n\n**Bold text**"

        result = await generator.generate(content, "test.pdf")

        assert result is False

    @pytest.mark.asyncio
    async def test_pdf_generation_with_content(self):
        """Test PDF generation with markdown content."""
        generator = PDFGenerator()
        content = "# Test Document\n\n## Section\n\n* Item 1\n* Item 2"

        result = await generator.generate(content, "test.pdf")

        assert result is False

        if Path("test.pdf").exists():
            Path("test.pdf").unlink()
