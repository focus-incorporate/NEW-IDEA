"use client"

import React, { createContext, useContext, useState, useEffect } from 'react'
import {
  Room,
  RoomEvent,
  LocalTrack,
  RoomConnectOptions,
  createLocalTracks,
  RoomOptions,
} from 'livekit-client'

type LiveKitContextType = {
  room: Room | null
  connectToRoom: (token: string, options?: RoomConnectOptions) => Promise<void>
  localTracks: LocalTrack[]
  disconnect: () => void
  isConnected: boolean
  error: string | null
}

const LiveKitContext = createContext<LiveKitContextType | undefined>(undefined)

export function LiveKitProvider({ children }: { children: React.ReactNode }) {
  const [room, setRoom] = useState<Room | null>(null)
  const [localTracks, setLocalTracks] = useState<LocalTrack[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    return () => {
      // Cleanup function to ensure we disconnect and clean up tracks
      if (room) {
        disconnect()
      }
      localTracks.forEach(track => track.stop())
    }
  }, [room, localTracks])

  const connectToRoom = async (token: string, options?: RoomConnectOptions) => {
    try {
      // If we've already created a room, disconnect first
      if (room) {
        await disconnect()
      }

      // Create a new room instance
      const newRoom = new Room({
        adaptiveStream: true,
        dynacast: true,
        stopLocalTrackOnUnpublish: true,
      })
      setRoom(newRoom)

      // Create local audio track
      const tracks = await createLocalTracks({
        audio: true,
        video: false,
      })

      setLocalTracks(tracks)

      // Set up room event handlers
      newRoom
        .on(RoomEvent.Connected, () => {
          console.log('Connected to room')
          setIsConnected(true)
          setError(null)
        })
        .on(RoomEvent.Disconnected, () => {
          console.log('Disconnected from room')
          setIsConnected(false)
          setRoom(null)
        })
        .on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
          console.log('Track subscribed:', track.sid)
        })
        .on(RoomEvent.TrackUnsubscribed, (track, publication, participant) => {
          console.log('Track unsubscribed:', track.sid)
        })
        .on(RoomEvent.ConnectionQualityChanged, (quality, participant) => {
          console.log('Connection quality changed:', quality)
        })
        .on(RoomEvent.MediaDevicesError, (e: Error) => {
          console.error('Media device error:', e)
          setError('Media device error: ' + e.message)
        })

      // Connect to LiveKit room
      await newRoom.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, token, options)
      
      // Publish local tracks
      await Promise.all(
        tracks.map(track => newRoom.localParticipant.publishTrack(track))
      )

      setIsConnected(true)
    } catch (error) {
      console.error('Error connecting to room:', error)
      setRoom(null)
      setIsConnected(false)
      setError(error instanceof Error ? error.message : 'Failed to connect to room')
      throw error
    }
  }

  const disconnect = async () => {
    try {
      if (room) {
        // Disconnect from the room
        room.disconnect()
        setRoom(null)
        setIsConnected(false)

        // Stop all local tracks
        localTracks.forEach(track => track.stop())
        setLocalTracks([])
      }
    } catch (error) {
      console.error('Error disconnecting from room:', error)
      setError(error instanceof Error ? error.message : 'Failed to disconnect from room')
      throw error
    }
  }

  const value: LiveKitContextType = {
    room,
    connectToRoom,
    localTracks,
    disconnect,
    isConnected,
    error
  }

  return (
    <LiveKitContext.Provider value={value}>
      {children}
    </LiveKitContext.Provider>
  )
}

export function useLiveKit() {
  const context = useContext(LiveKitContext)
  if (!context) {
    throw new Error('useLiveKit must be used within a LiveKitProvider')
  }
  return context
}
