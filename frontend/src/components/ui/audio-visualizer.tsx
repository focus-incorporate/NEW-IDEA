'use client'

import { useEffect, useRef } from 'react'

interface AudioVisualizerProps {
  isListening: boolean
  className?: string
}

export function AudioVisualizer({ isListening, className }: AudioVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationFrameRef = useRef<number>()
  const analyserRef = useRef<AnalyserNode | null>(null)
  const dataArrayRef = useRef<Uint8Array | null>(null)

  useEffect(() => {
    let audioContext: AudioContext | null = null
    let mediaStream: MediaStream | null = null

    const setupAudioContext = async () => {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
        audioContext = new AudioContext()
        const source = audioContext.createMediaStreamSource(mediaStream)
        const analyser = audioContext.createAnalyser()
        
        analyser.fftSize = 256
        source.connect(analyser)
        analyserRef.current = analyser
        dataArrayRef.current = new Uint8Array(analyser.frequencyBinCount)
        
        animate()
      } catch (error) {
        console.error('Error accessing microphone:', error)
      }
    }

    const animate = () => {
      if (!canvasRef.current || !analyserRef.current || !dataArrayRef.current) return

      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      const draw = () => {
        const WIDTH = canvas.width
        const HEIGHT = canvas.height

        animationFrameRef.current = requestAnimationFrame(draw)

        analyserRef.current!.getByteFrequencyData(dataArrayRef.current!)
        ctx.fillStyle = 'rgb(20, 20, 30)'
        ctx.fillRect(0, 0, WIDTH, HEIGHT)

        const barWidth = (WIDTH / dataArrayRef.current!.length) * 2.5
        let barHeight
        let x = 0

        for (let i = 0; i < dataArrayRef.current!.length; i++) {
          barHeight = (dataArrayRef.current![i] / 255) * HEIGHT

          const gradient = ctx.createLinearGradient(0, 0, 0, HEIGHT)
          gradient.addColorStop(0, '#60A5FA') // blue-400
          gradient.addColorStop(1, '#2DD4BF') // teal-400

          ctx.fillStyle = gradient
          ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight)

          x += barWidth + 1
        }
      }

      draw()
    }

    if (isListening) {
      setupAudioContext()
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
      if (audioContext) {
        audioContext.close()
      }
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop())
      }
    }
  }, [isListening])

  return (
    <canvas
      ref={canvasRef}
      className={className}
      width={300}
      height={100}
    />
  )
}
