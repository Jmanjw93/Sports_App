'use client'

import { useState } from 'react'
import axios from 'axios'
import { Calendar, MapPin, TrendingUp, Cloud, ChevronDown, ChevronUp, Trophy, Loader2 } from 'lucide-react'
import ConfidenceBar from './ConfidenceBar'
import GameSimulator from './GameSimulator'

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
  weather_impact?: {
    weather?: {
      location?: string
      temp?: number
      conditions?: string
      wind_speed?: number
      precipitation?: number
      description?: string
    }
    weather_impact?: {
      factors?: string[]
      overall_impact?: string
      severity?: string
    }
    adjustment_factor?: number
  }
  injury_impact?: {
    home_injury_impact: number
    away_injury_impact: number
    adjustment: number
    home_key_injuries: Array<{
      player: string
      team: string
      position: string
      injury: string
      status: string
    }>
    away_key_injuries: Array<{
      player: string
      team: string
      position: string
      injury: string
      status: string
    }>
    impact_descriptions: {
      home: string[]
      away: string[]
    }
  }
  mental_health_impact?: {
    home_team?: {
      overall_score: number
      team_chemistry: number
      morale: number
      pressure_handling: number
      impact_on_win_probability: number
      factors: string[]
      key_players: Array<{
        player_name: string
        position: string
        overall_score: number
        confidence_level: number
        stress_level: number
        focus_level: number
        motivation_level: number
        recent_trend: string
        factors: string[]
        impact_on_performance: number
      }>
    }
    away_team?: {
      overall_score: number
      team_chemistry: number
      morale: number
      pressure_handling: number
      impact_on_win_probability: number
      factors: string[]
      key_players: Array<{
        player_name: string
        position: string
        overall_score: number
        confidence_level: number
        stress_level: number
        focus_level: number
        motivation_level: number
        recent_trend: string
        factors: string[]
        impact_on_performance: number
      }>
    }
    net_adjustment: number
    summary: string
  }
  coaching_impact?: {
    home_coach: string
    away_coach: string
    home_team?: string
    away_team?: string
    adjustment_factor: number
    historical_record?: {
      home_coach: string
      away_coach: string
      num_games: number
      home_coach_wins: number
      away_coach_wins: number
      home_coach_record?: string
      away_coach_record?: string
      home_coach_win_rate: number
      away_coach_win_rate: number
      current_streak?: {
        coach: string
        length: number
        description: string
      }
    }
    key_insight: string
  }
  player_prop_adjustment?: any
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
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/predictions/game/${game.game_id}`
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
    try {
      // Handle ISO format dates
      let date: Date
      if (dateString.includes('T')) {
        date = new Date(dateString)
      } else {
        // If no timezone info, assume it's already in local time
        date = new Date(dateString + 'T13:00:00')
      }
      
      // Check if date is valid
      if (isNaN(date.getTime())) {
        console.error('Invalid date:', dateString)
        return 'Date TBD'
      }
      
      // Format the date
      const formatted = date.toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        timeZoneName: 'short'
      })
      
      return formatted
    } catch (error) {
      console.error('Error formatting date:', error, dateString)
      return 'Date TBD'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.7) return 'text-gray-900'
    if (confidence > 0.5) return 'text-gray-900'
    return 'text-gray-900'
  }

  return (
    <div className="bg-latte-50 rounded-lg p-6 border-4 border-warm-300 hover:border-warm-500 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-warm-300/50 backdrop-blur-sm">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-heading font-bold text-gray-900 mb-1 tracking-tight">{game.away_team}</h3>
          <p className="text-gray-900 text-sm font-sans font-bold">@</p>
          <h3 className="text-xl font-heading font-bold text-gray-900 tracking-tight">{game.home_team}</h3>
        </div>
        {prediction && (
          <div className={`text-right ${getConfidenceColor(prediction.confidence)}`}>
            <div className="text-2xl font-bold">
              {Math.round(prediction.confidence * 100)}%
            </div>
            <div className="text-xs text-gray-800 font-semibold">Confidence</div>
          </div>
        )}
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center text-gray-900 text-sm font-medium">
          <Calendar size={16} className="mr-2 text-gray-800" />
          {formatDate(game.date)}
        </div>
        <div className="flex items-center text-gray-900 text-sm font-medium">
          <MapPin size={16} className="mr-2 text-terracotta-500" />
          {game.location.city}, {game.location.state}
        </div>
      </div>

      {expanded && prediction && (
        <div className="mt-4 pt-4 border-t-2 border-warm-300">
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-900 text-sm font-semibold">Predicted Winner:</span>
              <span className="text-gray-900 font-bold text-lg">
                {prediction.predicted_winner}
                {/* Show indicator if probabilities don't match predicted winner */}
                {((prediction.predicted_winner === game.home_team && prediction.away_win_probability > prediction.home_win_probability) ||
                  (prediction.predicted_winner === game.away_team && prediction.home_win_probability > prediction.away_win_probability)) && (
                  <span className="text-terracotta-600 text-xs ml-2">⚠️</span>
                )}
              </span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-900 text-sm font-semibold">Home Win Probability:</span>
              <span className={`font-semibold text-lg ${
                prediction.home_win_probability > prediction.away_win_probability 
                  ? 'text-gray-900' 
                  : 'text-gray-600'
              }`}>
                {Math.round(prediction.home_win_probability * 100)}%
                {prediction.home_win_probability > prediction.away_win_probability && (
                  <span className="text-amber-600 text-xs ml-1">↑</span>
                )}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-900 text-sm font-semibold">Away Win Probability:</span>
              <span className={`font-semibold text-lg ${
                prediction.away_win_probability > prediction.home_win_probability 
                  ? 'text-gray-900' 
                  : 'text-gray-600'
              }`}>
                {Math.round(prediction.away_win_probability * 100)}%
                {prediction.away_win_probability > prediction.home_win_probability && (
                  <span className="text-amber-600 text-xs ml-1">↑</span>
                )}
              </span>
            </div>
            {/* Validation message if probabilities don't add up to 100% */}
            {Math.abs((prediction.home_win_probability + prediction.away_win_probability) - 1.0) > 0.01 && (
              <div className="mt-2 text-xs text-terracotta-600 font-semibold">
                ⚠️ Probabilities sum to {Math.round((prediction.home_win_probability + prediction.away_win_probability) * 100)}%
              </div>
            )}
          </div>

          {prediction.weather_impact && (
            <div className="mb-4 p-3 bg-warm-50 rounded-lg border-2 border-warm-400 shadow-md">
              <div className="flex items-center mb-2">
                <Cloud size={16} className="mr-2 text-gray-800" />
                <span className="text-sm font-semibold text-gray-900">Weather Impact</span>
              </div>
              <div className="text-xs text-gray-900 space-y-1 font-medium">
                {/* Show weather location */}
                {prediction.weather_impact.weather && prediction.weather_impact.weather.location && (
                  <div className="text-gray-900 font-bold">
                    Location: {prediction.weather_impact.weather.location}
                  </div>
                )}
                
                {/* Show weather conditions */}
                {prediction.weather_impact.weather && (
                  <div>
                    <span className="capitalize">
                      {prediction.weather_impact.weather.conditions || 'Clear conditions'}
                    </span>
                    {prediction.weather_impact.weather.temp && (
                      <span> - {Math.round(prediction.weather_impact.weather.temp)}°F</span>
                    )}
                    {prediction.weather_impact.weather.wind_speed && (
                      <span>, Wind: {Math.round(prediction.weather_impact.weather.wind_speed)} mph</span>
                    )}
                    {prediction.weather_impact.weather.precipitation && prediction.weather_impact.weather.precipitation > 0 && (
                      <span>, Precipitation: {prediction.weather_impact.weather.precipitation.toFixed(2)} in</span>
                    )}
                  </div>
                )}
                
                {/* Show impact factors */}
                {prediction.weather_impact.weather_impact && prediction.weather_impact.weather_impact.factors && prediction.weather_impact.weather_impact.factors.length > 0 && (
                  <div className="text-gray-900 mt-1">
                    <span className="font-bold text-gray-900">Impact: </span>
                    {prediction.weather_impact.weather_impact.factors.join(', ')}
                  </div>
                )}
                
                {/* Show adjustment if significant */}
                {prediction.weather_impact.adjustment_factor && Math.abs(prediction.weather_impact.adjustment_factor) > 0.01 && (
                  <div className="text-gray-900 mt-1 font-semibold">
                    Win probability adjustment: {prediction.weather_impact.adjustment_factor > 0 ? '+' : ''}
                    {(prediction.weather_impact.adjustment_factor * 100).toFixed(1)}%
                  </div>
                )}
              </div>
            </div>
          )}

          {prediction.coaching_impact && prediction.coaching_impact.key_insight && (
            <div className="mb-4 p-3 bg-amber-50 rounded-lg border-2 border-amber-400 shadow-md">
              <div className="flex items-center mb-2">
                <span className="text-sm font-semibold text-gray-900">📊 Coaching Matchup</span>
              </div>
              
              {/* Coach names and win/loss records */}
              {prediction.coaching_impact.historical_record && (
                <div className="mb-3 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-900 font-semibold">
                      {prediction.coaching_impact.home_coach}
                      {prediction.coaching_impact.home_team && (
                        <span className="text-gray-800 font-normal ml-1">
                          ({prediction.coaching_impact.home_team})
                        </span>
                      )}
                    </span>
                    <span className="text-gray-900 font-bold">
                      {prediction.coaching_impact.historical_record.home_coach_record || 
                       `${prediction.coaching_impact.historical_record.home_coach_wins}-${prediction.coaching_impact.historical_record.away_coach_wins}`}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-gray-900 font-semibold">
                      {prediction.coaching_impact.away_coach}
                      {prediction.coaching_impact.away_team && (
                        <span className="text-gray-900 font-normal ml-1">
                          ({prediction.coaching_impact.away_team})
                        </span>
                      )}
                    </span>
                    <span className="text-terracotta-600 font-bold">
                      {prediction.coaching_impact.historical_record.away_coach_record || 
                       `${prediction.coaching_impact.historical_record.away_coach_wins}-${prediction.coaching_impact.historical_record.home_coach_wins}`}
                    </span>
                  </div>
                  {prediction.coaching_impact.historical_record.num_games > 0 && (
                    <div className="text-xs text-gray-900 pt-1 border-t-2 border-warm-300 font-medium">
                      {prediction.coaching_impact.historical_record.num_games} total meetings
                      {prediction.coaching_impact.historical_record.current_streak?.description && (
                        <span className="ml-2 text-gray-900 font-semibold">
                          • {prediction.coaching_impact.historical_record.current_streak.description}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              )}
              
              <div className="text-xs text-gray-900 font-medium">
                {prediction.coaching_impact.key_insight}
              </div>
              {prediction.coaching_impact.adjustment_factor !== undefined && prediction.coaching_impact.adjustment_factor !== 0 && (
                <div className="text-xs text-gray-900 mt-1 font-semibold">
                  Adjustment: {prediction.coaching_impact.adjustment_factor > 0 ? '+' : ''}
                  {(prediction.coaching_impact.adjustment_factor * 100).toFixed(1)}% win probability
                </div>
              )}
            </div>
          )}

          {prediction.mental_health_impact && (
            <div className="mb-4 p-3 bg-gradient-to-r from-warm-50 via-amber-50 to-cozy-50 rounded-lg border-2 border-amber-400 shadow-md">
              <div className="flex items-center mb-2">
                <span className="text-sm font-semibold text-gray-900">🧠 Mental Health & Psychology</span>
              </div>
              
              {/* Summary */}
              {prediction.mental_health_impact.summary && (
                <div className="text-xs text-gray-900 mb-3 font-medium bg-white/60 p-2 rounded">
                  {prediction.mental_health_impact.summary}
                </div>
              )}
              
              {/* Home Team Mental Health */}
              {prediction.mental_health_impact.home_team && (
                <div className="mb-3 p-2 bg-white/60 rounded">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-gray-900">{prediction.home_team}</span>
                    <span className="text-xs font-semibold text-gray-900">
                      Score: {(prediction.mental_health_impact.home_team.overall_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-xs mb-2">
                    <div>
                      <span className="text-gray-900 font-semibold">Chemistry:</span>
                      <span className="text-gray-900 ml-1">
                        {(prediction.mental_health_impact.home_team.team_chemistry * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-900 font-semibold">Morale:</span>
                      <span className="text-gray-900 ml-1">
                        {(prediction.mental_health_impact.home_team.morale * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-900 font-semibold">Pressure:</span>
                      <span className="text-gray-900 ml-1">
                        {(prediction.mental_health_impact.home_team.pressure_handling * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  {prediction.mental_health_impact.home_team.factors && prediction.mental_health_impact.home_team.factors.length > 0 && (
                    <div className="text-xs text-gray-900">
                      <span className="font-semibold">Factors: </span>
                      {prediction.mental_health_impact.home_team.factors.join(', ')}
                    </div>
                  )}
                  {prediction.mental_health_impact.home_team.key_players && prediction.mental_health_impact.home_team.key_players.length > 0 && (
                    <details className="mt-2">
                      <summary className="text-xs text-gray-900 font-semibold cursor-pointer">Key Players Mental Health</summary>
                      <div className="mt-1 space-y-1 pl-2">
                        {prediction.mental_health_impact.home_team.key_players.slice(0, 3).map((player, idx) => (
                          <div key={idx} className="text-xs bg-white/40 p-1 rounded">
                            <span className="font-semibold text-gray-900">{player.player_name}</span>
                            <span className="text-gray-800 ml-1">({player.position})</span>
                            <div className="text-xs text-gray-900 mt-0.5">
                              Confidence: {(player.confidence_level * 100).toFixed(0)}% | 
                              Stress: {(player.stress_level * 100).toFixed(0)}% | 
                              Trend: <span className={player.recent_trend === 'improving' ? 'text-gray-900' : player.recent_trend === 'declining' ? 'text-terracotta-600' : 'text-gray-900'}>{player.recent_trend}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </details>
                  )}
                </div>
              )}
              
              {/* Away Team Mental Health */}
              {prediction.mental_health_impact.away_team && (
                <div className="mb-3 p-2 bg-white/60 rounded">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold text-gray-900">{prediction.away_team}</span>
                    <span className="text-xs font-semibold text-gray-900">
                      Score: {(prediction.mental_health_impact.away_team.overall_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-2 text-xs mb-2">
                    <div>
                      <span className="text-gray-900 font-semibold">Chemistry:</span>
                      <span className="text-gray-900 ml-1">
                        {(prediction.mental_health_impact.away_team.team_chemistry * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-900 font-semibold">Morale:</span>
                      <span className="text-gray-900 ml-1">
                        {(prediction.mental_health_impact.away_team.morale * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-terracotta-600 font-semibold">Pressure:</span>
                      <span className="text-terracotta-700 ml-1">
                        {(prediction.mental_health_impact.away_team.pressure_handling * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  {prediction.mental_health_impact.away_team.factors && prediction.mental_health_impact.away_team.factors.length > 0 && (
                    <div className="text-xs text-gray-900">
                      <span className="font-semibold">Factors: </span>
                      {prediction.mental_health_impact.away_team.factors.join(', ')}
                    </div>
                  )}
                  {prediction.mental_health_impact.away_team.key_players && prediction.mental_health_impact.away_team.key_players.length > 0 && (
                    <details className="mt-2">
                      <summary className="text-xs text-gray-900 font-semibold cursor-pointer">Key Players Mental Health</summary>
                      <div className="mt-1 space-y-1 pl-2">
                        {prediction.mental_health_impact.away_team.key_players.slice(0, 3).map((player, idx) => (
                          <div key={idx} className="text-xs bg-white/40 p-1 rounded">
                            <span className="font-semibold text-gray-900">{player.player_name}</span>
                            <span className="text-gray-900 ml-1">({player.position})</span>
                            <div className="text-xs text-gray-900 mt-0.5">
                              Confidence: {(player.confidence_level * 100).toFixed(0)}% | 
                              Stress: {(player.stress_level * 100).toFixed(0)}% | 
                              Trend: <span className={player.recent_trend === 'improving' ? 'text-gray-900' : player.recent_trend === 'declining' ? 'text-terracotta-600' : 'text-gray-900'}>{player.recent_trend}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </details>
                  )}
                </div>
              )}
              
              {/* Net Adjustment */}
              {prediction.mental_health_impact.net_adjustment !== undefined && Math.abs(prediction.mental_health_impact.net_adjustment) > 0.01 && (
                <div className="text-xs text-gray-900 mt-2 font-bold bg-sunny-200/60 p-2 rounded text-center">
                  Net Impact: {prediction.mental_health_impact.net_adjustment > 0 ? '+' : ''}
                  {(prediction.mental_health_impact.net_adjustment * 100).toFixed(1)}% win probability adjustment
                </div>
              )}
            </div>
          )}

          {prediction.injury_impact && (
            <div className="mb-4 p-3 bg-terracotta-50 rounded-lg border-2 border-terracotta-400 shadow-md">
              <div className="flex items-center mb-2">
                <span className="text-sm font-semibold text-terracotta-600">⚠️ Injury Impact</span>
              </div>
              <div className="space-y-2 text-xs">
                {prediction.injury_impact.home_key_injuries && prediction.injury_impact.home_key_injuries.length > 0 && (
                  <div>
                    <span className="text-gray-900 font-semibold">Home Team:</span>
                    <ul className="list-disc list-inside ml-2 text-gray-900 font-medium">
                      {prediction.injury_impact.home_key_injuries.map((inj: any, idx: number) => (
                        <li key={idx}>
                          {inj.player} ({inj.position}) - {inj.team} - {inj.status.toUpperCase()}: {inj.injury.replace('_', ' ')}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {prediction.injury_impact.away_key_injuries && prediction.injury_impact.away_key_injuries.length > 0 && (
                  <div>
                    <span className="text-gray-900 font-semibold">Away Team:</span>
                    <ul className="list-disc list-inside ml-2 text-gray-900 font-medium">
                      {prediction.injury_impact.away_key_injuries.map((inj: any, idx: number) => (
                        <li key={idx}>
                          {inj.player} ({inj.position}) - {inj.team} - {inj.status.toUpperCase()}: {inj.injury.replace('_', ' ')}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {(prediction.injury_impact.home_injury_impact > 0 || prediction.injury_impact.away_injury_impact > 0) && (
                  <div className="text-gray-900 mt-2 space-y-1">
                    {prediction.injury_impact.home_injury_impact > 0 && (
                      <div className="font-semibold">
                        <span className="text-warm-700">{game.home_team}:</span> {(prediction.injury_impact.home_injury_impact * 100).toFixed(1)}% performance reduction
                      </div>
                    )}
                    {prediction.injury_impact.away_injury_impact > 0 && (
                      <div className="font-semibold">
                        <span className="text-cozy-700">{game.away_team}:</span> {(prediction.injury_impact.away_injury_impact * 100).toFixed(1)}% performance reduction
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {prediction.key_factors && prediction.key_factors.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-semibold text-gray-900 mb-2">Key Factors:</p>
              <ul className="list-disc list-inside text-xs text-gray-900 space-y-1 font-medium">
                {prediction.key_factors.map((factor, idx) => (
                  <li key={idx}>{factor}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Game Simulator */}
          <div className="mt-4">
            <GameSimulator
              gameId={game.game_id}
              homeTeam={game.home_team}
              awayTeam={game.away_team}
            />
          </div>
        </div>
      )}

      <button
        onClick={fetchPrediction}
        disabled={loading}
        className="w-full mt-4 bg-gradient-to-r from-warm-500 to-amber-500 hover:from-sky-600 hover:to-mint-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-[1.02] active:scale-[0.98] shadow-xl shadow-sky-400/50"
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
  )
}

