from typing import Dict, Optional, List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
from pathlib import Path
import json
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(
        self,
        model_path: str,
        device: Optional[str] = None,
        max_length: int = 2048,
        temperature: float = 0.7
    ):
        """Initialize the LLM engine.
        
        Args:
            model_path: Path to the local LLM model
            device: Device to run the model on ("cuda" or "cpu")
            max_length: Maximum length for generated responses
            temperature: Temperature for response generation
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = max_length
        self.temperature = temperature
        
        logger.info(f"Loading LLM model from {model_path} on {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                low_cpu_mem_usage=True
            ).to(self.device)
            
            logger.info("LLM model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load LLM model: {e}")
            raise

    async def generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict]] = None,
        stream: bool = True
    ) -> Dict:
        """Generate response from the LLM.
        
        Args:
            prompt: User input prompt
            context: Previous conversation context
            stream: Whether to stream the response
        
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Prepare conversation history
            conversation = self._prepare_conversation(prompt, context)
            
            # Tokenize input
            inputs = self.tokenizer(conversation, return_tensors="pt").to(self.device)
            
            # Generate response
            response_ids = await self._generate_response_ids(inputs)
            
            if stream:
                async for response in self._stream_response(response_ids):
                    yield response
            else:
                response = self._decode_response(response_ids)
                yield {
                    "text": response,
                    "finished": True,
                    "success": True
                }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield {
                "success": False,
                "error": str(e)
            }

    def _prepare_conversation(self, prompt: str, context: Optional[List[Dict]] = None) -> str:
        """Prepare conversation history for the model."""
        if not context:
            return f"User: {prompt}\nAssistant:"
        
        conversation = ""
        for message in context:
            role = message.get("role", "user")
            content = message.get("content", "")
            conversation += f"{role.capitalize()}: {content}\n"
        
        conversation += f"User: {prompt}\nAssistant:"
        return conversation

    async def _generate_response_ids(self, inputs: Dict) -> torch.Tensor:
        """Generate response token IDs."""
        with torch.no_grad():
            output_ids = self.model.generate(
                inputs.input_ids,
                max_length=self.max_length,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                attention_mask=inputs.attention_mask
            )
        return output_ids[0][inputs.input_ids.shape[1]:]

    async def _stream_response(self, response_ids: torch.Tensor):
        """Stream response tokens."""
        response = ""
        for i in range(len(response_ids)):
            new_token = self.tokenizer.decode(response_ids[i:i+1], skip_special_tokens=True)
            response += new_token
            
            yield {
                "text": response,
                "finished": i == len(response_ids) - 1,
                "success": True
            }
            await asyncio.sleep(0.01)  # Prevent blocking

    def _decode_response(self, response_ids: torch.Tensor) -> str:
        """Decode response tokens to text."""
        return self.tokenizer.decode(response_ids, skip_special_tokens=True)

    def cleanup(self):
        """Cleanup resources."""
        if hasattr(self, 'model'):
            # Clear CUDA cache if using GPU
            if self.device == "cuda":
                torch.cuda.empty_cache()
            
            # Delete model and tokenizer
            del self.model
            del self.tokenizer
            logger.info("LLM engine cleaned up")
