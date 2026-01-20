from typing import List, Optional, Dict
from models.task import Task, TaskStatus, TaskPriority
from llm.llm_client import LLMClient
import json
import re


class TaskPlanner:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client
        self.tasks: Dict[str, Task] = {}

    async def decompose_task(self, task: Task) -> List[Task]:
        if not task.description:
            return [task]

        if self.llm_client:
            return await self._llm_decompose(task)
        else:
            return self._rule_based_decompose(task)

    async def _llm_decompose(self, task: Task) -> List[Task]:
        prompt = f"""
请将以下任务分解为具体的、可执行的子任务。

任务描述: {task.description}

要求:
1. 每个子任务应该是独立可执行的
2. 子任务之间应该有逻辑顺序
3. 子任务描述要清晰具体

请以 JSON 格式返回子任务列表，格式如下:
[
  {{
    "description": "子任务描述",
    "priority": "low|medium|high"
  }}
]
"""

        try:
            response = await self.llm_client.generate(prompt)
            return self._parse_llm_response(response, task.id)
        except Exception as e:
            print(f"LLM 分解失败，使用规则方法: {e}")
            return self._rule_based_decompose(task)

    def _rule_based_decompose(self, task: Task) -> List[Task]:
        description = task.description.lower()

        if "报告" in description or "分析" in description:
            return self._decompose_report_task(task)
        elif "生成" in description or "创建" in description:
            return self._decompose_generation_task(task)
        elif "测试" in description:
            return self._decompose_test_task(task)
        else:
            return [task]

    def _decompose_report_task(self, task: Task) -> List[Task]:
        subtasks = [
            Task(
                id=f"{task.id}-1",
                description="收集数据",
                priority=TaskPriority.HIGH,
                dependencies=[],
            ),
            Task(
                id=f"{task.id}-2",
                description="分析数据",
                priority=TaskPriority.HIGH,
                dependencies=[f"{task.id}-1"],
            ),
            Task(
                id=f"{task.id}-3",
                description="生成报告",
                priority=TaskPriority.MEDIUM,
                dependencies=[f"{task.id}-2"],
            ),
            Task(
                id=f"{task.id}-4",
                description="审核报告",
                priority=TaskPriority.LOW,
                dependencies=[f"{task.id}-3"],
            ),
        ]
        return subtasks

    def _decompose_generation_task(self, task: Task) -> List[Task]:
        subtasks = [
            Task(
                id=f"{task.id}-1",
                description="准备生成环境",
                priority=TaskPriority.HIGH,
                dependencies=[],
            ),
            Task(
                id=f"{task.id}-2",
                description="生成内容",
                priority=TaskPriority.HIGH,
                dependencies=[f"{task.id}-1"],
            ),
            Task(
                id=f"{task.id}-3",
                description="验证生成结果",
                priority=TaskPriority.MEDIUM,
                dependencies=[f"{task.id}-2"],
            ),
        ]
        return subtasks

    def _decompose_test_task(self, task: Task) -> List[Task]:
        subtasks = [
            Task(
                id=f"{task.id}-1",
                description="准备测试环境",
                priority=TaskPriority.HIGH,
                dependencies=[],
            ),
            Task(
                id=f"{task.id}-2",
                description="执行测试用例",
                priority=TaskPriority.HIGH,
                dependencies=[f"{task.id}-1"],
            ),
            Task(
                id=f"{task.id}-3",
                description="收集测试结果",
                priority=TaskPriority.MEDIUM,
                dependencies=[f"{task.id}-2"],
            ),
            Task(
                id=f"{task.id}-4",
                description="分析测试结果",
                priority=TaskPriority.MEDIUM,
                dependencies=[f"{task.id}-3"],
            ),
        ]
        return subtasks

    def _parse_llm_response(self, response: str, parent_id: str) -> List[Task]:
        try:
            json_match = re.search(r"\[[\s\S]*\]", response)
            if not json_match:
                return [Task(id=f"{parent_id}-1", description=response)]

            tasks_data = json.loads(json_match.group())
            subtasks = []

            for idx, task_data in enumerate(tasks_data):
                subtask = Task(
                    id=f"{parent_id}-{idx + 1}",
                    description=task_data.get("description", ""),
                    priority=TaskPriority(task_data.get("priority", "medium")),
                )
                subtasks.append(subtask)

            return (
                subtasks
                if subtasks
                else [Task(id=f"{parent_id}-1", description=response)]
            )
        except Exception as e:
            print(f"解析 LLM 响应失败: {e}")
            return [Task(id=f"{parent_id}-1", description=response)]

    async def plan_task(
        self, description: str, parent_task_id: Optional[str] = None
    ) -> Task:
        """
        Create and plan a new task.

        Args:
            description: Task description
            parent_task_id: Optional parent task ID for subtasks

        Returns:
            Created task with planned subtasks
        """
        task = Task(id=f"task-{len(self.tasks) + 1}", description=description)

        if parent_task_id and parent_task_id in self.tasks:
            parent = self.tasks[parent_task_id]
            parent.subtasks.append(task)
            task.dependencies = [parent_task_id]
        else:
            subtasks = await self.decompose_task(task)
            task.subtasks = subtasks

        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task or None if not found
        """
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return list(self.tasks.values())
