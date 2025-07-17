#!/usr/bin/env python3
"""
Script to check registered API routes
"""
from app.main import app

print("🔍 Checking registered API routes:")
print("=" * 40)

for route in app.routes:
    methods = list(route.methods) if hasattr(route, 'methods') else ['N/A']
    path = route.path if hasattr(route, 'path') else 'N/A'
    print(f"  {methods} {path}")

print("\n🔍 Checking if routers are properly included:")
print("=" * 40)

# Check if routers are included
try:
    from app.api import tasks, background, system
    print("✅ All API modules imported successfully")

    # Check if routes are registered
    task_routes = [route for route in app.routes if '/tasks' in str(route.path)]
    bg_routes = [route for route in app.routes if '/background-tasks' in str(route.path)]
    sys_routes = [route for route in app.routes if route.path in ['/', '/health', '/statistics']]

    print(f"  Task routes: {len(task_routes)}")
    print(f"  Background routes: {len(bg_routes)}")
    print(f"  System routes: {len(sys_routes)}")

except Exception as e:
    print(f"❌ Error importing API modules: {e}")