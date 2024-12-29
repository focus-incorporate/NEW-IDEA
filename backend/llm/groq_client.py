import groq
from typing import AsyncGenerator, Dict, List, Optional
import logging
import json
import asyncio
from ..config.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        """Initialize Groq client with API key."""
        self.client = groq.AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        logger.info(f"Initialized Groq client with model: {self.model}")

    async def generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> AsyncGenerator[Dict, None]:
        """Generate response from Groq.
        
        Args:
            prompt: User input prompt
            context: Previous conversation context
            stream: Whether to stream the response
            temperature: Temperature for response generation
            max_tokens: Maximum tokens to generate
        
        Yields:
            Dictionary containing response chunks and metadata
        """
        try:
            messages = self._prepare_messages(prompt, context)
            
            chat_params = {
                "messages": messages,
                "model": self.model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }

            if stream:
                async for chunk in await self.client.chat.completions.create(**chat_params):
                    if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta.content:
                        yield {
                            "text": chunk.choices[0].delta.content,
                            "finished": False,
                            "success": True
                        }
                
                # Send final chunk
                yield {
                    "text": "",
                    "finished": True,
                    "success": True
                }
            else:
                response = await self.client.chat.completions.create(**chat_params)
                yield {
                    "text": response.choices[0].message.content,
                    "finished": True,
                    "success": True
                }

        except Exception as e:
            logger.error(f"Error generating response from Groq: {e}")
            yield {
                "success": False,
                "error": str(e)
            }

    def _prepare_messages(self, prompt: str, context: Optional[List[Dict]] = None) -> List[Dict]:
        """Prepare messages for Groq chat completion.
        
        Args:
            prompt: Current user prompt
            context: Previous conversation context
        
        Returns:
            List of message dictionaries
        """
        messages = []
        
        # Add system message
        messages.append({
            "role": "system",
            "content": "You are a helpful and knowledgeable voice assistant. Provide clear, concise, and accurate responses."
        })
        
        # Add conversation context
        if context:
            messages.extend(context)
        
        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        return messages

    async def close(self):
        """Close the Groq client session."""
        if hasattr(self, 'client'):
            await self.client.close()
            logger.info("Groq client session closed")
