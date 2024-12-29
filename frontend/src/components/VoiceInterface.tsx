"use client"

import React, { useRef, useState, useEffect } from 'react'
import { LocalTrack, Track, createLocalTracks } from 'livekit-client'
import { useLiveKit } from '../contexts/LiveKitContext'
import { Button } from './ui/button'
import { useToast } from './ui/use-toast'
import { cn } from '@/lib/utils'
import { logger } from '../utils/logger';
import { handleError, handleAudioError, AppError, ErrorCodes } from '../utils/errorHandler';

export default function VoiceInterface({ onTranscriptUpdate }: { onTranscriptUpdate: (transcript: string) => void }) {
  const { room, isConnected } = useLiveKit()
  const [isListening, setIsListening] = useState(false)
  const localAudioRef = useRef<LocalTrack | null>(null)
  const { toast } = useToast()
  const [transcript, setTranscript] = useState('')
  const [error, setError] = useState<AppError | null>(null)

  useEffect(() => {
    onTranscriptUpdate?.(transcript);
  }, [transcript, onTranscriptUpdate]);

  const startListening = async () => {
    try {
      if (!room || !room.localParticipant) {
        toast({
          title: "Error",
          description: "Not connected to room",
          variant: "destructive",
        })
        return
      }

      // Create local audio track
      const tracks = await createLocalTracks({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }, 
        video: false,
      })

      if (tracks.length > 0) {
        localAudioRef.current = tracks[0]
        
        // Publish the track
        await room.localParticipant.publishTrack(tracks[0], {
          name: 'microphone',
          dtx: true, // Enable Opus DTX for better bandwidth usage
          red: true, // Enable redundant coding for better quality
        })
        
        setIsListening(true)
        toast({
          title: "Success",
          description: "Microphone activated",
        })
      }
    } catch (error) {
      console.error('Error starting listening:', error)
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to start microphone",
        variant: "destructive",
      })
      setError(handleAudioError(error));
      setIsListening(false);
    }
  }

  const stopListening = async () => {
    try {
      if (!room?.localParticipant || !localAudioRef.current) {
        return
      }

      // Unpublish the track
      await room.localParticipant.unpublishTrack(localAudioRef.current)
      
      // Stop the track to release the microphone
      localAudioRef.current.stop()
      localAudioRef.current = null
      
      setIsListening(false)
      toast({
        title: "Success",
        description: "Microphone deactivated",
      })
    } catch (error) {
      console.error('Error stopping listening:', error)
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to stop microphone",
        variant: "destructive",
      })
      setError(handleError(error, 'stopListening'));
    }
  }

  useEffect(() => {
    if (!room) return;

    const handleData = (data: Uint8Array) => {
      const response = JSON.parse(new TextDecoder().decode(data));
      if (response.transcript) {
        setTranscript(prev => prev + ' ' + response.transcript);
      }
    };

    room.on('dataReceived', handleData);

    return () => {
      room.off('dataReceived', handleData);
    };
  }, [room]);

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      {error && (
        <div className="text-red-500 text-center p-3 bg-red-950/30 rounded-lg border border-red-900/50">
          {error.message}
        </div>
      )}
      
      <h2 className="text-2xl font-bold mb-4">Voice Interface</h2>
      
      {!isConnected && (
        <div className="text-yellow-600 dark:text-yellow-400 mb-4">
          Not connected to room
        </div>
      )}
      
      <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
        <h3 className="text-lg font-semibold mb-3 text-gray-200">Transcript:</h3>
        <p className="text-gray-300 whitespace-pre-wrap min-h-[100px] font-mono text-sm">
          {transcript || 'No transcript available'}
        </p>
      </div>
      
      <Button
        onClick={isListening ? stopListening : startListening}
        disabled={!isConnected}
        variant={isListening ? "destructive" : "default"}
        className={cn(
          "w-32",
          isListening && "animate-pulse"
        )}
      >
        {isListening ? "Stop" : "Start"}
      </Button>
      
      {isListening && (
        <div className="text-green-600 dark:text-green-400 animate-pulse">
          Listening...
        </div>
      )}
    </div>
  )
}
