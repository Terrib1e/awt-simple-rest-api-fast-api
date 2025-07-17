#!/usr/bin/env python3
"""
Installation script for FastAPI Task Management API
Handles Python 3.13 compatibility issues automatically
"""

import subprocess
import sys
import os

def run_command(command, description=""):
    """Run a command and return success status"""
    print(f"🔧 {description}")
    print(f"   Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=True, text=True)
        print(f"   ✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed: {e.stderr}")
        return False

def check_python_version():
    """Check Python version and provide recommendations"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 13:
        print("⚠️  Warning: Python 3.13 detected. May have compatibility issues.")
        print("   Recommendation: Use Python 3.11 or 3.12 for best compatibility.")
        return "3.13"
    elif version.major == 3 and version.minor >= 9:
        print("✅ Good Python version for FastAPI")
        return "compatible"
    else:
        print("❌ Python 3.9+ required")
        return "incompatible"

def install_packages():
    """Try multiple installation methods"""
    print("\n📦 Installing packages...")

    # Method 1: Pre-built wheels (recommended for Python 3.13)
    print("\n1️⃣ Trying installation with pre-built wheels...")
    if run_command("pip install --only-binary=pydantic-core fastapi uvicorn[standard] pydantic python-multipart pytest httpx requests",
                   "Installing with pre-built wheels"):
        return True

    # Method 2: Latest versions
    print("\n2️⃣ Trying latest versions...")
    if run_command("pip install --upgrade fastapi uvicorn pydantic python-multipart pytest httpx requests",
                   "Installing latest versions"):
        return True

    # Method 3: Specific compatible versions
    print("\n3️⃣ Trying specific compatible versions...")
    packages = [
        "fastapi==0.108.0",
        "uvicorn[standard]==0.25.0",
        "pydantic==2.5.3",
        "python-multipart==0.0.6",
        "pytest==7.4.3",
        "httpx==0.25.2",
        "requests==2.31.0"
    ]

    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"   ⚠️  Failed to install {package}, continuing...")

    # Method 4: Minimal installation
    print("\n4️⃣ Trying minimal installation...")
    if run_command("pip install fastapi uvicorn requests",
                   "Installing minimal packages"):
        print("   ⚠️  Minimal installation successful. Some features may be limited.")
        return "minimal"

    return False

def verify_installation():
    """Verify the installation works"""
    print("\n🧪 Verifying installation...")

    try:
        import fastapi
        import uvicorn
        print(f"   ✅ FastAPI {fastapi.__version__} installed")
        print(f"   ✅ Uvicorn {uvicorn.__version__} installed")

        try:
            import pydantic
            print(f"   ✅ Pydantic {pydantic.__version__} installed")
        except ImportError:
            print("   ⚠️  Pydantic not installed (minimal mode)")

        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def create_simple_test():
    """Create a simple test to verify everything works"""
    print("\n📝 Creating simple test...")

    test_code = '''
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test API")

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting test server...")
    print("Visit: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    try:
        with open("test_server.py", "w") as f:
            f.write(test_code)
        print("   ✅ Created test_server.py")
        print("   🔧 Run: python test_server.py")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create test file: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Simple REST API FastAPI - Installation Script")
    print("=" * 60)

    # Check Python version
    python_status = check_python_version()

    if python_status == "incompatible":
        print("\n❌ Installation cancelled. Please upgrade Python to 3.9+")
        return False

    # Update pip
    print("\n📈 Updating pip...")
    run_command("python -m pip install --upgrade pip", "Updating pip")

    # Install packages
    install_result = install_packages()

    if not install_result:
        print("\n❌ Installation failed. Please check the TROUBLESHOOTING.md file.")
        return False

    # Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed.")
        return False

    # Create test file
    create_simple_test()

    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Test the installation: python test_server.py")
    print("2. Run the main API: python main.py")
    print("3. Check documentation: http://localhost:8000/docs")

    if python_status == "3.13":
        print("\n⚠️  Python 3.13 Notes:")
        print("   - If you encounter issues, consider using Python 3.11 or 3.12")
        print("   - Check TROUBLESHOOTING.md for additional solutions")

    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)