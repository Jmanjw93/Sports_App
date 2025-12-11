'use client'

import { useState, useEffect } from 'react'
import GameList from '@/components/GameList'
import BestBets from '@/components/BestBets'
import LockedPredictions from '@/components/LockedPredictions'
import Header from '@/components/Header'
import { TrendingUp, Target, BarChart3, Lock } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'games' | 'bets' | 'player-bets' | 'locked'>('games')
  const [sport, setSport] = useState('nfl')

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <Header sport={sport} setSport={setSport} />
      
      <div className="container mx-auto px-4 py-8">
        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-8">
          <button
            onClick={() => setActiveTab('games')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'games'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <BarChart3 size={20} />
            <span>Games & Predictions</span>
          </button>
          <button
            onClick={() => setActiveTab('bets')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'bets'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <TrendingUp size={20} />
            <span>Best Team Bets</span>
          </button>
          <button
            onClick={() => setActiveTab('player-bets')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'player-bets'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <Target size={20} />
            <span>Player Props</span>
          </button>
          <button
            onClick={() => setActiveTab('locked')}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === 'locked'
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <Lock size={20} />
            <span>Locked Predictions</span>
          </button>
        </div>

        {/* Content */}
        <div className="mt-8">
          {activeTab === 'games' && <GameList sport={sport} />}
          {activeTab === 'bets' && <BestBets sport={sport} />}
          {activeTab === 'player-bets' && (
            <div className="text-white">
              <h2 className="text-2xl font-bold mb-4">Player Prop Bets</h2>
              <p className="text-slate-400">Select a game to view player prop recommendations</p>
            </div>
          )}
          {activeTab === 'locked' && <LockedPredictions />}
        </div>
      </div>
    </main>
  )
}

