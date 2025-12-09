import type { Metadata } from 'next'
import { Inter, Nunito, Comic_Neue } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const nunito = Nunito({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-nunito',
  display: 'swap',
})

const comicNeue = Comic_Neue({
  subsets: ['latin'],
  weight: ['300', '400', '700'],
  variable: '--font-comic',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'wehuf sports analytics & Betting Predictions',
  description: 'Professional sports betting analytics with weather integration',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${nunito.variable} ${comicNeue.variable} font-sans antialiased`}>{children}</body>
    </html>
  )
}

