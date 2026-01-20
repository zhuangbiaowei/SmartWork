from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from core.task_planner import TaskPlanner
from core.task_executor import TaskExecutor
from models.task import Task

router = APIRouter()

task_planner = TaskPlanner()
task_executor = TaskExecutor()


class TaskCreateRequest(BaseModel):
    description: str
    parent_task_id: Optional[str] = None


@router.post("/")
async def create_task(request: TaskCreateRequest):
    """
    Create a new task and start execution.

    Args:
        request: Task creation request with description

    Returns:
        Created task with initial status
    """
    try:
        task = task_planner.plan_task(
            request.description, parent_task_id=request.parent_task_id
        )

        return {
            "success": True,
            "task": task.dict(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}")
async def get_task(task_id: str):
    """
    Get task details by ID.

    Args:
        task_id: Task identifier

    Returns:
        Task details with current status
    """
    try:
        task = task_planner.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "task": task.dict(),
            "logs": task_executor.get_task_logs(task_id),
            "result": task_executor.get_task_result(task_id),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{task_id}/execute")
async def execute_task(task_id: str):
    """
    Execute a task by ID.

    Args:
        task_id: Task identifier

    Returns:
        Updated task after execution
    """
    try:
        task = task_planner.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        executed_task = await task_executor.execute_task(task)

        return {
            "success": True,
            "task": executed_task.dict(),
            "result": task_executor.get_task_result(task_id),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}/state")
async def get_task_state(task_id: str):
    """
    Get current state of a task.

    Args:
        task_id: Task identifier

    Returns:
        Current task state
    """
    try:
        state = task_executor.get_task_state(task_id)
        if state is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "task_id": task_id,
            "state": state,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}/logs")
async def get_task_logs(task_id: str):
    """
    Get execution logs for a task.

    Args:
        task_id: Task identifier

    Returns:
        List of log entries
    """
    try:
        logs = task_executor.get_task_logs(task_id)

        return {
            "success": True,
            "task_id": task_id,
            "logs": logs,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}")
async def cancel_task(task_id: str):
    """
    Cancel a running task.

    Args:
        task_id: Task identifier

    Returns:
        Success status
    """
    try:
        cancelled = await task_executor.cancel_task(task_id)

        return {
            "success": cancelled,
            "message": "Task cancelled"
            if cancelled
            else "Task not running or not found",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_tasks():
    """
    List all tasks.

    Returns:
        List of all tasks
    """
    try:
        tasks = task_planner.get_all_tasks()

        return {
            "success": True,
            "tasks": [task.dict() for task in tasks],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
