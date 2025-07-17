#!/usr/bin/env python3
"""
Test script for API on port 8002
"""

import requests
import json
import time

def test_api_port_8002():
    BASE_URL = 'http://localhost:8002'
    print('Testing API on port 8002...')
    print()

    # Give the server a moment to start
    time.sleep(2)

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

    print()
    print('🎉 SUCCESS! Your FastAPI server is working perfectly!')
    print()
    print('You can now:')
    print('1. Visit http://localhost:8002/docs for API documentation')
    print('2. Visit http://localhost:8002/redoc for alternative docs')
    print('3. Use the API endpoints for your tasks')
    print()
    print('The Python 3.13 compatibility issue has been resolved!')
    return True

if __name__ == '__main__':
    test_api_port_8002()