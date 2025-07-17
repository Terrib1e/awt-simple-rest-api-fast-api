#!/usr/bin/env python3
"""
Python 3.13 Compatible Installation Script for FastAPI Task Management API
This script handles pydantic-core compilation issues with Python 3.13
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def install_dependencies():
    """Install dependencies with Python 3.13 compatibility"""
    print("🚀 Installing FastAPI Task Management API dependencies for Python 3.13...")
    print(f"Python version: {sys.version}")

    # Method 1: Try installing with --only-binary for pydantic-core
    print("\n📦 Method 1: Installing with pre-built wheels...")
    if run_command(
        "pip install --only-binary=pydantic-core -r requirements.txt",
        "Installing dependencies with pre-built wheels"
    ):
        return True

    # Method 2: Install dependencies individually
    print("\n📦 Method 2: Installing dependencies individually...")

    dependencies = [
        "fastapi==0.110.0",
        "uvicorn[standard]==0.28.0",
        "python-multipart==0.0.7",
        "pydantic-settings==2.2.1",
        "pytest==8.1.1",
        "httpx==0.27.0",
        "requests==2.31.0"
    ]

    # Install pydantic with --only-binary first
    if not run_command(
        "pip install --only-binary=pydantic-core pydantic==2.7.0",
        "Installing pydantic with pre-built wheels"
    ):
        print("❌ Failed to install pydantic. Trying alternative version...")
        if not run_command(
            "pip install --only-binary=pydantic-core pydantic==2.8.0b1",
            "Installing pydantic pre-release version"
        ):
            return False

    # Install other dependencies
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}, continuing...")

    return True

def verify_installation():
    """Verify that the installation was successful"""
    print("\n🔍 Verifying installation...")

    try:
        # Test imports
        import fastapi
        import uvicorn
        import pydantic
        from pydantic_settings import BaseSettings

        print("✅ All core dependencies imported successfully")
        print(f"FastAPI version: {fastapi.__version__}")
        print(f"Pydantic version: {pydantic.__version__}")

        # Test app import
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from app.main import app
        print("✅ FastAPI app imported successfully")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main installation function"""
    print("=" * 60)
    print("🔧 FastAPI Task Management API - Python 3.13 Installer")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)

    if sys.version_info >= (3, 13):
        print("⚠️  Python 3.13 detected. Using compatibility mode...")

    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please try manual installation:")
        print("1. pip install --only-binary=pydantic-core pydantic==2.7.0")
        print("2. pip install fastapi==0.110.0 uvicorn[standard]==0.28.0")
        print("3. pip install python-multipart==0.0.7 pydantic-settings==2.2.1")
        sys.exit(1)

    # Verify installation
    if verify_installation():
        print("\n🎉 Installation completed successfully!")
        print("You can now run the API with: python main.py")
    else:
        print("\n⚠️  Installation completed but verification failed")
        print("Please check the installation manually")

if __name__ == "__main__":
    main()