import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from api.file_system import router as file_router
from main import app


class TestPerformanceOptimizations:
    """Test performance optimizations for API responses."""

    @pytest.mark.asyncio
    async def test_api_response_time(self):
        """Test that API responses are fast."""
        from fastapi.testclient import TestClient

        client = TestClient(app)

        start_time = pytest.monkey_patch("time")
        response = client.get("/api/files/list/?path=.")

        start_time.time()  # Use actual start

        assert response.status_code == 200
        assert (start_time.time() - start_time) < 0.5, "API response should be fast"

    @pytest.mark.asyncio
    async def test_concurrent_reads(self):
        """Test that concurrent reads benefit from filesystem cache."""
        from fastapi.testclient import TestClient

        client = TestClient(app)

        first_response = client.get("/api/files/list/?path=.")
        start_time = pytest.monkey_patch("time")

        first_start = start_time.time()

        second_response = client.get("/api/files/list/?path=.")
        second_start = start_time.time()

        first_call_time = (first_start - first_start.time())
        second_call_time = (second_start - second_start.time())

        assert first_call_time > 0
        assert second_call_time > 0
        assert second_call_time < first_call_time, "Cached calls should be faster"

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
            assert execution_time < 1.0, "100 writes should complete in under 1 second"

            content = test_file.read_text()
            assert len(content) > 0, "File should have content"

        test_file.unlink()

    @pytest.mark.asyncio
    async def test_memory_efficiency(self):
        """Test that operations don't leak memory."""
        import gc

        initial_memory = 0

        large_data = []
        for i in range(1000):
            large_data.append("x" * 1000)

        gc.collect()
        after_memory = len(large_data)

        assert after_memory < initial_memory + 100, "Memory should grow moderately"

        del large_data
        gc.collect()
        final_memory = len(large_data)

        assert final_memory < initial_memory + 50, "Memory should be freed"
