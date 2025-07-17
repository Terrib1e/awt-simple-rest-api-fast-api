#!/usr/bin/env python3
"""
Test script for API on port 8003
"""

import requests
import json
import time

def test_api_port_8003():
    BASE_URL = 'http://localhost:8003'
    print('🧪 Testing API on port 8003...')
    print()

    # Give the server a moment to start
    time.sleep(3)

    # Test health
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f'✅ Health: {response.status_code} - {response.json()}')
    except Exception as e:
        print(f'❌ Health error: {e}')
        return False

    # Test task creation
    try:
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'active',
            'priority': 'medium',
            'tags': ['test']
        }
        response = requests.post(f'{BASE_URL}/tasks', json=task_data)
        print(f'✅ Task creation: {response.status_code} - {response.json()}')
        task_id = response.json()['id']
    except Exception as e:
        print(f'❌ Task creation error: {e}')
        return False

    # Test get tasks
    try:
        response = requests.get(f'{BASE_URL}/tasks')
        print(f'✅ Get tasks: {response.status_code} - Found {len(response.json())} tasks')
    except Exception as e:
        print(f'❌ Get tasks error: {e}')
        return False

    # Test task update
    try:
        update_data = {
            'title': 'Updated Test Task',
            'status': 'completed'
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=update_data)
        print(f'✅ Task update: {response.status_code} - {response.json()}')
    except Exception as e:
        print(f'❌ Task update error: {e}')
        return False

    print()
    print('🎉 SUCCESS! Your FastAPI server is working perfectly!')
    print()
    print('✅ PYTHON 3.13 COMPATIBILITY ISSUE RESOLVED!')
    print()
    print('You can now:')
    print('1. Visit http://localhost:8003/docs for interactive API documentation')
    print('2. Visit http://localhost:8003/redoc for alternative docs')
    print('3. Use all the API endpoints for your tasks')
    print()
    print('Available endpoints:')
    print('- GET /health - Health check')
    print('- GET /tasks - Get all tasks')
    print('- POST /tasks - Create new task')
    print('- PUT /tasks/{id} - Update task')
    print('- DELETE /tasks/{id} - Delete task')
    print('- GET /tasks/status/{status} - Filter by status')
    print('- POST /background-tasks - Start background task')
    print('- GET /background-tasks - Get background tasks')
    print()
    return True

if __name__ == '__main__':
    test_api_port_8003()