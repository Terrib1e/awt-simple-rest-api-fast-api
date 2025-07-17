"""
Task-related API endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import List, Optional

from app.models.task_models import (
    TaskCreate, TaskUpdate, TaskResponse, TasksResponse,
    TaskStatus, TaskPriority, SuccessResponse
)
from app.database.database import get_database

# Create router
router = APIRouter(prefix="/tasks", tags=["tasks"])

# Get database instance
db = get_database()


@router.get("", response_model=TasksResponse)
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get all tasks with optional filtering and pagination.

    - **status**: Filter by task status (active, completed, archived)
    - **priority**: Filter by task priority (low, medium, high)
    - **tags**: Filter by tags (can specify multiple)
    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (max 100)
    """
    try:
        tasks, total = db.get_tasks(
            status=status,
            priority=priority,
            tags=tags,
            page=page,
            page_size=page_size
        )

        return TasksResponse(
            tasks=tasks,
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@router.get("/status/{task_status}", response_model=List[TaskResponse])
async def get_tasks_by_status(
    task_status: TaskStatus = Path(..., description="Task status to filter by")
):
    """
    Get tasks filtered by status.

    - **task_status**: The status to filter by (active, completed, archived)
    """
    try:
        tasks = db.get_tasks_by_status(task_status)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks by status: {str(e)}"
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int = Path(..., gt=0, description="Task ID to retrieve")
):
    """
    Get a specific task by ID.

    - **task_id**: The ID of the task to retrieve
    """
    task = db.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Create a new task.

    - **title**: Task title (required, 1-100 characters)
    - **description**: Task description (optional, max 500 characters)
    - **status**: Task status (default: active)
    - **priority**: Task priority (default: medium)
    - **due_date**: Task due date (optional)
    - **tags**: Task tags (optional, max 5 tags)
    """
    try:
        task_data = task.model_dump()
        new_task = db.create_task(task_data)
        return new_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int = Path(..., gt=0, description="Task ID to update"),
    task_update: TaskUpdate = None
):
    """
    Update an existing task.

    - **task_id**: The ID of the task to update
    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **status**: New task status (optional)
    - **priority**: New task priority (optional)
    - **due_date**: New task due date (optional)
    - **tags**: New task tags (optional)
    """
    # Check if task exists
    if not db.get_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    try:
        # Get only non-null fields to update
        update_data = task_update.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        updated_task = db.update_task(task_id, update_data)
        return updated_task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/{task_id}", response_model=SuccessResponse)
async def delete_task(
    task_id: int = Path(..., gt=0, description="Task ID to delete")
):
    """
    Delete a task by ID.

    - **task_id**: The ID of the task to delete
    """
    if not db.get_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    try:
        success = db.delete_task(task_id)
        if success:
            return SuccessResponse(
                message=f"Task {task_id} deleted successfully"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete task"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )