import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from core.task_queue import TaskQueue
from models.task import Task, TaskStatus, TaskPriority


class TestTaskQueue:
    """Test task queue system."""

    @pytest.mark.asyncio
    async def test_add_single_task(self):
        """Test adding a single task."""
        queue = TaskQueue(max_concurrent=2)

        task1 = Task(id="1", description="Task 1", priority=TaskPriority.HIGH)
        task_id = await queue.add_task(task1)

        assert task_id == "1"

        status = await queue.get_status()
        assert status["pending"] == 1
        assert status["running"] == 0

    @pytest.mark.asyncio
    async def test_add_multiple_tasks(self):
        """Test adding multiple tasks."""
        queue = TaskQueue(max_concurrent=2)

        task1 = Task(id="1", description="Task 1")
        task2 = Task(id="2", description="Task 2")
        task3 = Task(id="3", description="Task 3")

        await queue.add_task(task1)
        await queue.add_task(task2)
        await queue.add_task(task3)

        await asyncio.sleep(2.5)

        status = await queue.get_status()
        assert status["pending"] == 1
        assert status["running"] == 2
        assert status["completed"] == 1

    @pytest.mark.asyncio
    async def test_concurrent_limit(self):
        """Test max concurrent limit."""
        queue = TaskQueue(max_concurrent=2)

        for i in range(5):
            task = Task(id=f"{i}", description=f"Task {i}")
            await queue.add_task(task)

        await asyncio.sleep(3)

        status = await queue.get_status()
        assert status["pending"] == 3
        assert status["running"] == 2
        assert status["completed"] == 2

    @pytest.mark.asyncio
    async def test_get_completed_tasks(self):
        """Test retrieving completed tasks."""
        queue = TaskQueue(max_concurrent=2)

        task1 = Task(id="1", description="Task 1")
        task2 = Task(id="2", description="Task 2")

        await queue.add_task(task1)
        await asyncio.sleep(2)

        task2_id = await queue.add_task(task2)
        await asyncio.sleep(1.5)

        status = await queue.get_status()
        assert status["completed"] == 1

        completed_tasks = await queue.get_completed_tasks()
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == "1"

    @pytest.mark.asyncio
    async def test_get_running_tasks(self):
        """Test retrieving running tasks."""
        queue = TaskQueue(max_concurrent=2)

        task1 = Task(id="1", description="Task 1")
        await queue.add_task(task1)

        await asyncio.sleep(0.5)

        running_tasks = await queue.get_running_tasks()
        assert len(running_tasks) == 1
        assert running_tasks[0].id == "1"

    @pytest.mark.asyncio
    async def test_queue_status(self):
        """Test queue status reporting."""
        queue = TaskQueue(max_concurrent=3)

        status = await queue.get_status()
        assert status["max_concurrent"] == 3
        assert status["pending"] == 0
        assert status["running"] == 0
        assert status["completed"] == 0
