from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import whisper
from typing import Dict

from .utils.logger import logger
from .utils.error_handler import handle_error, AppError, ErrorCodes

# Global model instance
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Voice Assistant backend...")
    try:
        global model
        logger.info("Loading Whisper model...")
        model = whisper.load_model("base")
        logger.info("Whisper model loaded successfully")
        yield
    except Exception as e:
        logger.error("Failed to initialize application", exc_info=e)
        raise
    finally:
        # Cleanup
        logger.info("Shutting down Voice Assistant backend...")

app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, error: AppError):
    logger.error(f"Application error: {error.message}", extra={
        "error_code": error.error_code,
        "path": request.url.path,
        "details": error.details
    })
    return JSONResponse(
        status_code=error.status_code,
        content={
            "message": error.message,
            "error_code": error.error_code,
            "details": error.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, error: Exception):
    logger.exception(f"Unhandled error occurred: {str(error)}", extra={
        "path": request.url.path
    })
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred",
            "error_code": ErrorCodes.INTERNAL_ERROR,
            "details": {"error": str(error)}
        }
    )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}

@app.post("/transcribe")
async def transcribe_audio(audio_data: bytes):
    try:
        logger.info("Received transcription request")
        
        if not model:
            raise AppError(
                "Whisper model not initialized",
                ErrorCodes.WHISPER_ERROR,
                status_code=500
            )

        if not audio_data:
            raise AppError(
                "No audio data provided",
                ErrorCodes.INVALID_AUDIO_FORMAT,
                status_code=400
            )

        # Process audio with Whisper
        logger.debug("Processing audio with Whisper model")
        result = model.transcribe(audio_data)
        
        logger.info("Audio transcription completed successfully")
        return {"text": result["text"]}

    except AppError as e:
        raise e
    except Exception as e:
        logger.exception("Error during transcription", extra={
            "error": str(e)
        })
        raise handle_error(e, "transcribe_audio")
