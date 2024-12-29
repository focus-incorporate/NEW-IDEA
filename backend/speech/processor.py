import torch
import whisper
from typing import Optional, Dict
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechProcessor:
    def __init__(self, model_name: str = "base", device: Optional[str] = None):
        """Initialize the speech processor with Whisper model.
        
        Args:
            model_name: Whisper model size ("tiny", "base", "small", "medium", "large")
            device: Device to run the model on ("cuda" or "cpu")
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Loading Whisper model '{model_name}' on {self.device}")
        
        try:
            self.model = whisper.load_model(model_name).to(self.device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    async def process_audio(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Dict:
        """Process audio data and return transcription.
        
        Args:
            audio_data: Audio data as numpy array
            sample_rate: Sample rate of the audio
        
        Returns:
            Dictionary containing transcription and metadata
        """
        try:
            # Ensure audio data is in the correct format
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio
            if np.abs(audio_data).max() > 1.0:
                audio_data = audio_data / np.abs(audio_data).max()

            # Process with Whisper
            result = self.model.transcribe(
                audio_data,
                language="en",
                task="transcribe",
                fp16=torch.cuda.is_available()
            )

            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"],
                "success": True
            }

        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def process_stream(self, audio_stream: bytes) -> Dict:
        """Process audio stream in real-time.
        
        Args:
            audio_stream: Raw audio stream bytes
        
        Returns:
            Dictionary containing transcription and metadata
        """
        try:
            # Convert audio stream to numpy array
            audio_data = np.frombuffer(audio_stream, dtype=np.float32)
            return await self.process_audio(audio_data)
        
        except Exception as e:
            logger.error(f"Error processing audio stream: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'model'):
            # Clear CUDA cache if using GPU
            if self.device == "cuda":
                torch.cuda.empty_cache()
            
            # Delete model
            del self.model
            logger.info("Speech processor cleaned up")
