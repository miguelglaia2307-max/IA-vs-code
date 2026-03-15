"""
Global exception handler and error monitoring middleware
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from typing import Callable
from app.services.logger import logger
from app.services.error_recovery import error_agent

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to capture and log all errors"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log the error
            error_type = type(e).__name__
            error_message = str(e)
            tb_str = traceback.format_exc()
            
            logger.log_error(
                error_type=error_type,
                message=error_message,
                context={
                    "path": request.url.path,
                    "method": request.method,
                    "client": request.client.host if request.client else "unknown"
                },
                traceback_str=tb_str
            )
            
            # Try to get AI analysis (async in background)
            try:
                analysis = error_agent.analyze_error(
                    error_type=error_type,
                    message=error_message,
                    traceback_str=tb_str
                )
                logger.log_info("AI analysis available", {"error_type": error_type})
            except Exception as ai_error:
                logger.log_warning("Could not get AI analysis", {"error": str(ai_error)})
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": error_type,
                    "message": error_message,
                    "detail": "An unexpected error occurred. Our monitoring system has been notified."
                }
            )

def add_error_handlers(app: FastAPI):
    """Add global exception handlers to FastAPI app"""
    
    @app.exception_handler(Exception)
    async def universal_exception_handler(request: Request, exc: Exception):
        error_type = type(exc).__name__
        error_message = str(exc)
        tb_str = traceback.format_exc()
        
        logger.log_error(
            error_type=error_type,
            message=error_message,
            context={
                "path": request.url.path,
                "method": request.method,
            },
            traceback_str=tb_str
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": error_type,
                "message": "An error occurred. Our system has logged this issue.",
            }
        )
