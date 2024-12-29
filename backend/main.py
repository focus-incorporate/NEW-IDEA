from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from speech.processor import SpeechProcessor
from speech.voice_detection import VoiceDetector
import logging
import numpy as np
from config.settings import get_settings

app = FastAPI()
settings = get_settings()
speech_processor = SpeechProcessor()
voice_detector = VoiceDetector()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_data = np.frombuffer(data, dtype=np.float32)
            
            # Check for voice activity
            if voice_detector.detect_voice_activity(audio_data):
                # Process audio with Whisper
                result = await speech_processor.process_audio(audio_data)
                await websocket.send_json({"transcript": result["text"]})
            
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
