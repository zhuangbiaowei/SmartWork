from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    id: str = Field(..., description="任务唯一标识符")
    description: str = Field(..., description="任务描述")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="任务优先级"
    )
    subtasks: List["Task"] = Field(default_factory=list, description="子任务列表")
    dependencies: List[str] = Field(
        default_factory=list, description="依赖的任务 ID 列表"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="最后更新时间")
    estimated_minutes: Optional[int] = Field(
        default=None, description="预估执行时间（分钟）"
    )

    class Config:
        use_enum_values = False
        json_encoders = {datetime: lambda v: v.isoformat()}
