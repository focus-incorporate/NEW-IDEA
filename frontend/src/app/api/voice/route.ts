import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const audioData = await request.arrayBuffer();
    
    // Forward the audio data to your Python backend
    const response = await fetch('http://localhost:8000/process-audio', {
      method: 'POST',
      body: audioData,
      headers: {
        'Content-Type': 'audio/raw',
      },
    });

    const result = await response.json();
    return NextResponse.json(result);
  } catch (error) {
    console.error('Error processing audio:', error);
    return NextResponse.json(
      { error: 'Failed to process audio' },
      { status: 500 }
    );
  }
}
