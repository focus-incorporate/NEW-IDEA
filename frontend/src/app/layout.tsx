import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { LiveKitProvider } from '../contexts/LiveKitContext'
import { Toaster } from "@/components/ui/toaster"

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Voice Assistant',
  description: 'Modern voice assistant with LiveKit streaming',
  keywords: ['voice assistant', 'AI', 'real-time audio', 'speech recognition'],
  authors: [{ name: 'Your Name' }],
  openGraph: {
    title: 'Voice Assistant',
    description: 'Modern voice assistant with LiveKit streaming',
    url: 'https://your-domain.com',
    siteName: 'Voice Assistant',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Voice Assistant Preview',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Voice Assistant',
    description: 'Modern voice assistant with LiveKit streaming',
    images: ['/og-image.png'],
    creator: '@yourusername',
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <LiveKitProvider>
          {children}
          <Toaster />
        </LiveKitProvider>
      </body>
    </html>
  )
}
