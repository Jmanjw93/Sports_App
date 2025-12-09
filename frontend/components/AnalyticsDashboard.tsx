'use client'

import { useState, useEffect } from 'react'
import { Activity, TrendingUp, BarChart3, Target } from 'lucide-react'
import GameSimulator from './GameSimulator'
import axios from 'axios'

interface AnalyticsDashboardProps {
  sport?: string
}

export default function AnalyticsDashboard({ sport = 'nfl' }: AnalyticsDashboardProps) {
  const [games, setGames] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedGame, setSelectedGame] = useState<string | null>(null)

  useEffect(() => {
    fetchGames()
  }, [sport])

  const fetchGames = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
      const response = await axios.get(`${apiUrl}/api/games/upcoming?sport=${sport}`)
      setGames(response.data.slice(0, 5)) // Get first 5 games
      if (response.data.length > 0) {
        setSelectedGame(response.data[0].game_id)
      }
    } catch (error) {
      console.error('Error fetching games:', error)
    } finally {
      setLoading(false)
    }
  }

  const selectedGameData = games.find(g => g.game_id === selectedGame)

  return (
    <div className="space-y-6">
      <div className="flex items-center mb-6">
        <Activity className="text-sage-600 mr-3" size={28} />
        <h2 className="text-3xl font-heading font-bold text-gray-900 tracking-tight drop-shadow-lg">Advanced Analytics</h2>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-latte-50 rounded-lg p-4 border-4 border-warm-300 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs text-gray-900 font-semibold">Total Games</div>
              <div className="text-2xl font-bold text-gray-900">{games.length}</div>
            </div>
            <BarChart3 className="text-warm-600" size={24} />
          </div>
        </div>
        <div className="bg-latte-50 rounded-lg p-4 border-4 border-amber-300 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs text-gray-900 font-semibold">Avg Confidence</div>
              <div className="text-2xl font-bold text-gray-900">72%</div>
            </div>
            <TrendingUp className="text-amber-600" size={24} />
          </div>
        </div>
        <div className="bg-latte-50 rounded-lg p-4 border-4 border-cozy-300 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs text-gray-900 font-semibold">Best Value</div>
              <div className="text-2xl font-bold text-gray-900">+15.3%</div>
            </div>
            <Target className="text-cozy-600" size={24} />
          </div>
        </div>
        <div className="bg-latte-50 rounded-lg p-4 border-4 border-terracotta-300 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs text-rose-600 font-semibold">Simulations</div>
              <div className="text-2xl font-bold text-rose-700">10K+</div>
            </div>
            <Activity className="text-rose-400" size={24} />
          </div>
        </div>
      </div>

      {/* Game Selection for Simulation */}
      {games.length > 0 && (
        <div className="bg-latte-50 rounded-lg p-4 border-4 border-happy-300 shadow-lg mb-6">
          <h3 className="text-lg font-bold text-happy-600 mb-3">Select Game for Simulation</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {games.map((game) => (
              <button
                key={game.game_id}
                onClick={() => setSelectedGame(game.game_id)}
                className={`p-3 rounded-lg border-2 transition-all ${
                  selectedGame === game.game_id
                    ? 'bg-happy-100 border-happy-500 shadow-md'
                    : 'bg-latte-50 border-happy-300 hover:border-happy-400'
                }`}
              >
                <div className="text-sm font-semibold text-happy-700">{game.away_team}</div>
                <div className="text-xs text-happy-500">@</div>
                <div className="text-sm font-semibold text-happy-700">{game.home_team}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Game Simulator */}
      {selectedGameData && (
        <GameSimulator
          gameId={selectedGame}
          homeTeam={selectedGameData.home_team}
          awayTeam={selectedGameData.away_team}
        />
      )}

      {/* Performance Trends */}
      <div className="bg-latte-50 rounded-lg p-6 border-4 border-warm-300 shadow-xl">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="mr-2" size={20} />
          Prediction Accuracy Trends
        </h3>
        <div className="space-y-4">
          <div className="bg-gradient-to-r from-warm-50 to-amber-50 p-4 rounded-lg border-2 border-warm-300">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-semibold text-gray-900">Last 30 Days</span>
              <span className="text-lg font-bold text-gray-900">68.5%</span>
            </div>
            <div className="w-full bg-warm-200 rounded-full h-3">
              <div className="bg-amber-500 h-3 rounded-full" style={{ width: '68.5%' }}></div>
            </div>
          </div>
          <div className="bg-gradient-to-r from-cozy-50 to-terracotta-50 p-4 rounded-lg border-2 border-cozy-300">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-semibold text-gray-900">Last 7 Days</span>
              <span className="text-lg font-bold text-gray-900">72.3%</span>
            </div>
            <div className="w-full bg-cozy-200 rounded-full h-3">
              <div className="bg-terracotta-500 h-3 rounded-full" style={{ width: '72.3%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

