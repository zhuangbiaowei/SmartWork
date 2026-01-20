import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import logging

from .sandbox import Sandbox
from models.task import Task, TaskStatus

logger = logging.getLogger(__name__)


class TaskExecutionState:
    """
    State machine for task execution lifecycle.

    States:
        - PENDING: Task waiting to start
        - PREPARING: Setting up environment
        - RUNNING: Task is executing
        - PAUSED: Task execution paused
        - COMPLETED: Task finished successfully
        - FAILED: Task failed
        - CANCELLED: Task was cancelled
    """

    PENDING = "pending"
    PREPARING = "preparing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    TRANSITIONS = {
        PENDING: [PREPARING, CANCELLED],
        PREPARING: [RUNNING, FAILED],
        RUNNING: [COMPLETED, FAILED, PAUSED],
        PAUSED: [RUNNING, CANCELLED],
        COMPLETED: [],
        FAILED: [],
        CANCELLED: [],
    }

    @classmethod
    def can_transition(cls, from_state: str, to_state: str) -> bool:
        return to_state in cls.TRANSITIONS.get(from_state, [])


class TaskExecutor:
    """
    Task execution engine with state machine and sandbox isolation.

    Manages the complete lifecycle of task execution including
    environment setup, execution, monitoring, and cleanup.
    """

    def __init__(self, sandbox: Optional[Sandbox] = None):
        self.sandbox: Sandbox = sandbox or Sandbox()
        self.task_states: Dict[str, str] = {}
        self.task_results: Dict[str, Dict[str, Any]] = {}
        self.task_logs: Dict[str, list] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}

    async def execute_task(
        self,
        task: Task,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> Task:
        """
        Execute a task through the state machine.

        Args:
            task: The task to execute
            progress_callback: Optional callback for progress updates

        Returns:
            Updated task with final status and results
        """
        task_id = task.id
        status_value = (
            task.status.value if hasattr(task.status, "value") else str(task.status)
        )

        if not TaskExecutionState.can_transition(
            status_value, TaskExecutionState.PREPARING
        ):
            logger.warning(f"Task {task_id} cannot be executed from {status_value}")
            return task

        try:
            self._set_state(task_id, TaskExecutionState.PREPARING)
            await self._prepare_task(task)

            self._set_state(task_id, TaskExecutionState.RUNNING)
            self._log(task_id, "Starting task execution")

            result = await self._process_task(task, progress_callback)

            if result["success"]:
                task.status = TaskStatus.COMPLETED
                self._set_state(task_id, TaskExecutionState.COMPLETED)
                self._log(task_id, "Task completed successfully")
            else:
                task.status = TaskStatus.FAILED
                self._set_state(task_id, TaskExecutionState.FAILED)
                self._log(
                    task_id, f"Task failed: {result.get('error', 'Unknown error')}"
                )

            self.task_results[task_id] = result
            return task

        except asyncio.CancelledError:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.CANCELLED)
            self._log(task_id, "Task was cancelled")
            return task

        except Exception as e:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.FAILED)
            self._log(task_id, f"Task execution error: {str(e)}")
            self.task_results[task_id] = {"success": False, "error": str(e)}
            return task

        try:
            self._set_state(task_id, TaskExecutionState.PREPARING)
            await self._prepare_task(task)

            self._set_state(task_id, TaskExecutionState.RUNNING)
            self._log(task_id, "Starting task execution")

            result = await self._process_task(task, progress_callback)

            if result["success"]:
                task.status = TaskStatus.COMPLETED
                self._set_state(task_id, TaskExecutionState.COMPLETED)
                self._log(task_id, "Task completed successfully")
            else:
                task.status = TaskStatus.FAILED
                self._set_state(task_id, TaskExecutionState.FAILED)
                self._log(
                    task_id, f"Task failed: {result.get('error', 'Unknown error')}"
                )

            self.task_results[task_id] = result
            return task

        except asyncio.CancelledError:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.CANCELLED)
            self._log(task_id, "Task was cancelled")
            return task

        except Exception as e:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.FAILED)
            self._log(task_id, f"Task execution error: {str(e)}")
            self.task_results[task_id] = {"success": False, "error": str(e)}
            return task

        try:
            self._set_state(task_id, TaskExecutionState.PREPARING)
            await self._prepare_task(task)

            self._set_state(task_id, TaskExecutionState.RUNNING)
            self._log(task_id, "Starting task execution")

            result = await self._process_task(task, progress_callback)

            if result["success"]:
                task.status = TaskStatus.COMPLETED
                self._set_state(task_id, TaskExecutionState.COMPLETED)
                self._log(task_id, "Task completed successfully")
            else:
                task.status = TaskStatus.FAILED
                self._set_state(task_id, TaskExecutionState.FAILED)
                self._log(
                    task_id, f"Task failed: {result.get('error', 'Unknown error')}"
                )

            self.task_results[task_id] = result
            return task

        except asyncio.CancelledError:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.CANCELLED)
            self._log(task_id, "Task was cancelled")
            return task

        except Exception as e:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.FAILED)
            self._log(task_id, f"Task execution error: {str(e)}")
            self.task_results[task_id] = {"success": False, "error": str(e)}
            return task

        try:
            self._set_state(task_id, TaskExecutionState.PREPARING)
            await self._prepare_task(task)

            self._set_state(task_id, TaskExecutionState.RUNNING)
            self._log(task_id, "Starting task execution")

            result = await self._process_task(task, progress_callback)

            if result["success"]:
                task.status = TaskStatus.COMPLETED
                self._set_state(task_id, TaskExecutionState.COMPLETED)
                self._log(task_id, "Task completed successfully")
            else:
                task.status = TaskStatus.FAILED
                self._set_state(task_id, TaskExecutionState.FAILED)
                self._log(
                    task_id, f"Task failed: {result.get('error', 'Unknown error')}"
                )

            self.task_results[task_id] = result
            return task

        except asyncio.CancelledError:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.CANCELLED)
            self._log(task_id, "Task was cancelled")
            return task

        except Exception as e:
            task.status = TaskStatus.FAILED
            self._set_state(task_id, TaskExecutionState.FAILED)
            self._log(task_id, f"Task execution error: {str(e)}")
            self.task_results[task_id] = {"success": False, "error": str(e)}
            return task

    async def _prepare_task(self, task: Task) -> None:
        """
        Prepare task execution environment.

        Initializes sandbox and any required resources.
        """
        self.sandbox.initialize()
        self._log(task.id, "Sandbox initialized")

    async def _process_task(
        self,
        task: Task,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Process the actual task execution.

        Args:
            task: The task to process
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with execution result
        """
        self._log(task.id, f"Executing task: {task.description}")

        if task.subtasks:
            result = await self._execute_subtasks(task, progress_callback)
        else:
            result = await self._execute_single_task(task, progress_callback)

        return result

    async def _execute_subtasks(
        self,
        task: Task,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Execute all subtasks sequentially.

        Args:
            task: Parent task with subtasks
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with overall execution result
        """
        total_subtasks = len(task.subtasks)
        completed = 0

        all_results = []

        for subtask in task.subtasks:
            self._log(task.id, f"Executing subtask: {subtask.description}")

            subtask_result = await self._execute_single_task(subtask, progress_callback)
            all_results.append(subtask_result)

            completed += 1
            if progress_callback:
                progress = (completed / total_subtasks) * 100
                progress_callback(subtask.description, progress)

        success = all(r["success"] for r in all_results)

        return {
            "success": success,
            "subtask_results": all_results,
            "total_subtasks": total_subtasks,
            "completed_subtasks": completed,
        }

    async def _execute_single_task(
        self,
        task: Task,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Execute a single task.

        Args:
            task: The task to execute
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with execution result
        """
        await asyncio.sleep(0.1)

        if progress_callback:
            progress_callback(task.description, 50)

        await asyncio.sleep(0.1)

        if progress_callback:
            progress_callback(task.description, 100)

        return {
            "success": True,
            "task_id": task.id,
            "description": task.description,
            "completed_at": datetime.now().isoformat(),
        }

    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a running task.

        Args:
            task_id: ID of task to cancel

        Returns:
            True if task was cancelled, False otherwise
        """
        if task_id in self._running_tasks:
            task = self._running_tasks[task_id]
            task.cancel()
            self._set_state(task_id, TaskExecutionState.CANCELLED)
            self._log(task_id, "Task cancelled")
            return True
        return False

    def _set_state(self, task_id: str, state: str) -> None:
        """
        Set the state of a task.

        Args:
            task_id: ID of the task
            state: New state value
        """
        self.task_states[task_id] = state
        logger.debug(f"Task {task_id} state: {state}")

    def _log(self, task_id: str, message: str) -> None:
        """
        Add a log entry for a task.

        Args:
            task_id: ID of the task
            message: Log message
        """
        if task_id not in self.task_logs:
            self.task_logs[task_id] = []

        timestamp = datetime.now().isoformat()
        self.task_logs[task_id].append({"timestamp": timestamp, "message": message})
        logger.debug(f"[Task {task_id}] {message}")

    def get_task_state(self, task_id: str) -> Optional[str]:
        """
        Get the current state of a task.

        Args:
            task_id: ID of the task

        Returns:
            Current state or None if task not found
        """
        return self.task_states.get(task_id)

    def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the execution result of a task.

        Args:
            task_id: ID of the task

        Returns:
            Task result or None if not available
        """
        return self.task_results.get(task_id)

    def get_task_logs(self, task_id: str) -> list:
        """
        Get all logs for a task.

        Args:
            task_id: ID of the task

        Returns:
            List of log entries
        """
        return self.task_logs.get(task_id, [])

    async def cleanup(self) -> None:
        """
        Clean up executor resources.

        Cancels all running tasks and cleans up sandbox.
        """
        for task_id, task in self._running_tasks.items():
            task.cancel()
            self._log(task_id, "Task cancelled during cleanup")

        self._running_tasks.clear()
        self.sandbox.cleanup()
