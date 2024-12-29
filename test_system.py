import asyncio
import websockets
import json
import numpy as np
import sounddevice as sd
import time
from datetime import datetime

async def test_voice_assistant():
    print("\n=== Voice Assistant System Test ===\n")
    
    # Test 1: Connect to WebSocket
    print("Test 1: WebSocket Connection")
    try:
        uri = "ws://localhost:8000/ws/test-client"
        async with websockets.connect(uri) as websocket:
            print("✓ WebSocket connection successful")
            
            # Test 2: Send Audio Data
            print("\nTest 2: Audio Processing")
            # Generate test audio (1 second of 440Hz tone)
            sample_rate = 16000
            duration = 1.0
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * 440 * t)
            audio_bytes = audio_data.astype(np.float32).tobytes()
            
            # Send audio data
            await websocket.send(audio_bytes)
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("success"):
                print("✓ Audio processing successful")
                print(f"Response: {json.dumps(response_data, indent=2)}")
            else:
                print("✗ Audio processing failed")
                print(f"Error: {response_data.get('error')}")
            
            # Test 3: Emotion Detection
            print("\nTest 3: Emotion Detection")
            # Send audio for emotion detection
            await websocket.send(audio_bytes)
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if "emotions" in response_data:
                print("✓ Emotion detection successful")
                print(f"Emotions: {json.dumps(response_data['emotions'], indent=2)}")
            else:
                print("✗ Emotion detection failed")
            
            # Test 4: Speaker Identification
            print("\nTest 4: Speaker Identification")
            await websocket.send(audio_bytes)
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if "embedding" in response_data:
                print("✓ Speaker identification successful")
                print("Speaker embedding generated")
            else:
                print("✗ Speaker identification failed")
            
            # Test 5: Groq Integration
            print("\nTest 5: Groq Integration")
            test_message = json.dumps({
                "type": "text",
                "data": "Hello, how are you?"
            })
            await websocket.send(test_message)
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("text"):
                print("✓ Groq integration successful")
                print(f"Response: {response_data['text']}")
            else:
                print("✗ Groq integration failed")
                
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False
    
    # Test 6: Check Monitoring
    print("\nTest 6: Monitoring Endpoints")
    try:
        import requests
        metrics_response = requests.get("http://localhost:9090/metrics")
        if metrics_response.status_code == 200:
            print("✓ Prometheus metrics available")
        else:
            print("✗ Prometheus metrics unavailable")
            
        grafana_response = requests.get("http://localhost:3000")
        if grafana_response.status_code == 200:
            print("✓ Grafana dashboard available")
        else:
            print("✗ Grafana dashboard unavailable")
    except Exception as e:
        print(f"✗ Monitoring test failed: {str(e)}")
    
    print("\n=== Test Summary ===")
    print("Tests completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return True

if __name__ == "__main__":
    print("Starting system test...")
    asyncio.run(test_voice_assistant())
