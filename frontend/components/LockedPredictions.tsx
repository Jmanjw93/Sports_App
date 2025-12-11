'use client'

import { useState, useEffect } from 'react'
import { Lock, CheckCircle, XCircle, TrendingUp, BarChart3, Calendar } from 'lucide-react'
import { 
  getLockedPredictions, 
  getPredictionAccuracy,
  type LockedPrediction 
} from '@/utils/predictionStorage'

export default function LockedPredictions() {
  const [predictions, setPredictions] = useState<LockedPrediction[]>([])
  const [filter, setFilter] = useState<'all' | 'analyzed' | 'pending'>('all')
  const [sportFilter, setSportFilter] = useState<string>('all')
  const accuracy = getPredictionAccuracy()

  useEffect(() => {
    loadPredictions()
    // Refresh every 30 seconds
    const interval = setInterval(loadPredictions, 30000)
    return () => clearInterval(interval)
  }, [])

  const loadPredictions = () => {
    const all = getLockedPredictions()
    setPredictions(all)
  }

  const filteredPredictions = predictions.filter(p => {
    if (filter === 'analyzed' && !p.analyzed) return false
    if (filter === 'pending' && p.analyzed) return false
    if (sportFilter !== 'all' && p.sport !== sportFilter) return false
    return true
  })

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
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
    <div className="space-y-6">
      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Total Locked</p>
              <p className="text-2xl font-bold text-white">{predictions.length}</p>
            </div>
            <Lock className="text-yellow-500" size={24} />
          </div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Analyzed</p>
              <p className="text-2xl font-bold text-white">{accuracy.total}</p>
            </div>
            <BarChart3 className="text-blue-500" size={24} />
          </div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Correct</p>
              <p className="text-2xl font-bold text-green-400">{accuracy.correct}</p>
            </div>
            <CheckCircle className="text-green-500" size={24} />
          </div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Accuracy</p>
              <p className="text-2xl font-bold text-primary-400">
                {accuracy.accuracy.toFixed(1)}%
              </p>
            </div>
            <TrendingUp className="text-primary-500" size={24} />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              filter === 'all'
                ? 'bg-primary-600 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('analyzed')}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              filter === 'analyzed'
                ? 'bg-primary-600 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Analyzed
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              filter === 'pending'
                ? 'bg-primary-600 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Pending
          </button>
        </div>
        <select
          value={sportFilter}
          onChange={(e) => setSportFilter(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white"
        >
          <option value="all">All Sports</option>
          <option value="nfl">NFL</option>
          <option value="nba">NBA</option>
          <option value="mlb">MLB</option>
          <option value="nhl">NHL</option>
        </select>
      </div>

      {/* Predictions List */}
      {filteredPredictions.length === 0 ? (
        <div className="bg-slate-800 rounded-lg p-8 border border-slate-700 text-center">
          <Lock className="mx-auto text-slate-600 mb-4" size={48} />
          <p className="text-slate-400">No locked predictions found</p>
          <p className="text-slate-500 text-sm mt-2">
            Lock predictions on game cards to track their accuracy
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredPredictions.map((pred) => (
            <div
              key={pred.game_id}
              className={`bg-slate-800 rounded-lg p-6 border transition-all ${
                pred.analyzed
                  ? pred.is_correct
                    ? 'border-green-500/50'
                    : 'border-red-500/50'
                  : 'border-slate-700'
              }`}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs uppercase bg-slate-700 px-2 py-1 rounded text-slate-300">
                      {pred.sport}
                    </span>
                    {pred.analyzed && (
                      <span
                        className={`text-xs px-2 py-1 rounded font-semibold ${
                          pred.is_correct
                            ? 'bg-green-900/50 text-green-400'
                            : 'bg-red-900/50 text-red-400'
                        }`}
                      >
                        {pred.is_correct ? 'Correct' : 'Incorrect'}
                      </span>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-1">{pred.away_team}</h3>
                  <p className="text-slate-400 text-sm">@</p>
                  <h3 className="text-xl font-bold text-white">{pred.home_team}</h3>
                  <div className="flex items-center gap-4 mt-2 text-xs text-slate-400">
                    <div className="flex items-center gap-1">
                      <Calendar size={12} />
                      {formatDate(pred.game_date)}
                    </div>
                    <div className="flex items-center gap-1">
                      <Lock size={12} />
                      Locked: {formatDate(pred.locked_at)}
                    </div>
                  </div>
                </div>
                <div className={`text-right ${getConfidenceColor(pred.confidence)}`}>
                  <div className="text-2xl font-bold">
                    {Math.round(pred.confidence * 100)}%
                  </div>
                  <div className="text-xs text-slate-400">Confidence</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-slate-700/50 rounded p-3">
                  <p className="text-xs text-slate-400 mb-1">Predicted Winner</p>
                  <p className="text-primary-400 font-bold">{pred.predicted_winner}</p>
                  <div className="mt-2 text-xs text-slate-400">
                    <div>Home: {Math.round(pred.home_win_probability * 100)}%</div>
                    <div>Away: {Math.round(pred.away_win_probability * 100)}%</div>
                  </div>
                </div>
                {pred.analyzed && (
                  <div className="bg-slate-700/50 rounded p-3">
                    <p className="text-xs text-slate-400 mb-1">Actual Winner</p>
                    <p className="text-white font-bold">{pred.actual_winner}</p>
                    {pred.actual_home_score !== undefined && pred.actual_away_score !== undefined && (
                      <div className="mt-2 text-xs text-slate-400">
                        <div>
                          {pred.away_team}: {pred.actual_away_score}
                        </div>
                        <div>
                          {pred.home_team}: {pred.actual_home_score}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {pred.key_factors && pred.key_factors.length > 0 && (
                <div className="mb-4">
                  <p className="text-sm font-semibold text-slate-300 mb-2">Key Factors:</p>
                  <ul className="list-disc list-inside text-xs text-slate-400 space-y-1">
                    {pred.key_factors.map((factor, idx) => (
                      <li key={idx}>{factor}</li>
                    ))}
                  </ul>
                </div>
              )}

              {pred.analyzed && !pred.is_correct && (
                <div className="mt-4 p-3 bg-red-900/20 rounded border border-red-500/30">
                  <p className="text-sm font-semibold text-red-400 mb-1">Analysis:</p>
                  <p className="text-xs text-slate-300">
                    The model predicted <span className="font-semibold">{pred.predicted_winner}</span> with{' '}
                    {Math.round(pred.confidence * 100)}% confidence, but{' '}
                    <span className="font-semibold">{pred.actual_winner}</span> won.
                    {pred.confidence > 0.7 && (
                      <span className="block mt-1 text-red-400">
                        High confidence prediction was incorrect - review key factors.
                      </span>
                    )}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

