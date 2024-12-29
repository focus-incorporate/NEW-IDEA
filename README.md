# AI Voice Assistant

A modern voice assistant application built with Next.js, FastAPI, and LiveKit for real-time audio streaming.

## Features

- Real-time voice recognition
- Modern UI with glass-morphism design
- LiveKit integration for audio streaming
- Voice activity detection
- Real-time transcription using Whisper
- Scalable architecture

## Tech Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn/ui components
- LiveKit for audio streaming

### Backend
- FastAPI
- Python 3.9+
- Whisper for speech recognition
- WebSocket for real-time communication

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NEW\ IDEA
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Running the Application

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. (Optional) Start LiveKit server using Docker:
```bash
docker run --rm -p 7880:7880 livekit/livekit-server
```

The application will be available at http://localhost:3000

## Project Structure

```
.
├── frontend/                # Next.js frontend application
│   ├── src/
│   │   ├── app/            # Next.js app directory
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   └── lib/           # Utility functions
│   └── public/            # Static assets
├── backend/               # FastAPI backend application
│   ├── api/              # API endpoints
│   ├── speech/           # Speech processing modules
│   └── llm/             # Language model integration
└── docker-compose.yml    # Docker compose configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
