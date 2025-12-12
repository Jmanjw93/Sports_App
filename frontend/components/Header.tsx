'use client'

import { Trophy } from 'lucide-react'

interface HeaderProps {
  sport: string
  setSport: (sport: string) => void
}

export default function Header({ sport, setSport }: HeaderProps) {
  return (
    <header className="bg-slate-800 border-b border-slate-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Trophy className="text-primary-400" size={32} />
            <div>
              <h1 className="text-2xl font-heading font-bold text-white">Bold Statement(s)</h1>
              <p className="text-sm text-slate-400">Professional Betting Predictions</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              value={sport}
              onChange={(e) => setSport(e.target.value)}
              className="bg-slate-700 text-white px-4 py-2 rounded-lg border border-slate-600 focus:outline-none focus:ring-2 focus:ring-primary-500"
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

