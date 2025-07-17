#!/usr/bin/env python3
"""
Run the FastAPI server on port 8003
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting FastAPI server on port 8003...")
    uvicorn.run(app, host="127.0.0.1", port=8003, reload=True)