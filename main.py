from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Path, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid
import time
import asyncio
from datetime import datetime

from models import (
    TaskCreate, TaskUpdate, TaskResponse, TasksResponse, TaskStatus, TaskPriority,
    BackgroundTaskResponse, BackgroundTaskStatus, ErrorResponse, SuccessResponse
)
from database import get_database

# Create FastAPI app with metadata
app = FastAPI(
    title="Task Management API",
    description="""
    A comprehensive REST API for task management with the following features:

    ## Features
    - **CRUD Operations**: Create, Read, Update, Delete tasks
    - **Status Filtering**: Filter tasks by status (active, completed, archived)
    - **Priority Management**: Assign and filter by priority levels
    - **Tag Support**: Add tags to tasks for better organization
    - **Background Tasks**: Long-running operations with progress tracking
    - **Pagination**: Efficient data retrieval with pagination support
    - **Comprehensive Validation**: Input validation using Pydantic models
    - **Error Handling**: Proper HTTP status codes and error messages

    ## Task Statuses
    - **Active**: Currently being worked on
    - **Completed**: Task has been finished
    - **Archived**: Old tasks moved to archive

    ## Priority Levels
    - **Low**: Nice to have
    - **Medium**: Normal priority
    - **High**: Urgent tasks
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@taskmanagement.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database instance
db = get_database()

# Error handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )

# Error handler for validation errors
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation Error",
            detail=str(exc),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ).model_dump()
    )

# Root endpoint
@app.get("/", response_model=dict)
async def root():
    """Welcome message and API information"""
    return {
        "message": "Welcome to Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "tasks": "/tasks",
            "task_by_id": "/tasks/{task_id}",
            "tasks_by_status": "/tasks/status/{status}",
            "background_tasks": "/background-tasks",
            "statistics": "/statistics"
        }
    }

# Health check endpoint
@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# GET - Get all tasks with filtering and pagination
@app.get("/tasks", response_model=TasksResponse)
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

# GET - Get tasks by status (alternative endpoint)
@app.get("/tasks/status/{task_status}", response_model=List[TaskResponse])
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

# GET - Get single task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
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

# POST - Create new task
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
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

# PUT - Update existing task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
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

# DELETE - Delete task
@app.delete("/tasks/{task_id}", response_model=SuccessResponse)
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

# GET - Task statistics
@app.get("/statistics", response_model=dict)
async def get_task_statistics():
    """
    Get task statistics including counts by status.
    """
    try:
        stats = db.get_task_statistics()
        return {
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving statistics: {str(e)}"
        )

# Background task simulation function
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

# POST - Start background task
@app.post("/background-tasks", response_model=BackgroundTaskResponse)
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

# GET - Get background task status
@app.get("/background-tasks/{task_id}", response_model=BackgroundTaskStatus)
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

# GET - Get all background tasks
@app.get("/background-tasks", response_model=List[BackgroundTaskStatus])
async def get_all_background_tasks():
    """
    Get all background tasks and their statuses.
    """
    return list(db.background_tasks.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)