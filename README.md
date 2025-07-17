# Task Management API

A comprehensive REST API for task management built with FastAPI, featuring CRUD operations, filtering, pagination, and background task processing.

## Features

- **CRUD Operations**: Create, Read, Update, Delete tasks
- **Status Filtering**: Filter tasks by status (active, completed, archived)
- **Priority Management**: Assign and filter by priority levels
- **Tag Support**: Add tags to tasks for better organization
- **Background Tasks**: Long-running operations with progress tracking
- **Pagination**: Efficient data retrieval with pagination support
- **Comprehensive Validation**: Input validation using Pydantic models
- **Error Handling**: Proper HTTP status codes and error messages

## Project Structure

```
.
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI app instance and configuration
│   ├── api/               # API route modules
│   │   ├── __init__.py
│   │   ├── tasks.py       # Task-related endpoints
│   │   ├── background.py  # Background task endpoints
│   │   └── system.py      # System endpoints (health, stats)
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   └── config.py      # Configuration settings
│   ├── models/            # Pydantic models
│   │   ├── __init__.py
│   │   └── task_models.py # Task data models
│   ├── database/          # Database operations
│   │   ├── __init__.py
│   │   └── database.py    # Database functions
│   ├── services/          # Business logic
│   │   └── __init__.py
│   └── utils/             # Utility functions
│       └── __init__.py
├── tests/                 # Test files
├── scripts/               # Utility scripts
├── main.py                # Application launcher
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd simple-rest-api-fast-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

**For Python 3.13 (recommended):**
```bash
# Clean install to avoid conflicts
pip uninstall pydantic pydantic-core pydantic-settings -y
pip install -r requirements.txt
```

**For Python 3.9-3.12:**
```bash
pip install -r requirements.txt
```

**Alternative installation script:**
```bash
python scripts/install_py313.py
```

## Running the Application

### Development Mode

```bash
python main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Tasks

- `GET /tasks` - Get all tasks with filtering and pagination
- `GET /tasks/{task_id}` - Get a specific task
- `POST /tasks` - Create a new task
- `PUT /tasks/{task_id}` - Update an existing task
- `DELETE /tasks/{task_id}` - Delete a task
- `GET /tasks/status/{status}` - Get tasks by status

### Background Tasks

- `POST /background-tasks` - Start a background task
- `GET /background-tasks/{task_id}` - Get background task status
- `GET /background-tasks` - Get all background tasks

### System

- `GET /` - API information
- `GET /health` - Health check
- `GET /statistics` - Task statistics

## Configuration

The application can be configured through environment variables or by modifying `app/core/config.py`:

- `APP_NAME`: Application name
- `VERSION`: API version
- `DEBUG`: Debug mode
- `HOST`: Server host
- `PORT`: Server port

## Testing

Run the tests:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.