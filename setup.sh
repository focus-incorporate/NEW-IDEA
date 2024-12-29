#!/bin/bash

# Exit on error
set -e

echo "Setting up Voice Assistant project..."

# Create necessary directories
mkdir -p backend/logs
mkdir -p frontend/logs

# Set proper permissions
chmod 755 backend/logs
chmod 755 frontend/logs

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
python3 -m pip install -r requirements.txt

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd ../frontend
npm install

# Create environment files if they don't exist
if [ ! -f .env.local ]; then
    echo "Creating frontend environment file..."
    cat > .env.local << EOL
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
NEXT_PUBLIC_VOICE_ASSISTANT_NAME=AI Assistant
NEXT_PUBLIC_MAX_AUDIO_DURATION_MS=10000
NEXT_PUBLIC_SILENCE_THRESHOLD_DB=-45
EOL
fi

cd ../backend
if [ ! -f .env ]; then
    echo "Creating backend environment file..."
    cat > .env << EOL
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
WHISPER_MODEL=base
DATABASE_URL=sqlite:///./voice_assistant.db
LOG_LEVEL=DEBUG
EOL
fi

echo "Setup completed successfully!"
