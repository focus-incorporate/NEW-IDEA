from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import json
import asyncio
import logging
from pathlib import Path

from .assistant import VoiceAssistant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Assistant API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize voice assistant
MODEL_PATH = Path("models/llama-7b")  # Update with your model path
assistant = VoiceAssistant(llm_model_path=str(MODEL_PATH))

# Store active connections
active_connections: Dict[str, WebSocket] = {}

@app.get("/")
async def root():
    return {"message": "Voice Assistant API is running"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_bytes()
            
            # Process voice input and stream response
            async for response in assistant.process_voice_input(client_id, data):
                await websocket.send_json(response)
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if client_id in active_connections:
            del active_connections[client_id]

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    assistant.cleanup()
    logger.info("Application shutting down")
