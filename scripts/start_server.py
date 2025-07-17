#!/usr/bin/env python3
"""
Start server script for Simple REST API FastAPI

This script provides an easy way to start the FastAPI server with proper configuration.
"""

import uvicorn
import subprocess
import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'pytest',
        'httpx'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages:")
        print("pip install -r requirements.txt")
        return False

    return True

def main():
    """Main function to start the server"""
    print("🚀 Simple REST API FastAPI Server")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    print("✅ All dependencies are installed")
    print("📡 Starting FastAPI server...")
    print("\nServer will be available at:")
    print("  - Main API: http://localhost:8000")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)

    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()