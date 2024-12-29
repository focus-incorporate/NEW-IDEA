import torch
from transformers import pipeline
import librosa
import numpy as np
from typing import Dict, Tuple
import logging
from ..config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class VoiceFeatureAnalyzer:
    def __init__(self):
        """Initialize voice feature analyzers."""
        try:
            # Initialize emotion detection
            self.emotion_detector = pipeline(
                "audio-classification",
                model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
            )
            
            # Initialize speaker identification
            self.speaker_identifier = pipeline(
                "audio-classification",
                model="microsoft/wav2vec2-base-960h"
            )
            
            logger.info("Voice feature analyzers initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize voice feature analyzers: {e}")
            raise

    async def analyze_emotion(self, audio_data: np.ndarray) -> Dict[str, float]:
        """Analyze emotion in speech.
        
        Args:
            audio_data: Audio data as numpy array
        
        Returns:
            Dictionary of emotion probabilities
        """
        try:
            # Ensure proper audio format
            audio_data = self._preprocess_audio(audio_data)
            
            # Get emotion predictions
            predictions = self.emotion_detector(audio_data)
            
            # Convert to dictionary of emotion probabilities
            emotions = {
                pred["label"]: pred["score"]
                for pred in predictions
            }
            
            return {
                "success": True,
                "emotions": emotions
            }
            
        except Exception as e:
            logger.error(f"Error analyzing emotion: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def identify_speaker(
        self,
        audio_data: np.ndarray,
        reference_embeddings: Dict[str, np.ndarray] = None
    ) -> Dict:
        """Identify speaker from voice.
        
        Args:
            audio_data: Audio data as numpy array
            reference_embeddings: Dictionary of speaker embeddings for comparison
        
        Returns:
            Dictionary with speaker identification results
        """
        try:
            # Ensure proper audio format
            audio_data = self._preprocess_audio(audio_data)
            
            # Extract speaker embedding
            embedding = await self._extract_speaker_embedding(audio_data)
            
            if reference_embeddings:
                # Compare with reference embeddings
                similarities = {
                    speaker: self._compute_similarity(embedding, ref_embedding)
                    for speaker, ref_embedding in reference_embeddings.items()
                }
                
                # Find best match
                best_match = max(similarities.items(), key=lambda x: x[1])
                
                return {
                    "success": True,
                    "speaker": best_match[0],
                    "confidence": best_match[1],
                    "similarities": similarities
                }
            else:
                # Return just the embedding for reference
                return {
                    "success": True,
                    "embedding": embedding.tolist()
                }
                
        except Exception as e:
            logger.error(f"Error identifying speaker: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _extract_speaker_embedding(self, audio_data: np.ndarray) -> np.ndarray:
        """Extract speaker embedding from audio."""
        # Get model predictions
        predictions = self.speaker_identifier(audio_data, output_hidden_states=True)
        
        # Use the last hidden state as speaker embedding
        embedding = predictions.hidden_states[-1].mean(dim=1).squeeze().numpy()
        return embedding

    def _compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between speaker embeddings."""
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

    def _preprocess_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Preprocess audio for feature extraction."""
        # Ensure float32 format
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        
        # Normalize if needed
        if np.abs(audio_data).max() > 1.0:
            audio_data = audio_data / np.abs(audio_data).max()
        
        return audio_data

    def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'emotion_detector'):
            del self.emotion_detector
        if hasattr(self, 'speaker_identifier'):
            del self.speaker_identifier
        torch.cuda.empty_cache()  # Clear CUDA cache if using GPU
        logger.info("Voice feature analyzer cleaned up")
