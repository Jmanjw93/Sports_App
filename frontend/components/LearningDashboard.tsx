'use client'

import { useState, useEffect } from 'react'
import { TrendingUp, TrendingDown, AlertCircle, Lightbulb, Target, BarChart3 } from 'lucide-react'
import axios from 'axios'

interface LearningDashboardProps {
  sport?: string
}

export default function LearningDashboard({ sport = 'nfl' }: LearningDashboardProps) {
  const [accuracy, setAccuracy] = useState<any>(null)
  const [insights, setInsights] = useState<any>(null)
  const [predictions, setPredictions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [sport])

  const fetchData = async () => {
    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
      
      const [accuracyRes, insightsRes, predictionsRes] = await Promise.all([
        axios.get(`${apiUrl}/api/learning/accuracy?sport=${sport}`),
        axios.get(`${apiUrl}/api/learning/insights?sport=${sport}`),
        axios.get(`${apiUrl}/api/learning/predictions?sport=${sport}&limit=20`)
      ])
      
      setAccuracy(accuracyRes.data)
      setInsights(insightsRes.data)
      setPredictions(predictionsRes.data.predictions || [])
    } catch (error) {
      console.error('Error fetching learning data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-900">Loading learning insights...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Lightbulb className="text-amber-600 mr-3" size={28} />
          <h2 className="text-3xl font-heading font-bold text-gray-900 tracking-tight">Learning & Accuracy</h2>
        </div>
        <button
          onClick={fetchData}
          className="bg-gradient-to-r from-amber-500 to-warm-500 hover:from-amber-600 hover:to-warm-600 text-white px-4 py-2 rounded-lg font-semibold"
        >
          Refresh
        </button>
      </div>

      {/* Accuracy Stats */}
      {accuracy && (
        <div className="bg-latte-50 rounded-lg p-6 border-4 border-amber-300 shadow-xl">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Target className="mr-2" size={20} />
            Prediction Accuracy
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4 border-2 border-warm-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Total Predictions</div>
              <div className="text-2xl font-bold text-gray-900">{accuracy.total}</div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-amber-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Correct</div>
              <div className="text-2xl font-bold text-amber-700">{accuracy.correct}</div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-terracotta-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Incorrect</div>
              <div className="text-2xl font-bold text-terracotta-700">{accuracy.incorrect}</div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-cozy-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Accuracy Rate</div>
              <div className="text-2xl font-bold text-cozy-700">
                {(accuracy.accuracy * 100).toFixed(1)}%
              </div>
            </div>
          </div>
          {accuracy.pending > 0 && (
            <div className="mt-4 text-sm text-gray-700">
              <span className="font-semibold">{accuracy.pending}</span> predictions pending results
            </div>
          )}
        </div>
      )}

      {/* Learning Insights */}
      {insights && insights.recommendations && (
        <div className="bg-latte-50 rounded-lg p-6 border-4 border-warm-300 shadow-xl">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Lightbulb className="mr-2" size={20} />
            Learning Insights
          </h3>
          
          {insights.recommendations.recommendations && insights.recommendations.recommendations.length > 0 ? (
            <div className="space-y-4">
              {insights.recommendations.recommendations.map((rec: any, idx: number) => (
                <div key={idx} className="bg-white rounded-lg p-4 border-2 border-amber-300">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center">
                      <AlertCircle className="text-amber-600 mr-2" size={18} />
                      <span className="font-bold text-gray-900">{rec.pattern.replace('_', ' ').toUpperCase()}</span>
                    </div>
                    <div className="text-xs text-gray-600">
                      Frequency: {rec.frequency} • Impact: {rec.impact}
                    </div>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">{rec.description}</p>
                  {Object.keys(rec.adjustment).length > 0 && (
                    <div className="text-xs text-gray-600 mt-2">
                      <span className="font-semibold">Suggested Adjustments:</span>
                      <ul className="list-disc list-inside ml-2 mt-1">
                        {Object.entries(rec.adjustment).map(([key, value]: [string, any]) => (
                          <li key={key}>
                            {key.replace('_', ' ')}: {typeof value === 'number' ? value.toFixed(3) : value}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-600">
              <p>No error patterns detected yet. More prediction data needed for learning insights.</p>
            </div>
          )}
        </div>
      )}

      {/* Recent Predictions */}
      {predictions.length > 0 && (
        <div className="bg-latte-50 rounded-lg p-6 border-4 border-cozy-300 shadow-xl">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <BarChart3 className="mr-2" size={20} />
            Recent Predictions
          </h3>
          <div className="space-y-2">
            {predictions.slice(0, 10).map((pred: any) => (
              <div
                key={pred.prediction_id}
                className={`bg-white rounded-lg p-3 border-2 ${
                  pred.outcome === 'correct'
                    ? 'border-amber-300'
                    : pred.outcome === 'incorrect'
                    ? 'border-terracotta-300'
                    : 'border-gray-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="font-semibold text-gray-900">
                      {pred.away_team} @ {pred.home_team}
                    </div>
                    <div className="text-xs text-gray-600 mt-1">
                      Predicted: <span className="font-semibold">{pred.predicted_winner}</span>
                      {pred.actual_winner && (
                        <>
                          {' • '}Actual: <span className="font-semibold">{pred.actual_winner}</span>
                        </>
                      )}
                    </div>
                    <div className="text-xs text-gray-600">
                      Confidence: {(pred.confidence * 100).toFixed(1)}% • 
                      Probabilities: Home {(pred.home_win_probability * 100).toFixed(1)}% / Away {(pred.away_win_probability * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="ml-4">
                    {pred.outcome === 'correct' && (
                      <span className="px-3 py-1 bg-amber-100 text-amber-800 rounded-full text-xs font-semibold">
                        ✓ Correct
                      </span>
                    )}
                    {pred.outcome === 'incorrect' && (
                      <span className="px-3 py-1 bg-terracotta-100 text-terracotta-800 rounded-full text-xs font-semibold">
                        ✗ Incorrect
                      </span>
                    )}
                    {pred.outcome === 'pending' && (
                      <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-semibold">
                        Pending
                      </span>
                    )}
                  </div>
                </div>
                {pred.error_analysis && pred.error_analysis.errors && pred.error_analysis.errors.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-200">
                    <div className="text-xs text-terracotta-700 font-semibold mb-1">Error Analysis:</div>
                    <ul className="text-xs text-gray-700 space-y-1">
                      {pred.error_analysis.errors.slice(0, 2).map((error: any, idx: number) => (
                        <li key={idx}>• {error.description}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {(!accuracy || accuracy.total === 0) && (
        <div className="bg-latte-50 rounded-lg p-12 border-4 border-warm-300 shadow-xl text-center">
          <Target className="mx-auto mb-4 text-amber-500" size={48} />
          <h3 className="text-xl font-bold text-gray-900 mb-2">No Prediction Data Yet</h3>
          <p className="text-gray-700 mb-6">
            Start making predictions and submit game results to begin learning from accuracy.
          </p>
        </div>
      )}
    </div>
  )
}




