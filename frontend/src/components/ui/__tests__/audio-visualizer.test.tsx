import { render, screen } from '@testing-library/react'
import { AudioVisualizer } from '../audio-visualizer'

describe('AudioVisualizer', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks()
  })

  it('renders canvas element', () => {
    render(<AudioVisualizer isListening={false} />)
    const canvas = screen.getByRole('img', { hidden: true })
    expect(canvas).toBeInTheDocument()
    expect(canvas.tagName.toLowerCase()).toBe('canvas')
  })

  it('initializes audio context when listening starts', () => {
    const { rerender } = render(<AudioVisualizer isListening={false} />)
    
    expect(window.navigator.mediaDevices.getUserMedia).not.toHaveBeenCalled()
    
    rerender(<AudioVisualizer isListening={true} />)
    
    expect(window.navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({
      audio: true,
    })
  })

  it('cleans up resources when unmounted', () => {
    const { unmount } = render(<AudioVisualizer isListening={true} />)
    
    unmount()
    
    // Verify that animation frame is cancelled
    expect(global.cancelAnimationFrame).toHaveBeenCalled()
  })

  it('applies custom className', () => {
    const customClass = 'test-class'
    render(<AudioVisualizer isListening={false} className={customClass} />)
    
    const canvas = screen.getByRole('img', { hidden: true })
    expect(canvas).toHaveClass(customClass)
  })
})
