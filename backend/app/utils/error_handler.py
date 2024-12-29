from fastapi import HTTPException
from typing import Dict, Any, Optional
from .logger import logger

class AppError(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ErrorCodes:
    AUDIO_PROCESSING_ERROR = "AUDIO_PROCESSING_ERROR"
    WHISPER_ERROR = "WHISPER_ERROR"
    INVALID_AUDIO_FORMAT = "INVALID_AUDIO_FORMAT"
    STREAM_ERROR = "STREAM_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"

def handle_error(error: Exception, context: str = "") -> HTTPException:
    """
    Handles different types of exceptions and converts them to HTTPException
    """
    if isinstance(error, AppError):
        logger.error(f"Application error in {context}: {error.message}", extra={
            "error_code": error.error_code,
            "details": error.details,
            "context": context
        })
        return HTTPException(
            status_code=error.status_code,
            detail={
                "message": error.message,
                "error_code": error.error_code,
                "details": error.details
            }
        )
    
    if isinstance(error, HTTPException):
        logger.error(f"HTTP error in {context}: {error.detail}", extra={
            "status_code": error.status_code,
            "context": context
        })
        return error
    
    # Log unexpected errors
    logger.exception(f"Unexpected error in {context}: {str(error)}")
    return HTTPException(
        status_code=500,
        detail={
            "message": "An unexpected error occurred",
            "error_code": ErrorCodes.INTERNAL_ERROR,
            "details": {"original_error": str(error)}
        }
    )

def log_error(
    message: str,
    error: Optional[Exception] = None,
    context: str = "",
    extra: Optional[Dict[str, Any]] = None
) -> None:
    """
    Utility function to log errors with consistent formatting
    """
    log_data = {
        "context": context,
        **(extra or {})
    }
    
    if error:
        log_data["error_type"] = type(error).__name__
        log_data["error_str"] = str(error)
        
        if isinstance(error, AppError):
            log_data["error_code"] = error.error_code
            log_data["details"] = error.details
    
    if error:
        logger.exception(message, extra=log_data)
    else:
        logger.error(message, extra=log_data)
