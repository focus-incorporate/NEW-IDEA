'use client';

import VoiceInterface from '@/components/VoiceInterface';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

export default function Home() {
  const [isActive, setIsActive] = useState(false);

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-400">
            AI Voice Assistant
          </h1>
          <p className="text-gray-400">
            Powered by Next.js and AI
          </p>
        </header>

        <div className="bg-gray-800/50 rounded-2xl p-8 backdrop-blur-sm shadow-xl border border-gray-700">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${isActive ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-sm text-gray-400">
                {isActive ? 'Listening' : 'Idle'}
              </span>
            </div>
            <Button
              variant="outline"
              className="text-sm"
              onClick={() => setIsActive(!isActive)}
            >
              {isActive ? 'Stop' : 'Start'}
            </Button>
          </div>

          <VoiceInterface onTranscriptUpdate={(transcript) => {
             console.log('Transcript updated:', transcript);
             // You can update state or UI based on transcript here
           }} />

          <div className="mt-8 pt-6 border-t border-gray-700">
            <h3 className="text-lg font-semibold mb-4">Assistant Status</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-400">Status:</span>
                <span className="ml-2">{isActive ? 'Processing voice input' : 'Ready'}</span>
              </div>
              <div>
                <span className="text-gray-400">Mode:</span>
                <span className="ml-2">Voice Recognition</span>
              </div>
            </div>
          </div>
        </div>

        <footer className="mt-8 text-center text-sm text-gray-500">
          <p>
            Built with Next.js and Modern UI Components
          </p>
        </footer>
      </div>
    </main>
  );
}
