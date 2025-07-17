#!/usr/bin/env python3
"""
Quick test script for Simple REST API FastAPI

This script performs a basic test of the API to verify it's working correctly.
Run this after starting the server to ensure everything is functioning.
"""

import requests
import json
import time

def test_api():
    """Test the basic API functionality"""
    BASE_URL = "http://localhost:8000"

    print("🧪 Quick API Test")
    print("=" * 40)

    try:
        # Test 1: Health check
        print("1. Testing health check...")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False

        # Test 2: Create a task
        print("2. Testing task creation...")
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "active",
            "priority": "medium",
            "tags": ["test"]
        }

        response = requests.post(f"{BASE_URL}/tasks", json=task_data)
        if response.status_code == 201:
            task = response.json()
            task_id = task["id"]
            print(f"   ✅ Task created with ID: {task_id}")
        else:
            print(f"   ❌ Task creation failed: {response.status_code}")
            return False

        # Test 3: Get the task
        print("3. Testing task retrieval...")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        if response.status_code == 200:
            print("   ✅ Task retrieved successfully")
        else:
            print(f"   ❌ Task retrieval failed: {response.status_code}")
            return False

        # Test 4: Update the task
        print("4. Testing task update...")
        update_data = {"status": "completed"}
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
        if response.status_code == 200:
            print("   ✅ Task updated successfully")
        else:
            print(f"   ❌ Task update failed: {response.status_code}")
            return False

        # Test 5: Filter tasks
        print("5. Testing task filtering...")
        response = requests.get(f"{BASE_URL}/tasks?status=completed")
        if response.status_code == 200:
            tasks = response.json()
            if tasks["total"] >= 1:
                print("   ✅ Task filtering works")
            else:
                print("   ❌ Task filtering returned no results")
        else:
            print(f"   ❌ Task filtering failed: {response.status_code}")
            return False

        # Test 6: Background task
        print("6. Testing background task...")
        response = requests.post(f"{BASE_URL}/background-tasks?duration=2")
        if response.status_code == 200:
            bg_task_id = response.json()["task_id"]
            print(f"   ✅ Background task started: {bg_task_id}")

            # Wait a moment and check progress
            time.sleep(3)
            response = requests.get(f"{BASE_URL}/background-tasks/{bg_task_id}")
            if response.status_code == 200:
                status = response.json()["status"]
                print(f"   ✅ Background task status: {status}")
            else:
                print("   ❌ Background task status check failed")
        else:
            print(f"   ❌ Background task failed: {response.status_code}")
            return False

        # Test 7: Delete the task
        print("7. Testing task deletion...")
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        if response.status_code == 200:
            print("   ✅ Task deleted successfully")
        else:
            print(f"   ❌ Task deletion failed: {response.status_code}")
            return False

        # Test 8: Statistics
        print("8. Testing statistics...")
        response = requests.get(f"{BASE_URL}/statistics")
        if response.status_code == 200:
            stats = response.json()["statistics"]
            print(f"   ✅ Statistics: {stats}")
        else:
            print(f"   ❌ Statistics failed: {response.status_code}")
            return False

        print("\n🎉 All tests passed! API is working correctly.")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API server.")
        print("Please make sure the server is running:")
        print("  python start_server.py")
        print("  or")
        print("  python main.py")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def main():
    """Main function"""
    success = test_api()
    if success:
        print("\n✅ API is ready to use!")
        print("📖 Check the README.md for more information")
        print("🌐 Visit http://localhost:8000/docs for interactive documentation")
    else:
        print("\n❌ Tests failed. Please check the server and try again.")

if __name__ == "__main__":
    main()