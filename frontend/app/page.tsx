'use client'

import { useState } from 'react'
import GameList from '@/components/GameList'
import BestBets from '@/components/BestBets'
import PlayerPropsList from '@/components/PlayerPropsList'
import Header from '@/components/Header'
import BackgroundDesign from '@/components/BackgroundDesign'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { TrendingUp, Target, BarChart3 } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'games' | 'bets' | 'player-bets'>('games')
  const [sport, setSport] = useState('nfl')

  return (
    <ErrorBoundary>
      <main className="min-h-screen bg-gradient-to-br from-sky-400 via-mint-300 to-coral-300 relative pulse-background">
        <BackgroundDesign />
        <div className="relative z-10">
          <Header sport={sport} setSport={setSport} />
        
        <div className="container mx-auto px-4 py-8">
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-3 mb-8">
            <button
              onClick={() => setActiveTab('games')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'games'
                  ? 'bg-sky-500 text-white shadow-lg scale-105 shadow-sky-600/50'
                  : 'bg-white/80 text-sky-600 hover:bg-sky-100 hover:scale-105 border-2 border-sky-300'
              }`}
            >
              <BarChart3 size={20} />
              <span>Games & Predictions</span>
            </button>
            <button
              onClick={() => setActiveTab('bets')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'bets'
                  ? 'bg-mint-500 text-white shadow-lg scale-105 shadow-mint-600/50'
                  : 'bg-white/80 text-mint-600 hover:bg-mint-100 hover:scale-105 border-2 border-mint-300'
              }`}
            >
              <TrendingUp size={20} />
              <span>Best Team Bets</span>
            </button>
            <button
              onClick={() => setActiveTab('player-bets')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'player-bets'
                  ? 'bg-coral-500 text-white shadow-lg scale-105 shadow-coral-600/50'
                  : 'bg-white/80 text-coral-600 hover:bg-coral-100 hover:scale-105 border-2 border-coral-300'
              }`}
            >
              <Target size={20} />
              <span>Player Props</span>
            </button>
          </div>

          {/* Content */}
          <div className="mt-8">
            {activeTab === 'games' && <GameList sport={sport} />}
            {activeTab === 'bets' && <BestBets sport={sport} />}
            {activeTab === 'player-bets' && <PlayerPropsList sport={sport} />}
          </div>
        </div>
        </div>
      </main>
    </ErrorBoundary>
  )
}

