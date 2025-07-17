from datetime import datetime
from typing import Dict, List, Optional
from app.models.task_models import TaskResponse, TaskStatus, TaskPriority, BackgroundTaskStatus
import threading


class InMemoryDatabase:
    """Simple in-memory database for storing tasks and background tasks"""

    def __init__(self):
        self.tasks: Dict[int, dict] = {}
        self.background_tasks: Dict[str, BackgroundTaskStatus] = {}
        self.next_task_id: int = 1
        self.lock = threading.Lock()

    def create_task(self, task_data: dict) -> TaskResponse:
        """Create a new task"""
        with self.lock:
            task_id = self.next_task_id
            self.next_task_id += 1

            now = datetime.now()
            task = {
                "id": task_id,
                "title": task_data["title"],
                "description": task_data.get("description"),
                "status": task_data.get("status", TaskStatus.ACTIVE),
                "priority": task_data.get("priority", TaskPriority.MEDIUM),
                "due_date": task_data.get("due_date"),
                "tags": task_data.get("tags", []),
                "created_at": now,
                "updated_at": now
            }

            self.tasks[task_id] = task
            return TaskResponse(**task)

    def get_task(self, task_id: int) -> Optional[TaskResponse]:
        """Get a task by ID"""
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                return TaskResponse(**task)
            return None

    def get_tasks(self,
                  status: Optional[TaskStatus] = None,
                  priority: Optional[TaskPriority] = None,
                  tags: Optional[List[str]] = None,
                  page: int = 1,
                  page_size: int = 10) -> tuple[List[TaskResponse], int]:
        """Get tasks with filtering and pagination"""
        with self.lock:
            tasks = list(self.tasks.values())

            # Apply filters
            if status:
                tasks = [task for task in tasks if task["status"] == status]

            if priority:
                tasks = [task for task in tasks if task["priority"] == priority]

            if tags:
                tasks = [task for task in tasks
                        if any(tag in task["tags"] for tag in tags)]

            # Sort by created_at descending
            tasks.sort(key=lambda x: x["created_at"], reverse=True)

            total = len(tasks)

            # Apply pagination
            start = (page - 1) * page_size
            end = start + page_size
            paginated_tasks = tasks[start:end]

            return [TaskResponse(**task) for task in paginated_tasks], total

    def update_task(self, task_id: int, update_data: dict) -> Optional[TaskResponse]:
        """Update a task"""
        with self.lock:
            if task_id not in self.tasks:
                return None

            task = self.tasks[task_id]

            # Update fields
            for field, value in update_data.items():
                if value is not None:
                    task[field] = value

            task["updated_at"] = datetime.now()

            return TaskResponse(**task)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                return True
            return False

    def get_tasks_by_status(self, status: TaskStatus) -> List[TaskResponse]:
        """Get tasks filtered by status"""
        with self.lock:
            tasks = [task for task in self.tasks.values()
                    if task["status"] == status]
            tasks.sort(key=lambda x: x["created_at"], reverse=True)
            return [TaskResponse(**task) for task in tasks]

    def get_task_statistics(self) -> dict:
        """Get task statistics"""
        with self.lock:
            total = len(self.tasks)
            active = sum(1 for task in self.tasks.values()
                        if task["status"] == TaskStatus.ACTIVE)
            completed = sum(1 for task in self.tasks.values()
                           if task["status"] == TaskStatus.COMPLETED)
            archived = sum(1 for task in self.tasks.values()
                          if task["status"] == TaskStatus.ARCHIVED)

            return {
                "total": total,
                "active": active,
                "completed": completed,
                "archived": archived
            }

    def create_background_task(self, task_id: str, message: str) -> BackgroundTaskStatus:
        """Create a background task entry"""
        with self.lock:
            bg_task = BackgroundTaskStatus(
                task_id=task_id,
                status="running",
                progress=0,
                message=message,
                started_at=datetime.now()
            )
            self.background_tasks[task_id] = bg_task
            return bg_task

    def update_background_task(self, task_id: str, status: str,
                             progress: int, message: str,
                             result: Optional[dict] = None) -> Optional[BackgroundTaskStatus]:
        """Update a background task"""
        with self.lock:
            if task_id not in self.background_tasks:
                return None

            bg_task = self.background_tasks[task_id]
            bg_task.status = status
            bg_task.progress = progress
            bg_task.message = message
            bg_task.result = result

            if status in ["completed", "failed"]:
                bg_task.completed_at = datetime.now()

            return bg_task

    def get_background_task(self, task_id: str) -> Optional[BackgroundTaskStatus]:
        """Get a background task status"""
        with self.lock:
            return self.background_tasks.get(task_id)

    def clear_all(self):
        """Clear all data (for testing)"""
        with self.lock:
            self.tasks.clear()
            self.background_tasks.clear()
            self.next_task_id = 1


# Global database instance
db = InMemoryDatabase()


def get_database():
    """Get the database instance"""
    return db