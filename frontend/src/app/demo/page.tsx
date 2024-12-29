'use client'

import { useEffect, useState } from 'react'
import { useLiveKit } from '@/contexts/LiveKitContext'
import VoiceInterface from '@/components/VoiceInterface'

export default function DemoPage() {
  const { connectToRoom, disconnect, isConnected, error } = useLiveKit()
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const autoConnect = async () => {
      try {
        setIsLoading(true)
        // In production, fetch this token from your backend
        const token = 'your-test-token'
        await connectToRoom(token, {
          autoSubscribe: true,
        })
      } catch (err) {
        console.error('Failed to connect:', err)
      } finally {
        setIsLoading(false)
      }
    }

    autoConnect()

    return () => {
      disconnect()
    }
  }, [connectToRoom, disconnect])

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-400">
            Voice Assistant Demo
          </h1>
          <p className="text-gray-400">
            Experience real-time voice interaction
          </p>
        </header>

        <div className="bg-gray-800/50 rounded-2xl p-8 backdrop-blur-sm shadow-xl border border-gray-700">
          {/* Connection Status */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <div 
                className={`w-3 h-3 rounded-full ${
                  isLoading 
                    ? 'bg-yellow-500' 
                    : isConnected 
                    ? 'bg-green-500' 
                    : 'bg-red-500'
                }`} 
              />
              <span className="text-sm text-gray-400">
                {isLoading 
                  ? 'Connecting...' 
                  : isConnected 
                  ? 'Connected' 
                  : 'Disconnected'}
              </span>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-6 p-4 bg-red-900/20 border border-red-900/50 rounded-lg text-red-400">
              {error}
            </div>
          )}

          {/* Voice Interface */}
          <VoiceInterface onTranscriptUpdate={(transcript) => {
            console.log('Transcript updated:', transcript);
          }} />
        </div>

        {/* Features Section */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <FeatureCard
            title="Real-time Processing"
            description="Experience instant voice recognition and response with minimal latency"
          />
          <FeatureCard
            title="High Quality Audio"
            description="Crystal clear audio streaming with noise suppression"
          />
          <FeatureCard
            title="Secure Connection"
            description="End-to-end encrypted communication for your privacy"
          />
        </div>
      </div>
    </main>
  )
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="p-6 bg-gray-800/30 rounded-xl border border-gray-700">
      <h3 className="text-lg font-semibold mb-2 text-gray-200">{title}</h3>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  )
}
