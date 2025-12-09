'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { TrendingUp, DollarSign, Target, AlertCircle } from 'lucide-react'
import { Loader2 } from 'lucide-react'

interface Bet {
  game_id: string
  bet_type: string
  selection: string
  platform: string
  odds: number
  expected_value: number
  kelly_percentage: number
  recommendation: string
  true_probability: number
  implied_probability: number
}

interface BestBetsProps {
  sport: string
}

export default function BestBets({ sport }: BestBetsProps) {
  const [bets, setBets] = useState<Bet[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchBestBets()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sport])

  const fetchBestBets = async () => {
    try {
      setLoading(true)
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/bets/best-bets`,
        { params: { sport, limit: 20 } }
      )
      setBets(response.data.best_bets || [])
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch best bets')
      console.error('Error fetching best bets:', err)
    } finally {
      setLoading(false)
    }
  }

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'strong_bet':
        return 'bg-mint-200 border-4 border-mint-500 text-mint-700'
      case 'moderate_bet':
        return 'bg-sky-200 border-4 border-sky-500 text-sky-700'
      case 'small_bet':
        return 'bg-coral-200 border-4 border-coral-500 text-coral-700'
      default:
        return 'bg-rose-200 border-4 border-rose-500 text-rose-700'
    }
  }

  const getRecommendationLabel = (recommendation: string) => {
    switch (recommendation) {
      case 'strong_bet':
        return 'Strong Bet'
      case 'moderate_bet':
        return 'Moderate Bet'
      case 'small_bet':
        return 'Small Bet'
      default:
        return 'Avoid'
    }
  }

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'bet365':
        return 'bg-sunny-200 text-sunny-700'
      case 'draftkings':
        return 'bg-sky-200 text-sky-700'
      case 'thescore_bet':
        return 'bg-mint-200 text-mint-700'
      default:
        return 'bg-coral-200 text-coral-700'
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="animate-spin text-sky-500" size={48} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-rose-200 border-4 border-rose-500 rounded-lg p-4 text-rose-800 font-semibold">
        <div className="flex items-center">
          <AlertCircle size={20} className="mr-2" />
          <p>Error: {error}</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-3xl font-heading font-bold text-white tracking-tight drop-shadow-lg">Best Betting Opportunities</h2>
        <button
          onClick={fetchBestBets}
          className="bg-gradient-to-r from-sky-500 to-mint-500 hover:from-sky-600 hover:to-mint-600 text-white px-4 py-2 rounded-lg transition-colors shadow-xl font-bold"
        >
          Refresh
        </button>
      </div>

      {bets.length === 0 ? (
        <div className="text-center py-12 text-white font-semibold drop-shadow-md">
          <Target size={48} className="mx-auto mb-4 opacity-80" />
          <p>No positive EV bets found at this time</p>
          <p className="text-sm mt-2">Check back later for new opportunities</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {bets.map((bet, idx) => (
            <div
              key={idx}
              className="bg-white rounded-lg p-6 border-4 border-sky-300 hover:border-sky-500 transition-all shadow-xl"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-heading font-bold text-sky-600 mb-1 tracking-tight">{bet.selection}</h3>
                  <p className="text-mint-600 text-sm font-semibold">{bet.bet_type.replace('_', ' ')}</p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${getPlatformColor(bet.platform)}`}
                >
                  {bet.platform.replace('_', ' ').toUpperCase()}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-mint-100 rounded-lg p-3 border-2 border-mint-400">
                  <div className="flex items-center text-mint-700 text-xs mb-1 font-semibold">
                    <DollarSign size={14} className="mr-1" />
                    Expected Value
                  </div>
                  <div className="text-2xl font-bold text-mint-600">
                    +{(bet.expected_value * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="bg-sky-100 rounded-lg p-3 border-2 border-sky-400">
                  <div className="flex items-center text-sky-700 text-xs mb-1 font-semibold">
                    <TrendingUp size={14} className="mr-1" />
                    Odds
                  </div>
                  <div className="text-2xl font-bold text-sky-600">{bet.odds.toFixed(2)}</div>
                </div>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-sky-600 font-semibold">True Probability:</span>
                  <span className="text-mint-600 font-bold">
                    {(bet.true_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-sky-600 font-semibold">Implied Probability:</span>
                  <span className="text-coral-600 font-bold">
                    {(bet.implied_probability * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-sky-600 font-semibold">Kelly Percentage:</span>
                  <span className="text-rose-600 font-bold">
                    {(bet.kelly_percentage * 100).toFixed(2)}%
                  </span>
                </div>
              </div>

              <div
                className={`border rounded-lg p-3 text-center font-semibold ${getRecommendationColor(bet.recommendation)}`}
              >
                {getRecommendationLabel(bet.recommendation)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

