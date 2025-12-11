'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { Calendar, MapPin, TrendingUp, Cloud, Loader2, ChevronUp, Lock } from 'lucide-react'

interface Game {
  game_id: string
  sport: string
  home_team: string
  away_team: string
  date: string
  venue: string
  location: {
    city: string
    state: string
    country: string
  }
}

interface Prediction {
  game_id: string
  home_team: string
  away_team: string
  predicted_winner: string
  home_win_probability: number
  away_win_probability: number
  confidence: number
  weather_impact: any
  key_factors: string[]
}

export default function GameCard({ game }: { game: Game }) {
  const [prediction, setPrediction] = useState<Prediction | null>(null)
  const [loading, setLoading] = useState(false)
  const [expanded, setExpanded] = useState(false)

  const fetchPrediction = async () => {
    if (prediction) {
      setExpanded(!expanded)
      return
    }

    try {
      setLoading(true)
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/predictions/game/${game.game_id}`
      )
      setPrediction(response.data)
      setExpanded(true)
    } catch (err) {
      console.error('Error fetching prediction:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    })
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.7) return 'text-green-400'
    if (confidence > 0.5) return 'text-yellow-400'
    return 'text-orange-400'
  }

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 hover:border-primary-500 transition-all">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-white mb-1">{game.away_team}</h3>
          <p className="text-slate-400 text-sm">@</p>
          <h3 className="text-xl font-bold text-white">{game.home_team}</h3>
        </div>
        {prediction && (
          <div className={`text-right ${getConfidenceColor(prediction.confidence)}`}>
            <div className="text-2xl font-bold">
              {Math.round(prediction.confidence * 100)}%
            </div>
            <div className="text-xs text-slate-400">Confidence</div>
          </div>
        )}
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center text-slate-400 text-sm">
          <Calendar size={16} className="mr-2" />
          {formatDate(game.date)}
        </div>
        <div className="flex items-center text-slate-400 text-sm">
          <MapPin size={16} className="mr-2" />
          {game.location.city}, {game.location.state}
        </div>
      </div>

      {expanded && prediction && (
        <div className="mt-4 pt-4 border-t border-slate-700">
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm">Predicted Winner:</span>
              <span className="text-primary-400 font-bold">{prediction.predicted_winner}</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-400 text-sm">Home Win Probability:</span>
              <span className="text-white font-semibold">
                {Math.round(prediction.home_win_probability * 100)}%
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400 text-sm">Away Win Probability:</span>
              <span className="text-white font-semibold">
                {Math.round(prediction.away_win_probability * 100)}%
              </span>
            </div>
          </div>

          {prediction.weather_impact && (
            <div className="mb-4 p-3 bg-slate-700/50 rounded">
              <div className="flex items-center mb-2">
                <Cloud size={16} className="mr-2 text-blue-400" />
                <span className="text-sm font-semibold text-blue-400">Weather Impact</span>
              </div>
              {prediction.weather_impact.weather_impact && (
                <div className="text-xs text-slate-300">
                  {prediction.weather_impact.weather_impact.conditions || 'Clear conditions'}
                </div>
              )}
            </div>
          )}

          {prediction.key_factors && prediction.key_factors.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-semibold text-slate-300 mb-2">Key Factors:</p>
              <ul className="list-disc list-inside text-xs text-slate-400 space-y-1">
                {prediction.key_factors.map((factor, idx) => (
                  <li key={idx}>{factor}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="flex gap-2 mt-4">
        <button
          onClick={fetchPrediction}
          disabled={loading}
          className="flex-1 bg-gradient-to-r from-warm-500 to-amber-500 hover:from-sky-600 hover:to-mint-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-[1.02] active:scale-[0.98] shadow-xl shadow-sky-400/50"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={16} />
              Loading prediction...
            </>
          ) : expanded ? (
            <>
              <ChevronUp size={16} />
              Hide Prediction
            </>
          ) : (
            <>
              <TrendingUp size={16} />
              View Prediction
            </>
          )}
        </button>
      </div>
    </div>
  )
}

