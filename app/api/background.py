"""
Background task API endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Path, status
from typing import List
import uuid
import asyncio
from datetime import datetime

from app.models.task_models import (
    BackgroundTaskResponse, BackgroundTaskStatus
)
from app.database.database import get_database

# Create router
router = APIRouter(prefix="/background-tasks", tags=["background-tasks"])

# Get database instance
db = get_database()


async def simulate_long_running_task(task_id: str, duration: int = 10):
    """Simulate a long-running background task"""
    try:
        # Create background task entry
        db.create_background_task(task_id, f"Starting long-running task (duration: {duration}s)")

        # Simulate work with progress updates
        for i in range(duration):
            await asyncio.sleep(1)
            progress = int((i + 1) / duration * 100)
            db.update_background_task(
                task_id,
                "running",
                progress,
                f"Processing step {i + 1}/{duration}"
            )

        # Complete the task
        result = {
            "processed_items": duration,
            "success": True,
            "completion_time": datetime.now().isoformat()
        }

        db.update_background_task(
            task_id,
            "completed",
            100,
            "Task completed successfully",
            result
        )

    except Exception as e:
        # Handle errors
        db.update_background_task(
            task_id,
            "failed",
            0,
            f"Task failed: {str(e)}"
        )


@router.post("", response_model=BackgroundTaskResponse)
async def start_background_task(
    background_tasks: BackgroundTasks,
    duration: int = Query(10, ge=1, le=60, description="Task duration in seconds")
):
    """
    Start a long-running background task.

    - **duration**: Task duration in seconds (1-60 seconds)

    This endpoint demonstrates background task processing with progress tracking.
    """
    try:
        task_id = str(uuid.uuid4())

        # Add the background task
        background_tasks.add_task(simulate_long_running_task, task_id, duration)

        return BackgroundTaskResponse(
            task_id=task_id,
            status="started",
            message=f"Background task started with duration {duration}s"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting background task: {str(e)}"
        )


@router.get("/{task_id}", response_model=BackgroundTaskStatus)
async def get_background_task_status(
    task_id: str = Path(..., description="Background task ID")
):
    """
    Get the status of a background task.

    - **task_id**: The ID of the background task
    """
    bg_task = db.get_background_task(task_id)
    if not bg_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Background task with ID {task_id} not found"
        )
    return bg_task


@router.get("", response_model=List[BackgroundTaskStatus])
async def get_all_background_tasks():
    """
    Get all background tasks and their statuses.
    """
    return list(db.background_tasks.values())