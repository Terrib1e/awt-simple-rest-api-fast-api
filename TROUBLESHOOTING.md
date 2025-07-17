# Troubleshooting Guide

## Python 3.13 Compatibility Issues

### Error: `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`

This error occurs when trying to install pydantic-core with Python 3.13. This is a known compatibility issue.

## Solutions (in order of recommendation)

### Solution 1: Use the Automated Installer (RECOMMENDED)

Run the automated installer that handles Python 3.13 compatibility:

```bash
python install.py
```

This script will:
- Detect your Python version
- Install compatible versions for Python 3.13
- Set up a virtual environment
- Install all dependencies
- Verify the installation

### Solution 2: Manual Installation with Compatible Versions

If the automated installer doesn't work, try these manual steps:

1. **Create a virtual environment:**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install compatible versions:**
   ```bash
   pip install --upgrade pip
   pip install "pydantic>=2.0.0,<3.0.0"
   pip install "fastapi>=0.104.0"
   pip install "uvicorn[standard]>=0.24.0"
   pip install "pytest>=7.4.0"
   pip install "httpx>=0.25.0"
   ```

### Solution 3: Use Pre-built Wheels

If compilation fails, try using pre-built wheels:

```bash
pip install --only-binary=all pydantic fastapi uvicorn pytest httpx
```

### Solution 4: Downgrade to Python 3.12

If all else fails, you can use Python 3.12 which has full compatibility:

1. Install Python 3.12 from python.org
2. Create a virtual environment with Python 3.12
3. Install normally with `pip install -r requirements.txt`

### Solution 5: Alternative Installation Methods

**Using conda (if available):**
```bash
conda create -n fastapi-env python=3.12
conda activate fastapi-env
pip install -r requirements.txt
```

**Using Docker:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Verification

After installation, verify everything works:

```bash
python quick_test.py
```

## Common Issues and Solutions

### Issue: "Failed building wheel for pydantic-core"
**Solution:** Use pre-built wheels with `--only-binary=all` flag

### Issue: "Microsoft Visual C++ 14.0 is required"
**Solution:** Install Microsoft C++ Build Tools or use pre-built wheels

### Issue: "Rust compiler not found"
**Solution:** Use pre-built wheels or install Rust toolkit

### Issue: Virtual environment activation fails
**Solution:**
- On Windows: Use `venv\Scripts\activate.bat` instead of `activate`
- On PowerShell: Use `venv\Scripts\Activate.ps1`

## Getting Help

If you're still having issues:

1. Check your Python version: `python --version`
2. Check pip version: `pip --version`
3. Try the automated installer: `python install.py`
4. If all fails, create an issue with:
   - Your Python version
   - Your operating system
   - The complete error message
   - Steps you've already tried

## Success Indicators

You'll know the installation worked when:
- `python quick_test.py` runs without errors
- `python main.py` starts the server successfully
- You can access http://localhost:8000/docs in your browser

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)