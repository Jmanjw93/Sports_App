'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import PlayerProps from './PlayerProps'
import { Loader2, Calendar, MapPin } from 'lucide-react'

interface Game {
  game_id: string
  sport: string
  home_team: string
  away_team: string
  date: string
  venue: string
  week?: string
  location: {
    city: string
    state: string
    country: string
  }
}

interface PlayerPropsListProps {
  sport: string
}

export default function PlayerPropsList({ sport }: PlayerPropsListProps) {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchGames()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sport])

  const fetchGames = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/games/`, {
        params: { sport, days_ahead: 7 }
      })
      setGames(response.data)
      setError(null)
    } catch (err: any) {
      setError(err.message || 'Failed to fetch games')
      console.error('Error fetching games:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    try {
      let date: Date
      if (dateString.includes('T')) {
        date = new Date(dateString)
      } else {
        date = new Date(dateString + 'T13:00:00')
      }
      
      if (isNaN(date.getTime())) {
        return 'Date TBD'
      }
      
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
      return 'Date TBD'
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="animate-spin text-sky-500" size={48} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-rose-200 border-4 border-rose-500 rounded-lg p-4 text-rose-800 font-semibold">
        <p>Error: {error}</p>
      </div>
    )
  }

  // Group games by week
  const gamesByWeek = games.reduce((acc, game) => {
    const week = game.week || 'Other'
    if (!acc[week]) {
      acc[week] = []
    }
    acc[week].push(game)
    return acc
  }, {} as Record<string, Game[]>)

  // Sort weeks: Today first, then This Week, then Next Week, then others
  const weekOrder = ['Today', 'This Week', 'Next Week']
  const sortedWeeks = Object.keys(gamesByWeek).sort((a, b) => {
    const aIndex = weekOrder.indexOf(a)
    const bIndex = weekOrder.indexOf(b)
    if (aIndex !== -1 && bIndex !== -1) return aIndex - bIndex
    if (aIndex !== -1) return -1
    if (bIndex !== -1) return 1
    return a.localeCompare(b)
  })

  return (
    <div>
      <h2 className="text-3xl font-heading font-bold text-white mb-6 tracking-tight drop-shadow-lg">Player Prop Bets</h2>
      <p className="text-white mb-8 font-semibold drop-shadow-md">Select a game to view player prop recommendations and predictions</p>
      
      {sortedWeeks.map((week) => (
        <div key={week} className="mb-8">
          <h3 className="text-2xl font-heading font-semibold text-sunny-300 mb-4 border-b-4 border-sunny-400 pb-2 tracking-tight drop-shadow-md">
            {week}
          </h3>
          <div className="space-y-6">
            {gamesByWeek[week].map((game) => (
              <div key={game.game_id} className="bg-white rounded-lg p-6 border-4 border-coral-300 hover:border-coral-500 transition-all shadow-xl">
                <div className="mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h3 className="text-xl font-heading font-bold text-sky-600 mb-1 tracking-tight">{game.away_team}</h3>
                      <p className="text-coral-500 text-sm font-sans font-bold">@</p>
                      <h3 className="text-xl font-heading font-bold text-mint-600 tracking-tight">{game.home_team}</h3>
                    </div>
                  </div>
                  
                  <div className="space-y-2 mt-4">
                    <div className="flex items-center text-sky-600 text-sm font-semibold">
                      <Calendar size={16} className="mr-2 text-coral-500" />
                      {formatDate(game.date)}
                    </div>
                    <div className="flex items-center text-mint-600 text-sm font-semibold">
                      <MapPin size={16} className="mr-2 text-rose-500" />
                      {game.location.city}, {game.location.state}
                    </div>
                  </div>
                </div>
                
                <PlayerProps gameId={game.game_id} />
              </div>
            ))}
          </div>
        </div>
      ))}
      
      {games.length === 0 && (
        <div className="text-center py-12 text-white font-semibold drop-shadow-md">
          <p>No upcoming games found</p>
        </div>
      )}
    </div>
  )
}

