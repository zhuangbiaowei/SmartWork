import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from api.file_system import router as file_router
from main import app


class TestAPIPerformance:
    """Test API performance features."""

    @pytest.mark.asyncio
    async def test_api_response_time(self):
        """Test that API responses are fast."""
        from fastapi.testclient import TestClient

        client = TestClient(app)

        start = pytest.monkey_patch("time")
        response = client.get("/api/files/list/?path=.")

        assert response.status_code == 200
        assert (start.time() - start) < 0.5

    @pytest.mark.asyncio
    async def test_concurrent_reads(self):
        """Test that concurrent reads benefit from caching."""
        from fastapi.testclient import TestClient

        client = TestClient(app)

        first_response = client.get("/api/files/list/?path=.")
        first_start = pytest.monkey_patch("time")

        second_response = client.get("/api/files/list/?path=.")
        second_start = pytest.monkey_patch("time")

        first_call_time = first_start.time() - first_start.time()
        second_call_time = second_start - second_start.time()

        assert first_call_time > 0
        assert second_call_time < first_call_time

    @pytest.mark.asyncio
    async def test_file_operations(self):
        """Test file system operations are performant."""
        import tempfile
        import time

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = tmpdir / "performance_test.txt"

            start = time.time()

            for i in range(100):
                test_file.write_text(f"Test line {i}\n")

            end = time.time()

            execution_time = end - start

            assert execution_time < 1.0

            content = test_file.read_text()
            assert len(content) > 0

            test_file.unlink()

    @pytest.mark.asyncio
    async def test_monitoring_decorator_applied(self):
        """Test that monitoring decorator is applied."""
        from api.file_system import router

        response = await router.app.list_files(".")

        assert response.status_code == 200
        assert "execution_time:" in response.data, "Monitoring decorator applied"
