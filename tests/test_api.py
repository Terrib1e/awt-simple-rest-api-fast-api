import pytest
import httpx
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app
from database import get_database

# Create test client
client = TestClient(app)

# Test data
sample_task = {
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the project",
    "status": "active",
    "priority": "high",
    "tags": ["documentation", "project"]
}

sample_task_update = {
    "title": "Updated task title",
    "status": "completed",
    "priority": "medium"
}

class TestTaskManagementAPI:
    """Test suite for Simple REST API FastAPI"""

    def setup_method(self):
        """Set up test environment before each test"""
        # Clear database before each test
        db = get_database()
        db.clear_all()

    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

    def test_create_task_success(self):
        """Test successful task creation"""
        response = client.post("/tasks", json=sample_task)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_task["title"]
        assert data["description"] == sample_task["description"]
        assert data["status"] == sample_task["status"]
        assert data["priority"] == sample_task["priority"]
        assert data["tags"] == sample_task["tags"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_invalid_data(self):
        """Test task creation with invalid data"""
        invalid_task = {
            "title": "",  # Empty title should fail
            "description": "Test description"
        }
        response = client.post("/tasks", json=invalid_task)
        assert response.status_code == 422

    def test_create_task_too_many_tags(self):
        """Test task creation with too many tags"""
        invalid_task = {
            "title": "Test task",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]  # More than 5 tags
        }
        response = client.post("/tasks", json=invalid_task)
        assert response.status_code == 422

    def test_get_task_success(self):
        """Test successful task retrieval"""
        # Create a task first
        create_response = client.post("/tasks", json=sample_task)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Get the task
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task["title"]

    def test_get_task_not_found(self):
        """Test task retrieval with non-existent ID"""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when database is empty"""
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 10

    def test_get_all_tasks_with_data(self):
        """Test getting all tasks with data"""
        # Create multiple tasks
        tasks = [
            {**sample_task, "title": "Task 1", "status": "active"},
            {**sample_task, "title": "Task 2", "status": "completed"},
            {**sample_task, "title": "Task 3", "status": "archived"}
        ]

        for task in tasks:
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Get all tasks
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 3
        assert data["total"] == 3

    def test_get_tasks_with_status_filter(self):
        """Test getting tasks with status filter"""
        # Create tasks with different statuses
        tasks = [
            {**sample_task, "title": "Active Task", "status": "active"},
            {**sample_task, "title": "Completed Task", "status": "completed"},
            {**sample_task, "title": "Archived Task", "status": "archived"}
        ]

        for task in tasks:
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Filter by active status
        response = client.get("/tasks?status=active")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["status"] == "active"

    def test_get_tasks_by_status_endpoint(self):
        """Test the alternative status filtering endpoint"""
        # Create tasks with different statuses
        tasks = [
            {**sample_task, "title": "Active Task", "status": "active"},
            {**sample_task, "title": "Completed Task", "status": "completed"}
        ]

        for task in tasks:
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Test status endpoint
        response = client.get("/tasks/status/active")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == "active"

    def test_update_task_success(self):
        """Test successful task update"""
        # Create a task first
        create_response = client.post("/tasks", json=sample_task)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Update the task
        response = client.put(f"/tasks/{task_id}", json=sample_task_update)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_task_update["title"]
        assert data["status"] == sample_task_update["status"]
        assert data["priority"] == sample_task_update["priority"]
        assert data["id"] == task_id

    def test_update_task_not_found(self):
        """Test task update with non-existent ID"""
        response = client.put("/tasks/999", json=sample_task_update)
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

    def test_update_task_no_data(self):
        """Test task update with no data"""
        # Create a task first
        create_response = client.post("/tasks", json=sample_task)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Try to update with empty data
        response = client.put(f"/tasks/{task_id}", json={})
        assert response.status_code == 400
        assert "No fields provided" in response.json()["error"]

    def test_delete_task_success(self):
        """Test successful task deletion"""
        # Create a task first
        create_response = client.post("/tasks", json=sample_task)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]

        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self):
        """Test task deletion with non-existent ID"""
        response = client.delete("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

    def test_statistics_empty(self):
        """Test statistics with empty database"""
        response = client.get("/statistics")
        assert response.status_code == 200
        data = response.json()
        stats = data["statistics"]
        assert stats["total"] == 0
        assert stats["active"] == 0
        assert stats["completed"] == 0
        assert stats["archived"] == 0

    def test_statistics_with_data(self):
        """Test statistics with data"""
        # Create tasks with different statuses
        tasks = [
            {**sample_task, "title": "Active Task 1", "status": "active"},
            {**sample_task, "title": "Active Task 2", "status": "active"},
            {**sample_task, "title": "Completed Task", "status": "completed"},
            {**sample_task, "title": "Archived Task", "status": "archived"}
        ]

        for task in tasks:
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Get statistics
        response = client.get("/statistics")
        assert response.status_code == 200
        data = response.json()
        stats = data["statistics"]
        assert stats["total"] == 4
        assert stats["active"] == 2
        assert stats["completed"] == 1
        assert stats["archived"] == 1

    def test_start_background_task(self):
        """Test starting a background task"""
        response = client.post("/background-tasks?duration=2")
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "started"
        assert "Background task started" in data["message"]

    def test_get_background_task_status(self):
        """Test getting background task status"""
        # Start a background task
        start_response = client.post("/background-tasks?duration=1")
        assert start_response.status_code == 200
        task_id = start_response.json()["task_id"]

        # Get task status
        response = client.get(f"/background-tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == task_id
        assert data["status"] in ["running", "completed"]
        assert "progress" in data

    def test_get_background_task_not_found(self):
        """Test getting non-existent background task"""
        response = client.get("/background-tasks/non-existent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["error"]

    def test_get_all_background_tasks(self):
        """Test getting all background tasks"""
        # Start a background task
        start_response = client.post("/background-tasks?duration=1")
        assert start_response.status_code == 200

        # Get all background tasks
        response = client.get("/background-tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_invalid_task_id_format(self):
        """Test endpoints with invalid task ID format"""
        # Test with string ID
        response = client.get("/tasks/invalid-id")
        assert response.status_code == 422

        # Test with zero ID
        response = client.get("/tasks/0")
        assert response.status_code == 422

    def test_priority_filtering(self):
        """Test filtering tasks by priority"""
        # Create tasks with different priorities
        tasks = [
            {**sample_task, "title": "High Priority", "priority": "high"},
            {**sample_task, "title": "Medium Priority", "priority": "medium"},
            {**sample_task, "title": "Low Priority", "priority": "low"}
        ]

        for task in tasks:
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Filter by high priority
        response = client.get("/tasks?priority=high")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["priority"] == "high"

    def test_tag_filtering(self):
        """Test filtering tasks by tags"""
        # Create tasks with different tags
        tasks = [
            {**sample_task, "title": "Task 1", "tags": ["urgent", "bug"]},
            {**sample_task, "title": "Task 2", "tags": ["feature", "enhancement"]},
            {**sample_task, "title": "Task 3", "tags": ["urgent", "feature"]}
        ]

        for task in tasks:
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Filter by urgent tag
        response = client.get("/tasks?tags=urgent")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2

        # Filter by feature tag
        response = client.get("/tasks?tags=feature")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2

    def test_pagination(self):
        """Test task pagination"""
        # Create 15 tasks
        for i in range(15):
            task = {**sample_task, "title": f"Task {i+1}"}
            response = client.post("/tasks", json=task)
            assert response.status_code == 201

        # Test first page
        response = client.get("/tasks?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1

        # Test second page
        response = client.get("/tasks?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 5
        assert data["total"] == 15
        assert data["page"] == 2

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])