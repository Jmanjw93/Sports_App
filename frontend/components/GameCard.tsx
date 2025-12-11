'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { Calendar, MapPin, TrendingUp, Cloud, Loader2, ChevronUp, Lock, Unlock, CheckCircle, XCircle } from 'lucide-react'
import { 
  saveLockedPrediction, 
  getLockedPrediction, 
  removeLockedPrediction, 
  isPredictionLocked,
  updatePredictionResult,
  type LockedPrediction 
} from '@/utils/predictionStorage'

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
  const [isLocked, setIsLocked] = useState(false)
  const [lockedPrediction, setLockedPrediction] = useState<LockedPrediction | null>(null)
  const [showResultInput, setShowResultInput] = useState(false)
  const [homeScore, setHomeScore] = useState('')
  const [awayScore, setAwayScore] = useState('')

  useEffect(() => {
    // Check if prediction is locked
    const locked = isPredictionLocked(game.game_id)
    setIsLocked(locked)
    
    if (locked) {
      const lockedData = getLockedPrediction(game.game_id)
      setLockedPrediction(lockedData)
      // If we have locked data, use it as prediction
      if (lockedData) {
        setPrediction({
          game_id: lockedData.game_id,
          home_team: lockedData.home_team,
          away_team: lockedData.away_team,
          predicted_winner: lockedData.predicted_winner,
          home_win_probability: lockedData.home_win_probability,
          away_win_probability: lockedData.away_win_probability,
          confidence: lockedData.confidence,
          weather_impact: lockedData.weather_impact,
          key_factors: lockedData.key_factors
        })
        setExpanded(true)
      }
    }
  }, [game.game_id])

  const fetchPrediction = async () => {
    if (prediction && !isLocked) {
      setExpanded(!expanded)
      return
    }

    // Don't fetch if locked - use locked data
    if (isLocked && lockedPrediction) {
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

  const handleLockPrediction = () => {
    if (!prediction) return

    const lockedPred: LockedPrediction = {
      game_id: game.game_id,
      sport: game.sport,
      home_team: game.home_team,
      away_team: game.away_team,
      game_date: game.date,
      predicted_winner: prediction.predicted_winner,
      home_win_probability: prediction.home_win_probability,
      away_win_probability: prediction.away_win_probability,
      confidence: prediction.confidence,
      weather_impact: prediction.weather_impact,
      key_factors: prediction.key_factors || [],
      locked_at: new Date().toISOString()
    }

    saveLockedPrediction(lockedPred)
    setIsLocked(true)
    setLockedPrediction(lockedPred)
  }

  const handleUnlockPrediction = () => {
    removeLockedPrediction(game.game_id)
    setIsLocked(false)
    setLockedPrediction(null)
  }

  const handleSubmitResult = () => {
    if (!homeScore || !awayScore) return

    const home = parseInt(homeScore)
    const away = parseInt(awayScore)
    const actualWinner = home > away ? game.home_team : home < away ? game.away_team : 'Tie'

    updatePredictionResult(game.game_id, actualWinner, home, away)
    
    // Refresh locked prediction
    const updated = getLockedPrediction(game.game_id)
    setLockedPrediction(updated)
    setShowResultInput(false)
    setHomeScore('')
    setAwayScore('')
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
    <div className={`bg-slate-800 rounded-lg p-6 border transition-all ${
      isLocked ? 'border-yellow-500/50 hover:border-yellow-500' : 'border-slate-700 hover:border-primary-500'
    }`}>
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            {isLocked && (
              <Lock size={16} className="text-yellow-500" />
            )}
            <h3 className="text-xl font-bold text-white">{game.away_team}</h3>
          </div>
          <p className="text-slate-400 text-sm">@</p>
          <h3 className="text-xl font-bold text-white">{game.home_team}</h3>
        </div>
        {prediction && (
          <div className={`text-right ${getConfidenceColor(prediction.confidence)}`}>
            <div className="text-2xl font-bold">
              {Math.round(prediction.confidence * 100)}%
            </div>
            <div className="text-xs text-slate-400">Confidence</div>
            {lockedPrediction?.analyzed && (
              <div className="mt-1">
                {lockedPrediction.is_correct ? (
                  <CheckCircle size={16} className="text-green-500 mx-auto" />
                ) : (
                  <XCircle size={16} className="text-red-500 mx-auto" />
                )}
              </div>
            )}
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

          {lockedPrediction?.analyzed && (
            <div className="mb-4 p-3 rounded border-2 border-slate-600">
              <p className="text-sm font-semibold text-slate-300 mb-2">Result Analysis:</p>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Actual Winner:</span>
                  <span className="text-white font-semibold">{lockedPrediction.actual_winner}</span>
                </div>
                {lockedPrediction.actual_home_score !== undefined && lockedPrediction.actual_away_score !== undefined && (
                  <div className="flex justify-between">
                    <span className="text-slate-400">Final Score:</span>
                    <span className="text-white">
                      {game.away_team}: {lockedPrediction.actual_away_score} - {game.home_team}: {lockedPrediction.actual_home_score}
                    </span>
                  </div>
                )}
                <div className="flex justify-between items-center mt-2 pt-2 border-t border-slate-600">
                  <span className="text-slate-400">Prediction:</span>
                  <span className={`font-bold ${lockedPrediction.is_correct ? 'text-green-400' : 'text-red-400'}`}>
                    {lockedPrediction.is_correct ? '✓ Correct' : '✗ Incorrect'}
                  </span>
                </div>
                {!lockedPrediction.is_correct && (
                  <div className="mt-2 p-2 bg-red-900/20 rounded text-slate-300">
                    <p className="text-xs">
                      Predicted: <span className="font-semibold">{lockedPrediction.predicted_winner}</span> 
                      {' '}but actual winner was <span className="font-semibold">{lockedPrediction.actual_winner}</span>
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {isLocked && !lockedPrediction?.analyzed && (
            <div className="mb-4">
              {!showResultInput ? (
                <button
                  onClick={() => setShowResultInput(true)}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 px-4 rounded transition-colors"
                >
                  Enter Game Result
                </button>
              ) : (
                <div className="p-3 bg-slate-700/50 rounded">
                  <p className="text-sm font-semibold text-slate-300 mb-3">Enter Final Score:</p>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <label className="text-xs text-slate-400 w-24">{game.away_team}:</label>
                      <input
                        type="number"
                        value={awayScore}
                        onChange={(e) => setAwayScore(e.target.value)}
                        className="flex-1 bg-slate-800 border border-slate-600 rounded px-2 py-1 text-white text-sm"
                        placeholder="Score"
                      />
                    </div>
                    <div className="flex items-center gap-2">
                      <label className="text-xs text-slate-400 w-24">{game.home_team}:</label>
                      <input
                        type="number"
                        value={homeScore}
                        onChange={(e) => setHomeScore(e.target.value)}
                        className="flex-1 bg-slate-800 border border-slate-600 rounded px-2 py-1 text-white text-sm"
                        placeholder="Score"
                      />
                    </div>
                    <div className="flex gap-2 mt-3">
                      <button
                        onClick={handleSubmitResult}
                        disabled={!homeScore || !awayScore}
                        className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white text-sm font-semibold py-2 px-4 rounded transition-colors"
                      >
                        Submit Result
                      </button>
                      <button
                        onClick={() => {
                          setShowResultInput(false)
                          setHomeScore('')
                          setAwayScore('')
                        }}
                        className="px-4 bg-slate-600 hover:bg-slate-700 text-white text-sm font-semibold py-2 rounded transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              )}
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
        {prediction && expanded && (
          <button
            onClick={isLocked ? handleUnlockPrediction : handleLockPrediction}
            className={`px-4 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center justify-center gap-2 ${
              isLocked
                ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                : 'bg-slate-700 hover:bg-slate-600 text-slate-300'
            }`}
            title={isLocked ? 'Unlock prediction' : 'Lock prediction to track accuracy'}
          >
            {isLocked ? (
              <>
                <Unlock size={16} />
                <span className="hidden sm:inline">Unlock</span>
              </>
            ) : (
              <>
                <Lock size={16} />
                <span className="hidden sm:inline">Lock</span>
              </>
            )}
          </button>
        )}
      </div>
    </div>
  )
}

