'use client'

import { Trophy } from 'lucide-react'

interface HeaderProps {
  sport: string
  setSport: (sport: string) => void
}

export default function Header({ sport, setSport }: HeaderProps) {
  return (
    <header className="bg-gradient-to-r from-sky-500 via-mint-400 to-coral-400 backdrop-blur-sm border-b-4 border-sunny-400 shadow-xl">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Trophy className="text-sunny-500" size={32} />
            <div>
              <h1 className="text-2xl font-display font-bold text-white tracking-tight drop-shadow-lg">wehuf sports analytics</h1>
              <p className="text-sm font-sans text-white/90">Professional Betting Predictions</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              value={sport}
              onChange={(e) => setSport(e.target.value)}
              className="bg-white text-sky-600 px-4 py-2 rounded-lg border-2 border-sunny-400 focus:outline-none focus:ring-2 focus:ring-sunny-400 focus:ring-offset-2 font-semibold shadow-md"
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

