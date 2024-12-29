// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom'

// Mock IntersectionObserver
class IntersectionObserver {
  observe = jest.fn()
  disconnect = jest.fn()
  unobserve = jest.fn()
}

Object.defineProperty(window, 'IntersectionObserver', {
  writable: true,
  configurable: true,
  value: IntersectionObserver,
})

Object.defineProperty(global, 'IntersectionObserver', {
  writable: true,
  configurable: true,
  value: IntersectionObserver,
})

// Mock AudioContext
class AudioContext {
  createAnalyser = jest.fn(() => ({
    connect: jest.fn(),
    disconnect: jest.fn(),
    fftSize: 0,
    frequencyBinCount: 0,
    getByteFrequencyData: jest.fn(),
  }))
  createMediaStreamSource = jest.fn(() => ({
    connect: jest.fn(),
    disconnect: jest.fn(),
  }))
  close = jest.fn()
}

window.AudioContext = AudioContext

// Mock MediaStream
window.MediaStream = jest.fn().mockImplementation(() => ({
  getTracks: () => [{
    stop: jest.fn()
  }]
}))

// Mock getUserMedia
window.navigator.mediaDevices = {
  getUserMedia: jest.fn().mockImplementation(() =>
    Promise.resolve(new window.MediaStream())
  )
}

// Mock requestAnimationFrame
global.requestAnimationFrame = jest.fn().mockImplementation(cb => setTimeout(cb, 0))
global.cancelAnimationFrame = jest.fn().mockImplementation(id => clearTimeout(id))
