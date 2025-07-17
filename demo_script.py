#!/usr/bin/env python3
"""
Demo script for Simple REST API FastAPI

This script demonstrates all the API endpoints with real examples.
Make sure to start the FastAPI server before running this demo:
    python main.py

or

    uvicorn main:app --reload
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_response(response: requests.Response, title: str = "Response"):
    """Print formatted response"""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running and healthy!")
            return True
        else:
            print("❌ Server is not responding properly")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the FastAPI server first.")
        print("Run: python main.py or uvicorn main:app --reload")
        return False

def demo_basic_endpoints():
    """Demonstrate basic API endpoints"""
    print_section("BASIC ENDPOINTS")

    # Root endpoint
    print("\n1. Testing Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root endpoint")

    # Health check
    print("\n2. Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health check")

def demo_crud_operations():
    """Demonstrate CRUD operations"""
    print_section("CRUD OPERATIONS")

    # Sample tasks to create
    sample_tasks = [
        {
            "title": "Complete API documentation",
            "description": "Write comprehensive documentation for the Task Management API",
            "status": "active",
            "priority": "high",
            "tags": ["documentation", "api", "urgent"]
        },
        {
            "title": "Implement user authentication",
            "description": "Add JWT-based authentication to secure the API",
            "status": "active",
            "priority": "medium",
            "tags": ["security", "auth", "backend"]
        },
        {
            "title": "Design database schema",
            "description": "Create optimized database schema for production",
            "status": "completed",
            "priority": "high",
            "tags": ["database", "design", "schema"]
        }
    ]

    created_tasks = []

    # CREATE - Create multiple tasks
    print("\n1. Creating Tasks (POST /tasks)")
    for i, task in enumerate(sample_tasks, 1):
        response = requests.post(f"{BASE_URL}/tasks", json=task)
        print(f"\nCreating task {i}: {task['title']}")
        print_response(response, f"Task {i} created")
        if response.status_code == 201:
            created_tasks.append(response.json())

    # READ - Get all tasks
    print("\n2. Getting All Tasks (GET /tasks)")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response, "All tasks")

    # READ - Get single task
    if created_tasks:
        task_id = created_tasks[0]["id"]
        print(f"\n3. Getting Single Task (GET /tasks/{task_id})")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        print_response(response, f"Task {task_id}")

    # UPDATE - Update a task
    if created_tasks:
        task_id = created_tasks[0]["id"]
        update_data = {
            "title": "Updated: Complete API documentation",
            "description": "Updated description with more details",
            "status": "completed",
            "priority": "medium"
        }
        print(f"\n4. Updating Task (PUT /tasks/{task_id})")
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
        print_response(response, f"Task {task_id} updated")

    # DELETE - Delete a task
    if len(created_tasks) > 1:
        task_id = created_tasks[1]["id"]
        print(f"\n5. Deleting Task (DELETE /tasks/{task_id})")
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        print_response(response, f"Task {task_id} deleted")

    return created_tasks

def demo_filtering_operations():
    """Demonstrate filtering operations"""
    print_section("FILTERING OPERATIONS")

    # Filter by status
    print("\n1. Filter by Status (GET /tasks?status=active)")
    response = requests.get(f"{BASE_URL}/tasks?status=active")
    print_response(response, "Active tasks")

    print("\n2. Filter by Status (GET /tasks?status=completed)")
    response = requests.get(f"{BASE_URL}/tasks?status=completed")
    print_response(response, "Completed tasks")

    print("\n3. Alternative Status Endpoint (GET /tasks/status/active)")
    response = requests.get(f"{BASE_URL}/tasks/status/active")
    print_response(response, "Active tasks (alternative endpoint)")

    # Filter by priority
    print("\n4. Filter by Priority (GET /tasks?priority=high)")
    response = requests.get(f"{BASE_URL}/tasks?priority=high")
    print_response(response, "High priority tasks")

    # Filter by tags
    print("\n5. Filter by Tags (GET /tasks?tags=documentation)")
    response = requests.get(f"{BASE_URL}/tasks?tags=documentation")
    print_response(response, "Tasks with 'documentation' tag")

def demo_background_tasks():
    """Demonstrate background task functionality"""
    print_section("BACKGROUND TASKS")

    # Start background task
    print("\n1. Starting Background Task (POST /background-tasks?duration=5)")
    response = requests.post(f"{BASE_URL}/background-tasks?duration=5")
    print_response(response, "Background task started")

    if response.status_code == 200:
        task_id = response.json()["task_id"]

        # Monitor progress
        print(f"\n2. Monitoring Background Task Progress (GET /background-tasks/{task_id})")
        for i in range(8):  # Check progress 8 times
            response = requests.get(f"{BASE_URL}/background-tasks/{task_id}")
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                progress = data["progress"]
                message = data["message"]
                print(f"Progress check {i+1}: {status} - {progress}% - {message}")

                if status == "completed":
                    print(f"Task completed! Result: {data.get('result', 'N/A')}")
                    break
                elif status == "failed":
                    print(f"Task failed: {message}")
                    break

            time.sleep(1)

    # Get all background tasks
    print("\n3. Getting All Background Tasks (GET /background-tasks)")
    response = requests.get(f"{BASE_URL}/background-tasks")
    print_response(response, "All background tasks")

def demo_statistics():
    """Demonstrate statistics endpoint"""
    print_section("STATISTICS")

    print("\n1. Getting Task Statistics (GET /statistics)")
    response = requests.get(f"{BASE_URL}/statistics")
    print_response(response, "Task statistics")

def demo_error_handling():
    """Demonstrate error handling"""
    print_section("ERROR HANDLING")

    # Test 404 error
    print("\n1. Testing 404 Error (GET /tasks/999)")
    response = requests.get(f"{BASE_URL}/tasks/999")
    print_response(response, "404 Error")

    # Test validation error
    print("\n2. Testing Validation Error (POST /tasks with invalid data)")
    invalid_task = {
        "title": "",  # Empty title should fail
        "description": "Test description"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=invalid_task)
    print_response(response, "Validation Error")

def main():
    """Main demo function"""
    print("🚀 Simple REST API FastAPI Demo Script")
    print("=" * 60)

    # Check if server is running
    if not check_server():
        return

    try:
        # Run all demo sections
        demo_basic_endpoints()
        created_tasks = demo_crud_operations()
        demo_filtering_operations()
        demo_background_tasks()
        demo_statistics()
        demo_error_handling()

        print_section("DEMO COMPLETED")
        print("✅ All API endpoints have been demonstrated successfully!")
        print("\nTo explore the API interactively:")
        print("1. Visit http://localhost:8000/docs for Swagger UI")
        print("2. Visit http://localhost:8000/redoc for ReDoc documentation")
        print("3. Use the test cases: python -m pytest test_api.py -v")

    except requests.exceptions.ConnectionError:
        print("❌ Connection lost during demo. Please ensure the server is running.")
    except Exception as e:
        print(f"❌ Error during demo: {e}")

if __name__ == "__main__":
    main()