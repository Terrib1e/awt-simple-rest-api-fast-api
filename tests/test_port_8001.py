#!/usr/bin/env python3
"""
Test script for API on port 8001
"""

import requests
import json

def test_api_port_8001():
    BASE_URL = 'http://localhost:8001'
    print('Testing API on port 8001...')
    print()

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
    print('🎉 API is working! You can now:')
    print('1. Visit http://localhost:8001/docs for API documentation')
    print('2. Run the full test suite: python test_api.py')
    print('3. Run the interactive demo: python demo_script.py')
    return True

if __name__ == '__main__':
    test_api_port_8001()