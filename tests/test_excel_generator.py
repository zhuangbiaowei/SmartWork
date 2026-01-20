import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from generators.excel_generator import ExcelGenerator


class TestExcelGenerator:
    """Test Excel document generator."""

    @pytest.mark.asyncio
    async def test_excel_generation(self):
        """Test basic Excel generation."""
        generator = ExcelGenerator()

        data = {
            "title": "Test Report",
            "headers": ["Column A", "Column B", "Column C"],
            "rows": [
                ["A1", "B1", "C1"],
                ["A2", "B2", "C2"],
                ["A3", "B3", "C3"],
            ],
        }

        result = await generator.generate(data, "test.xlsx")

        assert result is True
        assert Path("test.xlsx").exists()

        Path("test.xlsx").unlink()

    @pytest.mark.asyncio
    async def test_excel_with_formulas(self):
        """Test Excel with formulas."""
        if ExcelGenerator.ExcelGenerator is None:
            pytest.skip("openpyxl not installed")

        generator = ExcelGenerator()

        data = {
            "title": "Financial Report",
            "headers": ["Item", "Cost", "Tax", "Total"],
            "rows": [
                ["Laptop", 1200, 120, 1440],
                ["Mouse", 50, 5, 55],
                ["Keyboard", 300, 30, 330],
            ],
        }

        result = await generator.generate(data, "financial.xlsx")

        assert result is True
        assert Path("financial.xlsx").exists()

        Path("financial.xlsx").unlink()

    @pytest.mark.asyncio
    async def test_excel_empty_data(self):
        """Test Excel with empty data."""
        generator = ExcelGenerator()

        data = {
            "title": "Empty Report",
            "rows": [],
        }

        result = await generator.generate(data, "empty.xlsx")

        assert result is True
        assert Path("empty.xlsx").exists()

        Path("empty.xlsx").unlink()

    @pytest.mark.asyncio
    async def test_excel_with_headers_only(self):
        """Test Excel with headers but no rows."""
        generator = ExcelGenerator()

        data = {
            "title": "Headers Only",
            "headers": ["Name", "Email", "Phone"],
        }

        result = await generator.generate(data, "headers_only.xlsx")

        assert result is True
        assert Path("headers_only.xlsx").exists()

        Path("headers_only.xlsx").unlink()
