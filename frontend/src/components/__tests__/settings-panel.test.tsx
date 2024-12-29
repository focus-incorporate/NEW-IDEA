import { render, screen, fireEvent } from '@testing-library/react'
import { SettingsPanel } from '../settings-panel'

// Mock framer-motion to avoid animation issues in tests
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  },
  AnimatePresence: ({ children }: any) => <>{children}</>,
}))

describe('SettingsPanel', () => {
  const mockOnClose = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders when isOpen is true', () => {
    render(<SettingsPanel isOpen={true} onClose={mockOnClose} />)
    
    expect(screen.getByText('Settings')).toBeInTheDocument()
    expect(screen.getByText('Voice Activity Detection')).toBeInTheDocument()
    expect(screen.getByText('Noise Suppression')).toBeInTheDocument()
  })

  it('does not render when isOpen is false', () => {
    render(<SettingsPanel isOpen={false} onClose={mockOnClose} />)
    
    expect(screen.queryByText('Settings')).not.toBeInTheDocument()
  })

  it('calls onClose when close button is clicked', () => {
    render(<SettingsPanel isOpen={true} onClose={mockOnClose} />)
    
    const closeButton = screen.getByRole('button', { name: /close/i })
    fireEvent.click(closeButton)
    
    expect(mockOnClose).toHaveBeenCalledTimes(1)
  })

  it('toggles switches correctly', () => {
    render(<SettingsPanel isOpen={true} onClose={mockOnClose} />)
    
    const vadSwitch = screen.getByRole('switch', {
      name: /voice activity detection/i,
    })
    
    // Initially on
    expect(vadSwitch).toHaveAttribute('aria-checked', 'true')
    
    // Toggle off
    fireEvent.click(vadSwitch)
    expect(vadSwitch).toHaveAttribute('aria-checked', 'false')
    
    // Toggle on
    fireEvent.click(vadSwitch)
    expect(vadSwitch).toHaveAttribute('aria-checked', 'true')
  })

  it('updates slider value', () => {
    render(<SettingsPanel isOpen={true} onClose={mockOnClose} />)
    
    const slider = screen.getByRole('slider')
    fireEvent.change(slider, { target: { value: '-50' } })
    
    expect(screen.getByText('-50 dB')).toBeInTheDocument()
  })

  it('updates max audio duration', () => {
    render(<SettingsPanel isOpen={true} onClose={mockOnClose} />)
    
    const input = screen.getByRole('spinbutton')
    fireEvent.change(input, { target: { value: '20000' } })
    
    expect(input).toHaveValue(20000)
  })

  it('closes panel when backdrop is clicked', () => {
    render(<SettingsPanel isOpen={true} onClose={mockOnClose} />)
    
    const backdrop = screen.getByTestId('backdrop')
    fireEvent.click(backdrop)
    
    expect(mockOnClose).toHaveBeenCalledTimes(1)
  })
})
