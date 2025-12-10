'use client'

import { useState } from 'react'
import GameList from '@/components/GameList'
import BestBets from '@/components/BestBets'
import PlayerPropsList from '@/components/PlayerPropsList'
import BettingCalculator from '@/components/BettingCalculator'
import PlayerComparison from '@/components/PlayerComparison'
import AnalyticsDashboard from '@/components/AnalyticsDashboard'
import ParlayBuilder from '@/components/ParlayBuilder'
import LearningDashboard from '@/components/LearningDashboard'
import LockedPredictions from '@/components/LockedPredictions'
import Header from '@/components/Header'
import BackgroundDesign from '@/components/BackgroundDesign'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { TrendingUp, Target, BarChart3, Calculator, Users, Activity, Star, Lightbulb, Lock } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'games' | 'bets' | 'player-bets' | 'calculator' | 'comparison' | 'analytics' | 'parlay' | 'learning' | 'locked'>('games')
  const [sport, setSport] = useState('nfl')

  return (
    <ErrorBoundary>
      <main className="min-h-screen bg-gradient-to-br from-warm-50 via-amber-25 to-cozy-50 relative pulse-background">
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
                  ? 'bg-warm-500 text-white shadow-lg scale-105 shadow-warm-700/50'
                  : 'bg-white/90 text-gray-900 hover:bg-warm-50 hover:scale-105 border-2 border-warm-300'
              }`}
            >
              <BarChart3 size={20} />
              <span>Games & Predictions</span>
            </button>
            <button
              onClick={() => setActiveTab('bets')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'bets'
                  ? 'bg-amber-500 text-white shadow-lg scale-105 shadow-amber-700/50'
                  : 'bg-white/90 text-gray-900 hover:bg-amber-50 hover:scale-105 border-2 border-amber-300'
              }`}
            >
              <TrendingUp size={20} />
              <span>Best Team Bets</span>
            </button>
            <button
              onClick={() => setActiveTab('player-bets')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'player-bets'
                  ? 'bg-cozy-500 text-white shadow-lg scale-105 shadow-cozy-700/50'
                  : 'bg-white/90 text-gray-900 hover:bg-cozy-50 hover:scale-105 border-2 border-cozy-300'
              }`}
            >
              <Target size={20} />
              <span>Player Props</span>
            </button>
            <button
              onClick={() => setActiveTab('calculator')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'calculator'
                  ? 'bg-amber-600 text-white shadow-lg scale-105 shadow-amber-800/50'
                  : 'bg-white/90 text-gray-900 hover:bg-amber-50 hover:scale-105 border-2 border-amber-400'
              }`}
            >
              <Calculator size={20} />
              <span>Bet Calculator</span>
            </button>
            <button
              onClick={() => setActiveTab('comparison')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'comparison'
                  ? 'bg-terracotta-500 text-white shadow-lg scale-105 shadow-terracotta-700/50'
                  : 'bg-white/90 text-gray-900 hover:bg-terracotta-50 hover:scale-105 border-2 border-terracotta-300'
              }`}
            >
              <Users size={20} />
              <span>Compare Players</span>
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'analytics'
                  ? 'bg-sage-600 text-white shadow-lg scale-105 shadow-sage-800/50'
                  : 'bg-white/90 text-gray-900 hover:bg-sage-50 hover:scale-105 border-2 border-sage-400'
              }`}
            >
              <Activity size={20} />
              <span>Analytics</span>
            </button>
            <button
              onClick={() => setActiveTab('locked')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-heading font-semibold transition-all duration-200 transform tracking-tight ${
                activeTab === 'locked'
                  ? 'bg-purple-600 text-white shadow-lg scale-105 shadow-purple-800/50'
                  : 'bg-white/90 text-gray-900 hover:bg-purple-50 hover:scale-105 border-2 border-purple-400'
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
            {activeTab === 'player-bets' && <PlayerPropsList sport={sport} />}
            {activeTab === 'calculator' && <BettingCalculator sport={sport} />}
            {activeTab === 'comparison' && <PlayerComparison sport={sport} />}
            {activeTab === 'analytics' && <AnalyticsDashboard sport={sport} />}
            {activeTab === 'parlay' && <ParlayBuilder sport={sport} />}
            {activeTab === 'learning' && <LearningDashboard sport={sport} />}
            {activeTab === 'locked' && (
              <div>
                <LockedPredictions sport={sport} />
              </div>
            )}
          </div>
        </div>
        </div>
      </main>
    </ErrorBoundary>
  )
}

