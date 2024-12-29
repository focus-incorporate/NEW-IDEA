from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional
import json
import asyncio
import logging
from pathlib import Path

from ..speech.processor import SpeechProcessor
from ..llm.engine import LLMEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceAssistant:
    def __init__(self, llm_model_path: str, whisper_model: str = "base"):
        """Initialize the voice assistant with speech and LLM processors.
        
        Args:
            llm_model_path: Path to the local LLM model
            whisper_model: Whisper model size
        """
        try:
            self.speech_processor = SpeechProcessor(model_name=whisper_model)
            self.llm_engine = LLMEngine(model_path=llm_model_path)
            logger.info("Voice assistant initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize voice assistant: {e}")
            raise

        self.active_conversations: Dict[str, list] = {}

    async def process_voice_input(self, client_id: str, audio_data: bytes) -> Dict:
        """Process voice input and generate response.
        
        Args:
            client_id: Unique identifier for the client
            audio_data: Raw audio data
        
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Process speech to text
            transcription = await self.speech_processor.process_stream(audio_data)
            
            if not transcription["success"]:
                yield {
                    "success": False,
                    "error": "Failed to transcribe audio"
                }
                return

            # Get conversation context
            context = self.active_conversations.get(client_id, [])
            
            # Generate LLM response
            async for response in self.llm_engine.generate_response(
                transcription["text"],
                context=context,
                stream=True
            ):
                yield response

                # Update conversation history if response is complete
                if response.get("finished"):
                    self._update_conversation(client_id, transcription["text"], response["text"])

        except Exception as e:
            logger.error(f"Error processing voice input: {e}")
            yield {
                "success": False,
                "error": str(e)
            }

    def _update_conversation(self, client_id: str, user_input: str, assistant_response: str):
        """Update conversation history for a client."""
        if client_id not in self.active_conversations:
            self.active_conversations[client_id] = []
            
        conversation = self.active_conversations[client_id]
        conversation.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response}
        ])
        
        # Keep only last 10 messages for context
        self.active_conversations[client_id] = conversation[-10:]

    def cleanup(self):
        """Cleanup resources."""
        self.speech_processor.cleanup()
        self.llm_engine.cleanup()
        logger.info("Voice assistant cleaned up")
