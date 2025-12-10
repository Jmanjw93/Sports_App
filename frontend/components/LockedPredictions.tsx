'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { Lock, CheckCircle, XCircle, Clock, TrendingUp, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react'

interface LockedPrediction {
  prediction_id: string
  game_id: string
  sport: string
  home_team: string
  away_team: string
  predicted_winner: string
  actual_winner?: string
  home_win_probability: number
  away_win_probability: number
  confidence: number
  outcome: 'pending' | 'correct' | 'incorrect'
  prediction_date: string
  locked_date: string
  game_date?: string
  factors: any
  full_prediction_data: any
  error_analysis?: any
}

interface PredictionAnalysis {
  prediction_id: string
  was_correct: boolean
  predicted_winner: string
  actual_winner?: string
  predicted_probabilities: {
    home: number
    away: number
  }
  confidence: number
  factors_analysis: any
  success_factors?: string[]
  error_factors?: string[]
}

export default function LockedPredictions({ sport }: { sport: string }) {
  const [predictions, setPredictions] = useState<LockedPrediction[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<Record<string, PredictionAnalysis>>({})
  const [analyzingId, setAnalyzingId] = useState<string | null>(null)

  useEffect(() => {
    fetchLockedPredictions()
  }, [sport])

  const fetchLockedPredictions = async () => {
    try {
      setLoading(true)
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/learning/locked-predictions?include_resolved=true&sport=${sport}`
      )
      setPredictions(response.data.predictions || [])
    } catch (err) {
      console.error('Error fetching locked predictions:', err)
    } finally {
      setLoading(false)
    }
  }

  const analyzePrediction = async (predictionId: string) => {
    if (analysis[predictionId]) {
      setExpandedId(expandedId === predictionId ? null : predictionId)
      return
    }

    try {
      setAnalyzingId(predictionId)
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/learning/analyze-prediction/${predictionId}`
      )
      setAnalysis(prev => ({ ...prev, [predictionId]: response.data }))
      setExpandedId(predictionId)
    } catch (err) {
      console.error('Error analyzing prediction:', err)
      alert('Failed to analyze prediction')
    } finally {
      setAnalyzingId(null)
    }
  }

  const getOutcomeIcon = (outcome: string) => {
    switch (outcome) {
      case 'correct':
        return <CheckCircle className="text-green-600" size={20} />
      case 'incorrect':
        return <XCircle className="text-red-600" size={20} />
      default:
        return <Clock className="text-amber-600" size={20} />
    }
  }

  const getOutcomeColor = (outcome: string) => {
    switch (outcome) {
      case 'correct':
        return 'bg-green-100 border-green-400'
      case 'incorrect':
        return 'bg-red-100 border-red-400'
      default:
        return 'bg-amber-100 border-amber-400'
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-warm-600"></div>
        <p className="mt-4 text-gray-700">Loading locked predictions...</p>
      </div>
    )
  }

  if (predictions.length === 0) {
    return (
      <div className="text-center py-12 bg-white/80 rounded-lg border-2 border-warm-300">
        <Lock className="mx-auto text-warm-400" size={48} />
        <h3 className="mt-4 text-xl font-bold text-gray-900">No Locked Predictions</h3>
        <p className="mt-2 text-gray-700">
          Lock predictions from game cards to analyze them later
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="bg-white/90 rounded-lg p-4 border-2 border-warm-300 mb-4">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Locked Predictions Analysis</h2>
        <p className="text-gray-700">
          Review and analyze your locked predictions to understand what went right or wrong
        </p>
      </div>

      {predictions.map((pred) => (
        <div
          key={pred.prediction_id}
          className={`bg-white/90 rounded-lg p-6 border-2 ${getOutcomeColor(pred.outcome)} transition-all duration-200`}
        >
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                {getOutcomeIcon(pred.outcome)}
                <h3 className="text-xl font-bold text-gray-900">
                  {pred.away_team} @ {pred.home_team}
                </h3>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  pred.outcome === 'correct' ? 'bg-green-200 text-green-800' :
                  pred.outcome === 'incorrect' ? 'bg-red-200 text-red-800' :
                  'bg-amber-200 text-amber-800'
                }`}>
                  {pred.outcome === 'pending' ? 'Pending' : pred.outcome === 'correct' ? 'Correct' : 'Incorrect'}
                </span>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Predicted:</span>
                  <p className="font-bold text-gray-900">{pred.predicted_winner}</p>
                </div>
                {pred.actual_winner && (
                  <div>
                    <span className="text-gray-600">Actual:</span>
                    <p className="font-bold text-gray-900">{pred.actual_winner}</p>
                  </div>
                )}
                <div>
                  <span className="text-gray-600">Confidence:</span>
                  <p className="font-bold text-gray-900">{Math.round(pred.confidence * 100)}%</p>
                </div>
                <div>
                  <span className="text-gray-600">Locked:</span>
                  <p className="font-bold text-gray-900">
                    {new Date(pred.locked_date).toLocaleDateString()}
                  </p>
                </div>
              </div>

              <div className="mt-3 flex gap-2">
                <div className="flex-1 bg-gray-100 rounded p-2">
                  <div className="text-xs text-gray-600">Home Win Prob</div>
                  <div className="text-lg font-bold text-gray-900">
                    {Math.round(pred.home_win_probability * 100)}%
                  </div>
                </div>
                <div className="flex-1 bg-gray-100 rounded p-2">
                  <div className="text-xs text-gray-600">Away Win Prob</div>
                  <div className="text-lg font-bold text-gray-900">
                    {Math.round(pred.away_win_probability * 100)}%
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={() => analyzePrediction(pred.prediction_id)}
              disabled={analyzingId === pred.prediction_id}
              className="ml-4 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-bold py-2 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 flex items-center gap-2"
            >
              {analyzingId === pred.prediction_id ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <TrendingUp size={16} />
                  {expandedId === pred.prediction_id ? 'Hide Analysis' : 'Analyze'}
                </>
              )}
            </button>
          </div>

          {expandedId === pred.prediction_id && analysis[pred.prediction_id] && (
            <div className="mt-4 pt-4 border-t-2 border-gray-300">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 mb-4">
                <h4 className="font-bold text-gray-900 mb-2 flex items-center gap-2">
                  <AlertCircle size={20} />
                  Analysis Results
                </h4>
                {analysis[pred.prediction_id].was_correct ? (
                  <div className="space-y-2">
                    <p className="text-green-700 font-semibold">✓ Prediction was CORRECT</p>
                    {analysis[pred.prediction_id].success_factors && (
                      <ul className="list-disc list-inside text-gray-700 space-y-1">
                        {analysis[pred.prediction_id].success_factors!.map((factor, idx) => (
                          <li key={idx}>{factor}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-red-700 font-semibold">✗ Prediction was INCORRECT</p>
                    {analysis[pred.prediction_id].error_factors && (
                      <ul className="list-disc list-inside text-gray-700 space-y-1">
                        {analysis[pred.prediction_id].error_factors!.map((factor, idx) => (
                          <li key={idx}>{factor}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>

              {analysis[pred.prediction_id].factors_analysis && (
                <div className="space-y-3">
                  <h5 className="font-semibold text-gray-900">Factor Analysis:</h5>
                  
                  {analysis[pred.prediction_id].factors_analysis.weather && (
                    <div className="bg-white rounded p-3 border border-gray-200">
                      <div className="font-semibold text-gray-900">Weather Impact</div>
                      <p className="text-sm text-gray-700">
                        {analysis[pred.prediction_id].factors_analysis.weather.description}
                      </p>
                    </div>
                  )}

                  {analysis[pred.prediction_id].factors_analysis.coaching && (
                    <div className="bg-white rounded p-3 border border-gray-200">
                      <div className="font-semibold text-gray-900">Coaching Impact</div>
                      <p className="text-sm text-gray-700">
                        Adjustment: {(analysis[pred.prediction_id].factors_analysis.coaching.adjustment * 100).toFixed(1)}%
                      </p>
                      <p className="text-sm text-gray-700">
                        {analysis[pred.prediction_id].factors_analysis.coaching.insight}
                      </p>
                    </div>
                  )}

                  {analysis[pred.prediction_id].factors_analysis.injuries && (
                    <div className="bg-white rounded p-3 border border-gray-200">
                      <div className="font-semibold text-gray-900">Injury Impact</div>
                      <p className="text-sm text-gray-700">
                        Home: {(analysis[pred.prediction_id].factors_analysis.injuries.home_impact * 100).toFixed(1)}% | 
                        Away: {(analysis[pred.prediction_id].factors_analysis.injuries.away_impact * 100).toFixed(1)}%
                      </p>
                    </div>
                  )}

                  {analysis[pred.prediction_id].factors_analysis.mental_health && (
                    <div className="bg-white rounded p-3 border border-gray-200">
                      <div className="font-semibold text-gray-900">Mental Health Impact</div>
                      <p className="text-sm text-gray-700">
                        Net Adjustment: {(analysis[pred.prediction_id].factors_analysis.mental_health.net_adjustment * 100).toFixed(1)}%
                      </p>
                      <p className="text-sm text-gray-700">
                        {analysis[pred.prediction_id].factors_analysis.mental_health.summary}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

