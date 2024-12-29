import os
from typing import Dict, Any

# Get log level from environment variable, default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Base logging configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored": {
            "()": "rich.logging.RichFormatter",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "level": LOG_LEVEL,
            "formatter": "colored",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.json",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json",
            "level": LOG_LEVEL,
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "standard",
            "level": "ERROR",
        },
    },
    "loggers": {
        "voice_assistant": {  # Root logger for our application
            "handlers": ["console", "json_file", "error_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {  # Uvicorn logger
            "handlers": ["console", "json_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "fastapi": {  # FastAPI logger
            "handlers": ["console", "json_file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {  # Root logger
        "level": LOG_LEVEL,
        "handlers": ["console", "json_file", "error_file"],
    },
}
