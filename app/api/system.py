"""
System API endpoints (health, statistics, root)
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.database.database import get_database

# Create router
router = APIRouter(tags=["system"])

# Get database instance
db = get_database()


@router.get("/", response_model=dict)
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


@router.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@router.get("/statistics", response_model=dict)
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