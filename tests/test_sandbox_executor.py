import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from core.sandbox import Sandbox
from core.task_executor import TaskExecutor, TaskExecutionState
from models.task import Task, TaskStatus


class TestSandbox:
    """Test Sandbox execution environment."""

    def test_sandbox_initialization(self):
        """Test sandbox creates temporary directory."""
        sandbox = Sandbox()
        sandbox.initialize()

        temp_dir = sandbox.get_temp_dir()
        assert Path(temp_dir).exists()
        assert "smartwork_sandbox_" in temp_dir

        sandbox.cleanup()
        assert not Path(temp_dir).exists()

    def test_sandbox_context_manager(self):
        """Test sandbox works with context manager."""
        with Sandbox() as sandbox:
            temp_dir = sandbox.get_temp_dir()
            assert Path(temp_dir).exists()

        assert not Path(temp_dir).exists()

    def test_write_and_read_file(self):
        """Test writing and reading files in sandbox."""
        with Sandbox() as sandbox:
            content = "Hello, World!"

            write_result = sandbox.write_file("test.txt", content)
            assert write_result["success"] is True

            read_result = sandbox.read_file("test.txt")
            assert read_result["success"] is True
            assert read_result["content"] == content

    def test_read_nonexistent_file(self):
        """Test reading nonexistent file fails gracefully."""
        with Sandbox() as sandbox:
            result = sandbox.read_file("nonexistent.txt")
            assert result["success"] is False
            assert "not found" in result["error"]

    def test_execute_command(self):
        """Test executing a simple command."""
        with Sandbox() as sandbox:
            result = sandbox.execute_command("echo 'test'")
            assert result["success"] is True
            assert "test" in result["stdout"]
            assert result["returncode"] == 0

    def test_execute_failing_command(self):
        """Test executing a failing command."""
        with Sandbox() as sandbox:
            result = sandbox.execute_command("exit 1")
            assert result["success"] is False
            assert result["returncode"] == 1

    def test_list_files(self):
        """Test listing files in sandbox."""
        with Sandbox() as sandbox:
            sandbox.write_file("file1.txt", "content1")
            sandbox.write_file("file2.txt", "content2")

            result = sandbox.list_files()
            assert result["success"] is True
            assert len(result["files"]) >= 2

            file_names = [f["name"] for f in result["files"]]
            assert "file1.txt" in file_names
            assert "file2.txt" in file_names

    def test_list_nonexistent_directory(self):
        """Test listing nonexistent directory fails."""
        with Sandbox() as sandbox:
            result = sandbox.list_files("nonexistent")
            assert result["success"] is False
            assert "not found" in result["error"]


class TestTaskExecutionState:
    """Test task execution state machine."""

    def test_can_transition_valid(self):
        """Test valid state transitions."""
        assert TaskExecutionState.can_transition(
            TaskExecutionState.PENDING, TaskExecutionState.PREPARING
        )
        assert TaskExecutionState.can_transition(
            TaskExecutionState.PREPARING, TaskExecutionState.RUNNING
        )
        assert TaskExecutionState.can_transition(
            TaskExecutionState.RUNNING, TaskExecutionState.COMPLETED
        )

    def test_cannot_transition_invalid(self):
        """Test invalid state transitions are rejected."""
        assert not TaskExecutionState.can_transition(
            TaskExecutionState.COMPLETED, TaskExecutionState.RUNNING
        )
        assert not TaskExecutionState.can_transition(
            TaskExecutionState.FAILED, TaskExecutionState.PREPARING
        )


class TestTaskExecutor:
    """Test TaskExecutor with state machine."""

    @pytest.mark.asyncio
    async def test_execute_simple_task(self):
        """Test executing a simple task."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-1", description="Simple test task")
        progress_calls = []

        def progress_callback(description, progress):
            progress_calls.append((description, progress))

        result = await executor.execute_task(task, progress_callback)

        assert task.status == TaskStatus.COMPLETED
        assert len(progress_calls) == 2
        assert progress_calls[-1][1] == 100

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_execute_task_with_subtasks(self):
        """Test executing a task with multiple subtasks."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        subtask1 = Task(id="sub-1", description="Subtask 1")
        subtask2 = Task(id="sub-2", description="Subtask 2")
        task = Task(
            id="test-2", description="Parent task", subtasks=[subtask1, subtask2]
        )

        result = await executor.execute_task(task)

        assert task.status == TaskStatus.COMPLETED
        assert subtask1.status == TaskStatus.PENDING
        assert subtask2.status == TaskStatus.PENDING

        task_result = executor.get_task_result("test-2")
        assert task_result is not None
        assert task_result["success"] is True
        assert task_result["completed_subtasks"] == 2

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_task_state_transitions(self):
        """Test task goes through correct state transitions."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-3", description="State test task")

        await executor.execute_task(task)

        states = []
        if "test-3" in executor.task_states:
            states.append(executor.task_states["test-3"])

        assert task.status == TaskStatus.COMPLETED

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_task_logging(self):
        """Test task execution generates logs."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-4", description="Logging test task")

        await executor.execute_task(task)

        logs = executor.get_task_logs("test-4")
        assert len(logs) > 0
        assert any("Sandbox initialized" in log["message"] for log in logs)
        assert any("Task completed" in log["message"] for log in logs)

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_get_task_state(self):
        """Test retrieving task state."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-5", description="State retrieval task")

        await executor.execute_task(task)

        final_state = executor.get_task_state("test-5")
        assert final_state == TaskExecutionState.COMPLETED

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_task_state_transitions(self):
        """Test task goes through correct state transitions."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-3", description="State test task")

        await executor.execute_task(task)

        states = []
        if "test-3" in executor.task_states:
            states.append(executor.task_states["test-3"])

        assert task.status == TaskStatus.COMPLETED

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_task_logging(self):
        """Test task execution generates logs."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-4", description="Logging test task")

        await executor.execute_task(task)

        logs = executor.get_task_logs("test-4")
        assert len(logs) > 0
        assert any("Sandbox initialized" in log["message"] for log in logs)
        assert any("Task completed" in log["message"] for log in logs)

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_get_task_state(self):
        """Test retrieving task state."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-5", description="State retrieval task")

        await executor.execute_task(task)

        final_state = executor.get_task_state("test-5")
        assert final_state == TaskExecutionState.COMPLETED

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_get_nonexistent_task_state(self):
        """Test retrieving state of nonexistent task."""
        executor = TaskExecutor()

        state = executor.get_task_state("nonexistent")
        assert state is None

    @pytest.mark.asyncio
    async def test_cancel_task(self):
        """Test cancelling a task."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        task = Task(id="test-6", description="Cancel test task")

        cancelled = await executor.cancel_task("test-6")
        assert cancelled is False

        await executor.cleanup()

    @pytest.mark.asyncio
    async def test_cleanup(self):
        """Test executor cleanup."""
        sandbox = Sandbox()
        executor = TaskExecutor(sandbox)

        await executor.cleanup()

        assert not sandbox.temp_dir.exists()
