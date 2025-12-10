'use client'

import { useState, useEffect, useMemo } from 'react'
import axios from 'axios'
import GameCard from './GameCard'
import { Loader2, Search, Filter } from 'lucide-react'
import { GameCardSkeleton } from './SkeletonLoader'

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

interface GameListProps {
  sport: string
}

export default function GameList({ sport }: GameListProps) {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<'date' | 'confidence'>('date')

  useEffect(() => {
    fetchGames()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sport])

  const fetchGames = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/games/`, {
        params: { sport, days_ahead: 7 },
        timeout: 60000 // 60 second timeout (for Render free tier wake-up)
      })
      setGames(response.data || [])
    } catch (err: any) {
      const errorMessage = err.code === 'ECONNABORTED' 
        ? `Backend server is not responding. API URL: ${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}. Please check your backend configuration.`
        : err.response?.data?.detail || err.message || 'Failed to fetch games'
      setError(errorMessage)
      console.error('Error fetching games:', err)
      setGames([]) // Set empty array on error
    } finally {
      setLoading(false)
    }
  }

  // Filter and sort games
  const filteredAndSortedGames = useMemo(() => {
    let filtered = games
    
    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(game => 
        game.home_team.toLowerCase().includes(query) ||
        game.away_team.toLowerCase().includes(query) ||
        game.location.city.toLowerCase().includes(query)
      )
    }
    
    // Sort games
    if (sortBy === 'date') {
      filtered = [...filtered].sort((a, b) => 
        new Date(a.date).getTime() - new Date(b.date).getTime()
      )
    }
    
    return filtered
  }, [games, searchQuery, sortBy])

  if (loading) {
    return (
      <div>
        <h2 className="text-3xl font-bold text-gray-900 mb-6 drop-shadow-lg">Upcoming Games</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <GameCardSkeleton key={i} />
          ))}
        </div>
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

  // Group games by week from filtered games
  const gamesByWeek = filteredAndSortedGames.reduce((acc, game) => {
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
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <h2 className="text-3xl font-heading font-bold text-gray-900 tracking-tight drop-shadow-lg">Upcoming Games</h2>
        
        {/* Search and Filter */}
        <div className="flex gap-3">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-warm-600" size={18} />
            <input
              type="text"
              placeholder="Search teams or city..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-latte-50 border-2 border-warm-300 rounded-lg text-gray-800 placeholder-warm-500 focus:outline-none focus:ring-2 focus:ring-warm-400 focus:ring-offset-2 font-medium shadow-md"
            />
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'date' | 'confidence')}
            className="px-4 py-2 bg-latte-50 border-2 border-amber-300 rounded-lg text-amber-800 focus:outline-none focus:ring-2 focus:ring-amber-400 focus:ring-offset-2 font-semibold shadow-md"
          >
            <option value="date">Sort by Date</option>
            <option value="confidence">Sort by Confidence</option>
          </select>
        </div>
      </div>

      {searchQuery && (
        <div className="mb-4 text-gray-900 text-sm font-semibold drop-shadow-md">
          Found {filteredAndSortedGames.length} game{filteredAndSortedGames.length !== 1 ? 's' : ''} matching "{searchQuery}"
        </div>
      )}

      {sortedWeeks.map((week) => (
        <div key={week} className="mb-8">
          <h3 className="text-2xl font-heading font-semibold text-amber-300 mb-4 border-b-4 border-amber-400 pb-2 tracking-tight drop-shadow-md">
            {week}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {gamesByWeek[week].map((game) => (
              <GameCard key={game.game_id} game={game} />
            ))}
          </div>
        </div>
      ))}
      {games.length === 0 && (
        <div className="text-center py-12 text-gray-900 font-semibold drop-shadow-md">
          <p>No upcoming games found</p>
        </div>
      )}
    </div>
  )
}

