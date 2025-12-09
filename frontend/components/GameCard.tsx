'use client'

import { useState } from 'react'
import axios from 'axios'
import { Calendar, MapPin, TrendingUp, Cloud, ChevronDown, ChevronUp, Trophy, Loader2 } from 'lucide-react'
import ConfidenceBar from './ConfidenceBar'

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
    if (confidence > 0.7) return 'text-mint-600'
    if (confidence > 0.5) return 'text-sky-500'
    return 'text-coral-500'
  }

  return (
    <div className="bg-white/95 rounded-lg p-6 border-4 border-sky-300 hover:border-sky-500 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-sky-300/50 backdrop-blur-sm">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-heading font-bold text-sky-600 mb-1 tracking-tight">{game.away_team}</h3>
          <p className="text-coral-500 text-sm font-sans font-bold">@</p>
          <h3 className="text-xl font-heading font-bold text-mint-600 tracking-tight">{game.home_team}</h3>
        </div>
        {prediction && (
          <div className={`text-right ${getConfidenceColor(prediction.confidence)}`}>
            <div className="text-2xl font-bold">
              {Math.round(prediction.confidence * 100)}%
            </div>
            <div className="text-xs text-sky-500 font-semibold">Confidence</div>
          </div>
        )}
      </div>

      <div className="space-y-2 mb-4">
        <div className="flex items-center text-sky-600 text-sm font-medium">
          <Calendar size={16} className="mr-2 text-coral-500" />
          {formatDate(game.date)}
        </div>
        <div className="flex items-center text-mint-600 text-sm font-medium">
          <MapPin size={16} className="mr-2 text-rose-500" />
          {game.location.city}, {game.location.state}
        </div>
      </div>

      {expanded && prediction && (
        <div className="mt-4 pt-4 border-t-2 border-sky-300">
          <div className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sky-600 text-sm font-semibold">Predicted Winner:</span>
              <span className="text-mint-600 font-bold text-lg">{prediction.predicted_winner}</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sky-600 text-sm font-semibold">Home Win Probability:</span>
              <span className="text-coral-600 font-semibold text-lg">
                {Math.round(prediction.home_win_probability * 100)}%
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sky-600 text-sm font-semibold">Away Win Probability:</span>
              <span className="text-rose-600 font-semibold text-lg">
                {Math.round(prediction.away_win_probability * 100)}%
              </span>
            </div>
          </div>

          {prediction.weather_impact && (
            <div className="mb-4 p-3 bg-sky-100 rounded-lg border-2 border-sky-400 shadow-md">
              <div className="flex items-center mb-2">
                <Cloud size={16} className="mr-2 text-sky-500" />
                <span className="text-sm font-semibold text-sky-600">Weather Impact</span>
              </div>
              <div className="text-xs text-sky-700 space-y-1 font-medium">
                {/* Show weather location */}
                {prediction.weather_impact.weather && prediction.weather_impact.weather.location && (
                  <div className="text-sky-600 font-bold">
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
                  <div className="text-mint-600 mt-1">
                    <span className="font-bold text-mint-700">Impact: </span>
                    {prediction.weather_impact.weather_impact.factors.join(', ')}
                  </div>
                )}
                
                {/* Show adjustment if significant */}
                {prediction.weather_impact.adjustment_factor && Math.abs(prediction.weather_impact.adjustment_factor) > 0.01 && (
                  <div className="text-coral-600 mt-1 font-semibold">
                    Win probability adjustment: {prediction.weather_impact.adjustment_factor > 0 ? '+' : ''}
                    {(prediction.weather_impact.adjustment_factor * 100).toFixed(1)}%
                  </div>
                )}
              </div>
            </div>
          )}

          {prediction.coaching_impact && prediction.coaching_impact.key_insight && (
            <div className="mb-4 p-3 bg-mint-100 rounded-lg border-2 border-mint-400 shadow-md">
              <div className="flex items-center mb-2">
                <span className="text-sm font-semibold text-mint-600">📊 Coaching Matchup</span>
              </div>
              
              {/* Coach names and win/loss records */}
              {prediction.coaching_impact.historical_record && (
                <div className="mb-3 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-sky-600 font-semibold">
                      {prediction.coaching_impact.home_coach}
                      {prediction.coaching_impact.home_team && (
                        <span className="text-sky-500 font-normal ml-1">
                          ({prediction.coaching_impact.home_team})
                        </span>
                      )}
                    </span>
                    <span className="text-mint-600 font-bold">
                      {prediction.coaching_impact.historical_record.home_coach_record || 
                       `${prediction.coaching_impact.historical_record.home_coach_wins}-${prediction.coaching_impact.historical_record.away_coach_wins}`}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-coral-600 font-semibold">
                      {prediction.coaching_impact.away_coach}
                      {prediction.coaching_impact.away_team && (
                        <span className="text-coral-500 font-normal ml-1">
                          ({prediction.coaching_impact.away_team})
                        </span>
                      )}
                    </span>
                    <span className="text-rose-600 font-bold">
                      {prediction.coaching_impact.historical_record.away_coach_record || 
                       `${prediction.coaching_impact.historical_record.away_coach_wins}-${prediction.coaching_impact.historical_record.home_coach_wins}`}
                    </span>
                  </div>
                  {prediction.coaching_impact.historical_record.num_games > 0 && (
                    <div className="text-xs text-sky-600 pt-1 border-t-2 border-sky-300 font-medium">
                      {prediction.coaching_impact.historical_record.num_games} total meetings
                      {prediction.coaching_impact.historical_record.current_streak?.description && (
                        <span className="ml-2 text-mint-600 font-semibold">
                          • {prediction.coaching_impact.historical_record.current_streak.description}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              )}
              
              <div className="text-xs text-sky-700 font-medium">
                {prediction.coaching_impact.key_insight}
              </div>
              {prediction.coaching_impact.adjustment_factor !== undefined && prediction.coaching_impact.adjustment_factor !== 0 && (
                <div className="text-xs text-coral-600 mt-1 font-semibold">
                  Adjustment: {prediction.coaching_impact.adjustment_factor > 0 ? '+' : ''}
                  {(prediction.coaching_impact.adjustment_factor * 100).toFixed(1)}% win probability
                </div>
              )}
            </div>
          )}

          {prediction.injury_impact && (
            <div className="mb-4 p-3 bg-rose-100 rounded-lg border-2 border-rose-400 shadow-md">
              <div className="flex items-center mb-2">
                <span className="text-sm font-semibold text-rose-600">⚠️ Injury Impact</span>
              </div>
              <div className="space-y-2 text-xs">
                {prediction.injury_impact.home_key_injuries && prediction.injury_impact.home_key_injuries.length > 0 && (
                  <div>
                    <span className="text-sky-600 font-semibold">Home Team:</span>
                    <ul className="list-disc list-inside ml-2 text-sky-700 font-medium">
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
                    <span className="text-mint-600 font-semibold">Away Team:</span>
                    <ul className="list-disc list-inside ml-2 text-mint-700 font-medium">
                      {prediction.injury_impact.away_key_injuries.map((inj: any, idx: number) => (
                        <li key={idx}>
                          {inj.player} ({inj.position}) - {inj.team} - {inj.status.toUpperCase()}: {inj.injury.replace('_', ' ')}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className="text-coral-600 mt-2 font-semibold">
                  Impact: {((prediction.injury_impact.home_injury_impact + prediction.injury_impact.away_injury_impact) / 2 * 100).toFixed(1)}% team performance reduction
                </div>
              </div>
            </div>
          )}

          {prediction.key_factors && prediction.key_factors.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-semibold text-sunny-600 mb-2">Key Factors:</p>
              <ul className="list-disc list-inside text-xs text-sky-700 space-y-1 font-medium">
                {prediction.key_factors.map((factor, idx) => (
                  <li key={idx}>{factor}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <button
        onClick={fetchPrediction}
        disabled={loading}
        className="w-full mt-4 bg-gradient-to-r from-sky-500 to-mint-500 hover:from-sky-600 hover:to-mint-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transform hover:scale-[1.02] active:scale-[0.98] shadow-xl shadow-sky-400/50"
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

