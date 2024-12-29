import numpy as np
import webrtcvad
import torch
from transformers import pipeline
import logging
from ..config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class VoiceDetector:
    def __init__(self):
        """Initialize voice activity and wake word detection."""
        self.vad = webrtcvad.Vad(3)  # Aggressiveness level 3 (highest)
        
        if settings.WAKE_WORD_ENABLED:
            # Initialize wake word detection model
            try:
                self.wake_word_detector = pipeline(
                    "audio-classification",
                    model="microsoft/wav2vec2-base-960h"
                )
                logger.info("Wake word detection initialized")
            except Exception as e:
                logger.error(f"Failed to initialize wake word detection: {e}")
                self.wake_word_detector = None

    def detect_voice_activity(self, audio_frame: bytes) -> bool:
        """Detect if there is voice activity in the audio frame.
        
        Args:
            audio_frame: Raw audio frame bytes
        
        Returns:
            True if voice activity detected, False otherwise
        """
        try:
            return self.vad.is_speech(audio_frame, settings.SAMPLE_RATE)
        except Exception as e:
            logger.error(f"Error detecting voice activity: {e}")
            return False

    async def detect_wake_word(self, audio_data: np.ndarray) -> bool:
        """Detect wake word in audio data.
        
        Args:
            audio_data: Audio data as numpy array
        
        Returns:
            True if wake word detected, False otherwise
        """
        if not settings.WAKE_WORD_ENABLED or not self.wake_word_detector:
            return True

        try:
            # Convert audio data to proper format
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)

            # Normalize audio
            if np.abs(audio_data).max() > 1.0:
                audio_data = audio_data / np.abs(audio_data).max()

            # Run wake word detection
            result = self.wake_word_detector(audio_data)
            
            # Check if any of the predictions match our wake word
            for pred in result:
                if pred["score"] > settings.VAD_THRESHOLD and \
                   pred["label"].lower() in settings.WAKE_WORD_PHRASE.lower():
                    return True
            
            return False

        except Exception as e:
            logger.error(f"Error detecting wake word: {e}")
            return False

    def preprocess_audio(self, audio_data: bytes) -> np.ndarray:
        """Preprocess audio data for voice detection.
        
        Args:
            audio_data: Raw audio data bytes
        
        Returns:
            Preprocessed audio data as numpy array
        """
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Convert to float32 and normalize
            audio_float = audio_array.astype(np.float32) / 32768.0
            
            return audio_float
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            return np.array([])
