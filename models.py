from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Enumeration for task statuses"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskPriority(str, Enum):
    """Enumeration for task priorities"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    """Base model for task data"""
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    status: TaskStatus = Field(TaskStatus.ACTIVE, description="Task status")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    tags: List[str] = Field(default_factory=list, description="Task tags")

    @validator('title')
    def validate_title(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) > 5:
            raise ValueError('Maximum 5 tags allowed')
        return [tag.strip().lower() for tag in v if tag.strip()]


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Model for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None and (not v or v.strip() == ""):
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v

    @validator('tags')
    def validate_tags(cls, v):
        if v is not None:
            if len(v) > 5:
                raise ValueError('Maximum 5 tags allowed')
            return [tag.strip().lower() for tag in v if tag.strip()]
        return v


class TaskResponse(TaskBase):
    """Model for task response data"""
    id: int = Field(..., description="Task ID")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")

    class Config:
        from_attributes = True


class TasksResponse(BaseModel):
    """Model for multiple tasks response"""
    tasks: List[TaskResponse]
    total: int
    page: int
    page_size: int


class BackgroundTaskResponse(BaseModel):
    """Model for background task response"""
    task_id: str = Field(..., description="Background task ID")
    status: str = Field(..., description="Background task status")
    message: str = Field(..., description="Background task message")


class BackgroundTaskStatus(BaseModel):
    """Model for background task status"""
    task_id: str
    status: str
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    message: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    status_code: int = Field(..., description="HTTP status code")


class SuccessResponse(BaseModel):
    """Model for success responses"""
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Response data")