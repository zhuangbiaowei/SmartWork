import asyncio
from typing import List
from collections import deque
from datetime import datetime

from models.task import Task, TaskStatus


class TaskQueue:
    """
    Task queue system with parallel execution.

    Manages concurrent task execution with configurable limits.
    """

    def __init__(self, max_concurrent: int = 3):
        """
        Initialize task queue.

        Args:
            max_concurrent: Maximum number of concurrent tasks
        """
        self.max_concurrent = max_concurrent
        self.queue = deque()
        self.running_tasks = set()
        self.completed_tasks = set()

    async def add_task(self, task: Task) -> str:
        """
        Add a task to the queue.

        Args:
            task: Task to add

        Returns:
            Task ID
        """
        self.queue.append(task)
        await self._process_queue()
        return task.id

    async def get_status(self) -> dict:
        """
        Get queue status.

        Returns:
            Dictionary with queue statistics
        """
        return {
            "pending": len(self.queue),
            "running": len(self.running_tasks),
            "completed": len(self.completed_tasks),
            "max_concurrent": self.max_concurrent,
        }

    async def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.

        Returns:
            List of completed tasks
        """
        return list(self.completed_tasks)

    async def get_running_tasks(self) -> List[Task]:
        """
        Get currently running tasks.

        Returns:
            List of running tasks
        """
        return list(self.running_tasks)

    async def _process_queue(self):
        """
        Process the queue and execute tasks.

        Starts pending tasks when slots are available.
        """
        while len(self.running_tasks) < self.max_concurrent and self.queue:
            task = self.queue.popleft()
            task.status = TaskStatus.RUNNING
            self.running_tasks.add(task.id)

            asyncio.create_task(self._execute_task(task))

    async def _execute_task(self, task: Task):
        """
        Execute a single task.

        Args:
            task: Task to execute
        """
        try:
            await asyncio.sleep(1)

            task.status = TaskStatus.COMPLETED
        except Exception as e:
            task.status = TaskStatus.FAILED
            print(f"Task {task.id} failed: {e}")
        finally:
            if task.id in self.running_tasks:
                self.running_tasks.remove(task.id)

            if task.status == TaskStatus.COMPLETED:
                self.completed_tasks.add(task.id)

            await self._process_queue()
