"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.models.task_models import ErrorResponse
from app.api import tasks, background, system

# Create FastAPI app with metadata
app = FastAPI(
    title=settings.app_name,
    description="""
    A comprehensive REST API for task management with the following features:

    ## Features
    - **CRUD Operations**: Create, Read, Update, Delete tasks
    - **Status Filtering**: Filter tasks by status (active, completed, archived)
    - **Priority Management**: Assign and filter by priority levels
    - **Tag Support**: Add tags to tasks for better organization
    - **Background Tasks**: Long-running operations with progress tracking
    - **Pagination**: Efficient data retrieval with pagination support
    - **Comprehensive Validation**: Input validation using Pydantic models
    - **Error Handling**: Proper HTTP status codes and error messages

    ## Task Statuses
    - **Active**: Currently being worked on
    - **Completed**: Task has been finished
    - **Archived**: Old tasks moved to archive

    ## Priority Levels
    - **Low**: Nice to have
    - **Medium**: Normal priority
    - **High**: Urgent tasks
    """,
    version=settings.version,
    debug=settings.debug,
    contact={
        "name": "API Support",
        "email": "support@taskmanagement.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Include routers
app.include_router(system.router)
app.include_router(tasks.router)
app.include_router(background.router)

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )

@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation Error",
            detail=str(exc),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ).model_dump()
    )