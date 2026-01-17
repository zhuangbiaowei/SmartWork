import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from core.task_planner import TaskPlanner
from models.task import Task, TaskStatus, TaskPriority


def test_task_decomposition():
    planner = TaskPlanner()

    task = Task(id="test-1", description="生成月度销售报告")

    subtasks = planner._rule_based_decompose(task)

    assert len(subtasks) > 1
    assert any("收集" in subtask.description for subtask in subtasks)
    assert any("生成" in subtask.description for subtask in subtasks)


def test_task_priority_assignment():
    planner = TaskPlanner()

    task = Task(id="test-2", description="测试生成任务")

    subtasks = planner._rule_based_decompose(task)

    assert all(hasattr(subtask, "priority") for subtask in subtasks)
    assert all(isinstance(subtask.priority, TaskPriority) for subtask in subtasks)


def test_task_dependencies():
    planner = TaskPlanner()

    task = Task(id="test-3", description="分析数据")

    subtasks = planner._rule_based_decompose(task)

    assert all(hasattr(subtask, "dependencies") for subtask in subtasks)

    for subtask in subtasks:
        if subtask.dependencies:
            dep_ids = [dep for dep in subtask.dependencies]
            assert all(any(st.id == dep_id for st in subtasks) for dep_id in dep_ids)


def test_parse_llm_response():
    planner = TaskPlanner()

    response_json = '[{"description": "测试子任务1", "priority": "high"}, {"description": "测试子任务2", "priority": "medium"}]'
    subtasks = planner._parse_llm_response(response_json, "test-parent")

    assert len(subtasks) == 2
    assert subtasks[0].id == "test-parent-1"
    assert subtasks[1].id == "test-parent-2"


def test_simple_task():
    planner = TaskPlanner()

    task = Task(id="test-4", description="")

    subtasks = planner._decompose_generation_task(task)

    assert len(subtasks) > 0
    assert all(isinstance(st, Task) for st in subtasks)
