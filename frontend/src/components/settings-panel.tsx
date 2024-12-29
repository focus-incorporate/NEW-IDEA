'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface SettingsPanelProps {
  isOpen: boolean
  onClose: () => void
}

export function SettingsPanel({ isOpen, onClose }: SettingsPanelProps) {
  const [settings, setSettings] = useState({
    voiceActivityDetection: true,
    noiseSuppression: true,
    echoCancellation: true,
    autoGainControl: true,
    silenceThreshold: -45,
    maxAudioDuration: 30000,
  })

  const handleSettingChange = (key: keyof typeof settings, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }))
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            onClick={onClose}
          />

          {/* Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 20 }}
            className="fixed right-0 top-0 h-full w-80 bg-gray-900 border-l border-gray-800 p-6 shadow-xl z-50"
          >
            <div className="flex flex-col h-full">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-white">Settings</h2>
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              <div className="space-y-6">
                {/* Voice Activity Detection */}
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-300">
                    Voice Activity Detection
                  </label>
                  <Switch
                    checked={settings.voiceActivityDetection}
                    onChange={(checked) =>
                      handleSettingChange('voiceActivityDetection', checked)
                    }
                  />
                </div>

                {/* Noise Suppression */}
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-300">
                    Noise Suppression
                  </label>
                  <Switch
                    checked={settings.noiseSuppression}
                    onChange={(checked) =>
                      handleSettingChange('noiseSuppression', checked)
                    }
                  />
                </div>

                {/* Echo Cancellation */}
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-300">
                    Echo Cancellation
                  </label>
                  <Switch
                    checked={settings.echoCancellation}
                    onChange={(checked) =>
                      handleSettingChange('echoCancellation', checked)
                    }
                  />
                </div>

                {/* Auto Gain Control */}
                <div className="flex items-center justify-between">
                  <label className="text-sm text-gray-300">
                    Auto Gain Control
                  </label>
                  <Switch
                    checked={settings.autoGainControl}
                    onChange={(checked) =>
                      handleSettingChange('autoGainControl', checked)
                    }
                  />
                </div>

                {/* Silence Threshold */}
                <div className="space-y-2">
                  <label className="text-sm text-gray-300">
                    Silence Threshold (dB)
                  </label>
                  <input
                    type="range"
                    min="-60"
                    max="-30"
                    value={settings.silenceThreshold}
                    onChange={(e) =>
                      handleSettingChange('silenceThreshold', Number(e.target.value))
                    }
                    className="w-full"
                  />
                  <div className="text-sm text-gray-400">
                    {settings.silenceThreshold} dB
                  </div>
                </div>

                {/* Max Audio Duration */}
                <div className="space-y-2">
                  <label className="text-sm text-gray-300">
                    Max Audio Duration (ms)
                  </label>
                  <input
                    type="number"
                    value={settings.maxAudioDuration}
                    onChange={(e) =>
                      handleSettingChange('maxAudioDuration', Number(e.target.value))
                    }
                    className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm"
                  />
                </div>
              </div>

              <div className="mt-auto">
                <button
                  onClick={onClose}
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white rounded-lg px-4 py-2 transition-colors"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

// Switch Component
function Switch({
  checked,
  onChange,
}: {
  checked: boolean
  onChange: (checked: boolean) => void
}) {
  return (
    <button
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`
        relative inline-flex h-6 w-11 items-center rounded-full transition-colors
        ${checked ? 'bg-blue-500' : 'bg-gray-700'}
      `}
    >
      <span
        className={`
          inline-block h-4 w-4 transform rounded-full bg-white transition-transform
          ${checked ? 'translate-x-6' : 'translate-x-1'}
        `}
      />
    </button>
  )
}
