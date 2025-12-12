import type { Metadata } from 'next'
import { Inter, Merriweather, Comfortaa } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const merriweather = Merriweather({ 
  subsets: ['latin'],
  weight: ['300', '400', '700', '900'],
  variable: '--font-merriweather',
  display: 'swap',
})

const comfortaa = Comfortaa({ 
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-comfortaa',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Bold Statement(s) - Sports Analytics & Betting Predictions',
  description: 'Professional sports betting analytics with weather integration',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${merriweather.variable} ${comfortaa.variable} font-sans`}>
        {children}
      </body>
    </html>
  )
}

