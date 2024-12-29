import pytest
from fastapi.testclient import TestClient
import numpy as np
from backend.api.main import app
from backend.speech.voice_detection import VoiceDetector
from backend.speech.advanced_features import VoiceFeatureAnalyzer
from backend.llm.groq_client import GroqClient

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def voice_detector():
    return VoiceDetector()

@pytest.fixture
def feature_analyzer():
    return VoiceFeatureAnalyzer()

@pytest.fixture
def groq_client():
    return GroqClient()

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Voice Assistant API is running"}

@pytest.mark.asyncio
async def test_voice_detection(voice_detector):
    # Create sample audio data
    sample_rate = 16000
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Convert to bytes
    audio_bytes = audio_data.astype(np.float32).tobytes()
    
    # Test voice activity detection
    result = voice_detector.detect_voice_activity(audio_bytes)
    assert isinstance(result, bool)

@pytest.mark.asyncio
async def test_emotion_detection(feature_analyzer):
    # Create sample audio data
    sample_rate = 16000
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)
    
    # Test emotion analysis
    result = await feature_analyzer.analyze_emotion(audio_data)
    assert result["success"] is True
    assert "emotions" in result

@pytest.mark.asyncio
async def test_speaker_identification(feature_analyzer):
    # Create sample audio data
    sample_rate = 16000
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)
    
    # Test speaker identification without reference
    result = await feature_analyzer.identify_speaker(audio_data)
    assert result["success"] is True
    assert "embedding" in result

@pytest.mark.asyncio
async def test_groq_client(groq_client):
    # Test simple prompt
    prompt = "Hello, how are you?"
    response_generator = groq_client.generate_response(prompt, stream=False)
    
    response = None
    async for r in response_generator:
        response = r
        break
    
    assert response is not None
    assert response["success"] is True
    assert "text" in response

def test_websocket_connection(client):
    with client.websocket_connect("/ws/test-client") as websocket:
        # Test connection is established
        assert websocket.client is not None
