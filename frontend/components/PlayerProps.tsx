'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'

interface PlayerProp {
  player_name: string
  position: string
  prop_type: string
  prop_name: string
  line: number
  predicted_value: number
  unit: string
  over_probability: number
  under_probability: number
  confidence: number
  ev?: number
  injury_status?: string
  injury_type?: string
  historical_matchup?: {
    team_matchup_factor: number
    coach_matchup_factor: number
    total_adjustment: number
    historical_games: number
  }
  odds?: {
    bet365?: {
      available: boolean
      line: number
      over_odds: number
      under_odds: number
    }
    draftkings?: {
      available: boolean
      line: number
      over_odds: number
      under_odds: number
    }
    thescore_bet?: {
      available: boolean
      line: number
      over_odds: number
      under_odds: number
    }
  }
}

interface PlayerPropsData {
  game_id: string
  home_team: string
  away_team: string
  home_team_props: PlayerProp[]
  away_team_props: PlayerProp[]
}

export default function PlayerProps({ gameId }: { gameId: string }) {
  const [propsData, setPropsData] = useState<PlayerPropsData | null>(null)
  const [loading, setLoading] = useState(false)
  const [expanded, setExpanded] = useState(false)

  const fetchProps = async () => {
    if (propsData) {
      setExpanded(!expanded)
      return
    }

    try {
      setLoading(true)
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/player-props/game/${gameId}`
      )
      setPropsData(response.data)
      setExpanded(true)
    } catch (error) {
      console.error('Error fetching player props:', error)
    } finally {
      setLoading(false)
    }
  }


  const renderProp = (prop: PlayerProp) => {
    const isValueBet = (prop.ev || 0) > 0.05

    return (
      <div key={`${prop.player_name}-${prop.prop_type}`} className="bg-slate-700/50 rounded p-3 mb-2">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-semibold text-white">{prop.player_name}</span>
              <span className="text-xs text-slate-400">({prop.position})</span>
              {prop.injury_status && (
                <span className={`text-xs px-2 py-0.5 rounded ${
                  prop.injury_status === 'out' ? 'bg-red-900/50 text-red-300' :
                  prop.injury_status === 'doubtful' ? 'bg-orange-900/50 text-orange-300' :
                  prop.injury_status === 'questionable' ? 'bg-yellow-900/50 text-yellow-300' :
                  'bg-blue-900/50 text-blue-300'
                }`}>
                  {prop.injury_status.toUpperCase()}
                </span>
              )}
              {prop.historical_matchup && prop.historical_matchup.historical_games > 0 && (
                <span className="text-xs px-2 py-0.5 rounded bg-purple-900/50 text-purple-300" title={`Historical matchup data from ${prop.historical_matchup.historical_games} games`}>
                  📊 Historical Data
                </span>
              )}
            </div>
            <div className="text-sm text-slate-300 mt-1">
              {prop.prop_name}: {prop.line} {prop.unit}
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm font-semibold text-white">
              Pred: {prop.predicted_value.toFixed(1)} {prop.unit}
            </div>
            <div className="text-xs text-slate-400">
              {Math.round(prop.confidence * 100)}% confidence
            </div>
          </div>
        </div>


        {isValueBet && (
          <div className="mt-2 text-xs text-green-400 flex items-center gap-1">
            <TrendingUp size={12} />
            Value Bet Detected (EV: {((prop.ev || 0) * 100).toFixed(1)}%)
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="mt-4">
      <button
        onClick={fetchProps}
        disabled={loading}
        className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {loading ? (
          'Loading Player Props...'
        ) : expanded ? (
          'Hide Player Props'
        ) : (
          <>
            <TrendingUp size={16} className="mr-2" />
            View Player Props
          </>
        )}
      </button>

      {expanded && propsData && (
        <div className="mt-4 space-y-6">
          {/* Home Team Props */}
          <div>
            <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
              <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
              {propsData.home_team} - Player Props
            </h3>
            {propsData.home_team_props.length > 0 ? (
              <div className="space-y-2">
                {propsData.home_team_props.map(prop => renderProp(prop))}
              </div>
            ) : (
              <div className="text-slate-400 text-sm">No player props available</div>
            )}
          </div>

          {/* Away Team Props */}
          <div>
            <h3 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
              <span className="w-3 h-3 bg-red-500 rounded-full"></span>
              {propsData.away_team} - Player Props
            </h3>
            {propsData.away_team_props.length > 0 ? (
              <div className="space-y-2">
                {propsData.away_team_props.map(prop => renderProp(prop))}
              </div>
            ) : (
              <div className="text-slate-400 text-sm">No player props available</div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

