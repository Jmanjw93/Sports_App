'use client'

import { useState, useEffect } from 'react'
import { Plus, X, TrendingUp, DollarSign, AlertCircle, Star, Share2, Save, Calculator } from 'lucide-react'
import axios from 'axios'

interface ParlayBuilderProps {
  sport?: string
}

interface ParlayLeg {
  id: string
  player_name: string
  team: string
  prop_type: string
  prop_value: number
  selection: 'over' | 'under'
  odds: number
  win_probability: number
}

interface ParlayResult {
  parlay_odds: number
  combined_probability: number
  bet_amount: number
  potential_payout: number
  total_return: number
  expected_value: number
  ev_percentage: number
  risk_metrics: {
    win_rate: number
    loss_rate: number
    risk_reward_ratio: number
    kelly_percentage: number
    recommended_bet_percentage: number
  }
  recommendation: string
  recommendation_text: string
  legs: ParlayLeg[]
}

// Mock player data - in production, this would come from an API
const mockPlayers: Array<{
  name: string
  team: string
  props: Array<{
    type: string
    value: number
    over_odds: number
    under_odds: number
    over_prob: number
    under_prob: number
  }>
}> = [
  {
    name: 'Patrick Mahomes',
    team: 'Kansas City Chiefs',
    props: [
      { type: 'Passing Yards', value: 275.5, over_odds: 1.91, under_odds: 1.91, over_prob: 0.58, under_prob: 0.42 },
      { type: 'Passing TDs', value: 2.5, over_odds: 1.83, under_odds: 1.95, over_prob: 0.60, under_prob: 0.40 },
      { type: 'Completions', value: 24.5, over_odds: 1.87, under_odds: 1.93, over_prob: 0.55, under_prob: 0.45 }
    ]
  },
  {
    name: 'Josh Allen',
    team: 'Buffalo Bills',
    props: [
      { type: 'Passing Yards', value: 265.5, over_odds: 1.91, under_odds: 1.91, over_prob: 0.57, under_prob: 0.43 },
      { type: 'Passing TDs', value: 2.5, over_odds: 1.83, under_odds: 1.95, over_prob: 0.60, under_prob: 0.40 },
      { type: 'Rushing Yards', value: 45.5, over_odds: 1.87, under_odds: 1.93, over_prob: 0.52, under_prob: 0.48 }
    ]
  },
  {
    name: 'Travis Kelce',
    team: 'Kansas City Chiefs',
    props: [
      { type: 'Receiving Yards', value: 75.5, over_odds: 1.91, under_odds: 1.91, over_prob: 0.55, under_prob: 0.45 },
      { type: 'Receptions', value: 6.5, over_odds: 1.87, under_odds: 1.93, over_prob: 0.53, under_prob: 0.47 },
      { type: 'Receiving TDs', value: 0.5, over_odds: 1.65, under_odds: 2.20, over_prob: 0.48, under_prob: 0.52 }
    ]
  },
  {
    name: 'Stefon Diggs',
    team: 'Buffalo Bills',
    props: [
      { type: 'Receiving Yards', value: 85.5, over_odds: 1.91, under_odds: 1.91, over_prob: 0.54, under_prob: 0.46 },
      { type: 'Receptions', value: 7.5, over_odds: 1.87, under_odds: 1.93, over_prob: 0.52, under_prob: 0.48 }
    ]
  }
]

export default function ParlayBuilder({ sport = 'nfl' }: ParlayBuilderProps) {
  const [legs, setLegs] = useState<ParlayLeg[]>([])
  const [betAmount, setBetAmount] = useState(100)
  const [results, setResults] = useState<ParlayResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [selectedPlayer, setSelectedPlayer] = useState<string>('')
  const [selectedProp, setSelectedProp] = useState<string>('')
  const [showAddLeg, setShowAddLeg] = useState(false)

  const calculateParlay = async () => {
    if (legs.length < 2) {
      alert('Parlay must have at least 2 legs')
      return
    }

    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
      const response = await axios.post(`${apiUrl}/api/parlays/calculate`, {
        legs: legs.map(leg => ({
          player_name: leg.player_name,
          team: leg.team,
          prop_type: leg.prop_type,
          prop_value: leg.prop_value,
          selection: leg.selection,
          odds: leg.odds,
          win_probability: leg.win_probability
        })),
        bet_amount: betAmount
      })
      setResults(response.data)
    } catch (error: any) {
      console.error('Parlay calculation error:', error)
      alert(error.response?.data?.detail || 'Error calculating parlay')
    } finally {
      setLoading(false)
    }
  }

  const addLeg = () => {
    if (!selectedPlayer || !selectedProp) return

    const player = mockPlayers.find(p => p.name === selectedPlayer)
    if (!player) return

    const prop = player.props.find(p => `${p.type} ${p.value}` === selectedProp)
    if (!prop) return

    const selection = prop.over_prob > prop.under_prob ? 'over' : 'under'
    const odds = selection === 'over' ? prop.over_odds : prop.under_odds
    const winProb = selection === 'over' ? prop.over_prob : prop.under_prob

    const newLeg: ParlayLeg = {
      id: Date.now().toString(),
      player_name: player.name,
      team: player.team,
      prop_type: prop.type,
      prop_value: prop.value,
      selection,
      odds,
      win_probability: winProb
    }

    setLegs([...legs, newLeg])
    setSelectedPlayer('')
    setSelectedProp('')
    setShowAddLeg(false)
  }

  const removeLeg = (id: string) => {
    setLegs(legs.filter(leg => leg.id !== id))
    setResults(null)
  }

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'strong_parlay':
        return 'bg-amber-100 border-amber-500 text-amber-800'
      case 'moderate_parlay':
        return 'bg-warm-100 border-warm-500 text-warm-800'
      case 'small_parlay':
        return 'bg-cozy-100 border-cozy-500 text-cozy-800'
      default:
        return 'bg-terracotta-100 border-terracotta-500 text-terracotta-800'
    }
  }

  const availableProps = selectedPlayer
    ? mockPlayers.find(p => p.name === selectedPlayer)?.props || []
    : []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Star className="text-amber-600 mr-3" size={28} />
          <h2 className="text-3xl font-heading font-bold text-gray-900 tracking-tight">Parlay Builder</h2>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowAddLeg(true)}
            className="bg-gradient-to-r from-amber-500 to-warm-500 hover:from-amber-600 hover:to-warm-600 text-white px-4 py-2 rounded-lg font-semibold flex items-center"
          >
            <Plus size={18} className="mr-2" />
            Add Leg
          </button>
        </div>
      </div>

      {/* Add Leg Modal */}
      {showAddLeg && (
        <div className="bg-latte-50 rounded-lg p-6 border-4 border-amber-300 shadow-xl mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold text-gray-900">Add Parlay Leg</h3>
            <button
              onClick={() => {
                setShowAddLeg(false)
                setSelectedPlayer('')
                setSelectedProp('')
              }}
              className="text-gray-600 hover:text-gray-900"
            >
              <X size={20} />
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-900 mb-2">Select Player</label>
              <select
                value={selectedPlayer}
                onChange={(e) => {
                  setSelectedPlayer(e.target.value)
                  setSelectedProp('')
                }}
                className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-500"
              >
                <option value="">Choose a player...</option>
                {mockPlayers.map((player) => (
                  <option key={player.name} value={player.name}>
                    {player.name} ({player.team})
                  </option>
                ))}
              </select>
            </div>

            {selectedPlayer && (
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Select Prop</label>
                <select
                  value={selectedProp}
                  onChange={(e) => setSelectedProp(e.target.value)}
                  className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-500"
                >
                  <option value="">Choose a prop...</option>
                  {availableProps.map((prop) => (
                    <option key={`${prop.type}-${prop.value}`} value={`${prop.type} ${prop.value}`}>
                      {prop.type} {prop.value} (Over: {prop.over_odds.toFixed(2)}, Under: {prop.under_odds.toFixed(2)})
                    </option>
                  ))}
                </select>
              </div>
            )}

            <button
              onClick={addLeg}
              disabled={!selectedPlayer || !selectedProp}
              className="w-full bg-amber-500 hover:bg-amber-600 text-white px-4 py-2 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Add to Parlay
            </button>
          </div>
        </div>
      )}

      {/* Parlay Legs */}
      {legs.length > 0 && (
        <div className="bg-latte-50 rounded-lg p-6 border-4 border-warm-300 shadow-xl">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Parlay Legs ({legs.length})</h3>
          <div className="space-y-3">
            {legs.map((leg) => (
              <div
                key={leg.id}
                className="bg-white rounded-lg p-4 border-2 border-warm-200 flex items-center justify-between"
              >
                <div className="flex-1">
                  <div className="font-bold text-gray-900">{leg.player_name}</div>
                  <div className="text-sm text-gray-700">
                    {leg.team} • {leg.prop_type} {leg.prop_value} {leg.selection.toUpperCase()}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">
                    Odds: {leg.odds.toFixed(2)} • Win Prob: {(leg.win_probability * 100).toFixed(1)}%
                  </div>
                </div>
                <button
                  onClick={() => removeLeg(leg.id)}
                  className="text-terracotta-600 hover:text-terracotta-800 ml-4"
                >
                  <X size={20} />
                </button>
              </div>
            ))}
          </div>

          {/* Bet Amount and Calculate */}
          <div className="mt-6 pt-6 border-t-2 border-warm-300">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Bet Amount ($)</label>
                <input
                  type="number"
                  value={betAmount}
                  onChange={(e) => setBetAmount(Number(e.target.value))}
                  className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-amber-400 focus:border-amber-500"
                  min="1"
                />
              </div>
              <div className="flex items-end">
                <button
                  onClick={calculateParlay}
                  disabled={loading || legs.length < 2}
                  className="w-full bg-gradient-to-r from-amber-500 to-warm-500 hover:from-amber-600 hover:to-warm-600 text-white px-6 py-2 rounded-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  <Calculator className="mr-2" size={18} />
                  {loading ? 'Calculating...' : 'Calculate Parlay'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="bg-latte-50 rounded-lg p-6 border-4 border-amber-300 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">Parlay Analysis</h3>
            <div className="flex gap-2">
              <button className="p-2 bg-warm-100 hover:bg-warm-200 rounded-lg text-gray-900">
                <Save size={18} />
              </button>
              <button className="p-2 bg-warm-100 hover:bg-warm-200 rounded-lg text-gray-900">
                <Share2 size={18} />
              </button>
            </div>
          </div>

          {/* Recommendation */}
          <div className={`p-4 rounded-lg border-2 mb-4 ${getRecommendationColor(results.recommendation)}`}>
            <div className="font-bold text-lg">{results.recommendation_text}</div>
            <div className="text-sm mt-1">Expected Value: {results.ev_percentage > 0 ? '+' : ''}{results.ev_percentage.toFixed(2)}%</div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg p-4 border-2 border-amber-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Parlay Odds</div>
              <div className="text-2xl font-bold text-gray-900">{results.parlay_odds.toFixed(2)}</div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-warm-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Win Probability</div>
              <div className="text-2xl font-bold text-gray-900">{(results.combined_probability * 100).toFixed(1)}%</div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-cozy-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Potential Payout</div>
              <div className="text-2xl font-bold text-gray-900">${results.potential_payout.toFixed(2)}</div>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-amber-300">
              <div className="text-xs text-gray-600 font-semibold mb-1">Total Return</div>
              <div className="text-2xl font-bold text-gray-900">${results.total_return.toFixed(2)}</div>
            </div>
          </div>

          {/* Risk Analysis */}
          <div className="bg-gradient-to-r from-warm-50 to-amber-50 rounded-lg p-4 border-2 border-warm-300 mb-4">
            <h4 className="font-bold text-gray-900 mb-3">Risk Analysis</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
              <div>
                <span className="text-gray-700 font-semibold">Win Rate:</span>
                <span className="text-gray-900 ml-2 font-bold">{(results.risk_metrics.win_rate * 100).toFixed(1)}%</span>
              </div>
              <div>
                <span className="text-gray-700 font-semibold">Risk/Reward:</span>
                <span className="text-gray-900 ml-2 font-bold">1:{results.risk_metrics.risk_reward_ratio.toFixed(2)}</span>
              </div>
              <div>
                <span className="text-gray-700 font-semibold">Expected Value:</span>
                <span className={`ml-2 font-bold ${results.expected_value >= 0 ? 'text-gray-900' : 'text-terracotta-700'}`}>
                  ${results.expected_value.toFixed(2)}
                </span>
              </div>
              <div>
                <span className="text-gray-700 font-semibold">Recommended Bet:</span>
                <span className="text-gray-900 ml-2 font-bold">{results.risk_metrics.recommended_bet_percentage.toFixed(2)}%</span>
              </div>
            </div>
          </div>

          {/* Parlay Breakdown */}
          <div className="bg-white rounded-lg p-4 border-2 border-warm-200">
            <h4 className="font-bold text-gray-900 mb-3">Parlay Breakdown</h4>
            <div className="space-y-2">
              {results.legs.map((leg, idx) => (
                <div key={idx} className="flex justify-between items-center text-sm">
                  <span className="text-gray-700">
                    Leg {idx + 1}: {leg.player_name} - {leg.prop_type} {leg.prop_value} {leg.selection}
                  </span>
                  <span className="text-gray-900 font-semibold">
                    {(leg.win_probability * 100).toFixed(1)}% • {leg.odds.toFixed(2)}x
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {legs.length === 0 && (
        <div className="bg-latte-50 rounded-lg p-12 border-4 border-warm-300 shadow-xl text-center">
          <Star className="mx-auto mb-4 text-amber-500" size={48} />
          <h3 className="text-xl font-bold text-gray-900 mb-2">Start Building Your Parlay</h3>
          <p className="text-gray-700 mb-6">Add at least 2 legs to create a parlay bet</p>
          <button
            onClick={() => setShowAddLeg(true)}
            className="bg-gradient-to-r from-amber-500 to-warm-500 hover:from-amber-600 hover:to-warm-600 text-white px-6 py-3 rounded-lg font-bold flex items-center mx-auto"
          >
            <Plus size={20} className="mr-2" />
            Add First Leg
          </button>
        </div>
      )}
    </div>
  )
}


