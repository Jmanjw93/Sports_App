'use client'

import { Trophy } from 'lucide-react'

interface HeaderProps {
  sport: string
  setSport: (sport: string) => void
}

export default function Header({ sport, setSport }: HeaderProps) {
  return (
    <header className="bg-gradient-to-r from-warm-600 via-amber-500 to-cozy-600 backdrop-blur-sm border-b-4 border-amber-400 shadow-xl">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Trophy className="text-amber-200" size={32} />
            <div>
              <h1 className="text-2xl font-display font-bold text-white tracking-tight drop-shadow-lg">Mental MQW</h1>
              {/* Updated branding to Mental MQW */}
              <p className="text-sm font-sans text-white/95">Professional Betting Predictions</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              value={sport}
              onChange={(e) => setSport(e.target.value)}
              className="bg-white text-warm-700 px-4 py-2 rounded-lg border-2 border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-400 focus:ring-offset-2 font-semibold shadow-md"
            >
              <option value="nfl">NFL</option>
              <option value="nba">NBA</option>
              <option value="mlb">MLB</option>
              <option value="nhl">NHL</option>
            </select>
          </div>
        </div>
      </div>
    </header>
  )
}

