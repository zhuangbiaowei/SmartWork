import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "backend"))

from generators.ppt_generator import PowerPointGenerator


class TestPowerPointGenerator:
    """Test PowerPoint document generator."""

    @pytest.mark.asyncio
    async def test_ppt_generation(self):
        """Test basic PowerPoint generation."""
        generator = PowerPointGenerator()

        data = {
            "title": "Test Presentation",
            "slides": [
                {
                    "title": "Slide 1",
                    "content": "This is the first slide",
                },
                {
                    "title": "Slide 2",
                    "content": "This is the second slide",
                    "points": [
                        "Point 1",
                        "Point 2",
                        "Point 3",
                    ],
                },
            ],
        }

        result = await generator.generate(data, "test.pptx")

        assert result is True
        assert Path("test.pptx").exists()

        Path("test.pptx").unlink()

    @pytest.mark.asyncio
    async def test_ppt_with_multiple_slides(self):
        """Test PowerPoint with multiple slides."""
        generator = PowerPointGenerator()

        data = {
            "title": "Multi-Slide Presentation",
            "slides": [
                {
                    "title": "Introduction",
                    "content": "Overview of the project",
                },
                {
                    "title": "Features",
                    "points": [
                        "Feature A",
                        "Feature B",
                        "Feature C",
                    ],
                },
                {
                    "title": "Conclusion",
                    "content": "Summary and next steps",
                },
            ],
        }

        result = await generator.generate(data, "multi.pptx")

        assert result is True
        assert Path("multi.pptx").exists()

        Path("multi.pptx").unlink()

    @pytest.mark.asyncio
    async def test_ppt_with_empty_slides(self):
        """Test PowerPoint with empty slide."""
        generator = PowerPointGenerator()

        data = {
            "title": "Empty Test",
            "slides": [
                {
                    "title": "Only Title",
                    "content": "Just a title, no content",
                },
            ],
        }

        result = await generator.generate(data, "empty.pptx")

        assert result is True
        assert Path("empty.pptx").exists()

        Path("empty.pptx").unlink()

    @pytest.mark.asyncio
    async def test_ppt_without_python_pptx(self):
        """Test PowerPoint generator without library."""
        generator = PowerPointGenerator()

        data = {
            "title": "Test Without Library",
            "slides": [],
        }

        result = await generator.generate(data, "test.xlsx")

        assert result is False
