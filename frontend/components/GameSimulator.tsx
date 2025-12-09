'use client'

import { useState } from 'react'
import { Play, BarChart3, TrendingUp } from 'lucide-react'
import axios from 'axios'

interface GameSimulatorProps {
  gameId: string
  homeTeam: string
  awayTeam: string
}

export default function GameSimulator({ gameId, homeTeam, awayTeam }: GameSimulatorProps) {
  const [simulating, setSimulating] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [numSimulations, setNumSimulations] = useState(10000)

  const runSimulation = async () => {
    setSimulating(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
      const response = await axios.get(
        `${apiUrl}/api/simulations/simulate-game/${gameId}?num_simulations=${numSimulations}`
      )
      setResults(response.data)
    } catch (error) {
      console.error('Simulation error:', error)
    } finally {
      setSimulating(false)
    }
  }

  return (
    <div className="bg-latte-50 rounded-lg p-6 border-4 border-cozy-300 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <BarChart3 className="text-gray-900 mr-3" size={28} />
          <h3 className="text-xl font-heading font-bold text-gray-900 tracking-tight">Monte Carlo Simulation</h3>
        </div>
        <button
          onClick={runSimulation}
          disabled={simulating}
          className="bg-gradient-to-r from-cozy-500 to-terracotta-500 hover:from-cozy-600 hover:to-terracotta-600 text-white px-4 py-2 rounded-lg font-semibold disabled:opacity-50 flex items-center"
        >
          <Play size={18} className="mr-2" />
          {simulating ? 'Running...' : 'Run Simulation'}
        </button>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-900 mb-2">
          Number of Simulations: {numSimulations.toLocaleString()}
        </label>
        <input
          type="range"
          value={numSimulations}
          onChange={(e) => setNumSimulations(Number(e.target.value))}
          min="1000"
          max="50000"
          step="1000"
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-900 mt-1">
          <span>1,000</span>
          <span>50,000</span>
        </div>
      </div>

      {results && (
        <div className="space-y-4">
          {/* Win Probabilities */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-warm-50 p-4 rounded-lg border-2 border-warm-400">
              <div className="text-sm font-semibold text-gray-900 mb-2">{homeTeam}</div>
              <div className="text-2xl font-bold text-gray-900">
                {(results.simulated_win_probabilities.home * 100).toFixed(1)}%
              </div>
              <div className="text-xs text-gray-900 mt-1">
                Predicted: {(results.predicted_win_probabilities.home * 100).toFixed(1)}%
              </div>
            </div>
            <div className="bg-cozy-50 p-4 rounded-lg border-2 border-cozy-400">
              <div className="text-sm font-semibold text-gray-900 mb-2">{awayTeam}</div>
              <div className="text-2xl font-bold text-gray-900">
                {(results.simulated_win_probabilities.away * 100).toFixed(1)}%
              </div>
              <div className="text-xs text-gray-900 mt-1">
                Predicted: {(results.predicted_win_probabilities.away * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Score Difference Stats */}
          {results.score_difference_stats && (
            <div className="bg-gradient-to-r from-amber-50 to-warm-50 p-4 rounded-lg border-2 border-amber-400">
              <h4 className="text-sm font-bold text-gray-900 mb-3 flex items-center">
                <TrendingUp className="mr-2" size={16} />
                Score Difference Distribution
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-2 text-xs">
                <div>
                  <div className="text-gray-900 font-semibold">Mean</div>
                  <div className="text-gray-900 font-bold">
                    {results.score_difference_stats.mean > 0 ? '+' : ''}
                    {results.score_difference_stats.mean.toFixed(1)}
                  </div>
                </div>
                {Object.entries(results.score_difference_stats.percentiles).map(([key, value]: [string, any]) => (
                  <div key={key}>
                    <div className="text-gray-900 font-semibold">{key.toUpperCase()}</div>
                    <div className="text-gray-900 font-bold">
                      {value > 0 ? '+' : ''}{value.toFixed(1)}
                    </div>
                  </div>
                ))}
              </div>
              {results.score_difference_stats.confidence_95 && (
                <div className="mt-3 text-xs text-gray-900">
                  <strong>95% Confidence:</strong> {homeTeam} wins by{' '}
                  {results.score_difference_stats.confidence_95.lower.toFixed(1)} to{' '}
                  {results.score_difference_stats.confidence_95.upper.toFixed(1)} points
                </div>
              )}
            </div>
          )}

          {/* Simulation Stats */}
          <div className="bg-amber-100 p-3 rounded-lg border-2 border-amber-400 text-xs">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="font-semibold text-yellow-600">Simulations Run:</span>
                <span className="text-yellow-700 ml-2 font-bold">{results.num_simulations.toLocaleString()}</span>
              </div>
              <div>
                <span className="font-semibold text-yellow-600">Home Wins:</span>
                <span className="text-yellow-700 ml-2 font-bold">{results.simulation_results.home_wins.toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {!results && (
        <div className="text-center py-8 text-gray-900">
          <p className="text-sm">Click "Run Simulation" to generate Monte Carlo results</p>
          <p className="text-xs mt-2">More simulations = more accurate results (but slower)</p>
        </div>
      )}
    </div>
  )
}

