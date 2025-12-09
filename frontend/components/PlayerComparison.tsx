'use client'

import { useState, useEffect } from 'react'
import { Users, TrendingUp, Target, Award } from 'lucide-react'
import axios from 'axios'

interface PlayerComparisonProps {
  sport?: string
}

interface Player {
  name: string
  team: string
  position: string
  stats: {
    points_per_game?: number
    yards_per_game?: number
    assists_per_game?: number
    rebounds_per_game?: number
    goals_per_game?: number
    [key: string]: any
  }
}

export default function PlayerComparison({ sport = 'nfl' }: PlayerComparisonProps) {
  const [player1, setPlayer1] = useState<Player | null>(null)
  const [player2, setPlayer2] = useState<Player | null>(null)
  const [search1, setSearch1] = useState('')
  const [search2, setSearch2] = useState('')
  const [loading, setLoading] = useState(false)

  const mockPlayers: Player[] = [
    { name: 'Patrick Mahomes', team: 'Kansas City Chiefs', position: 'QB', stats: { yards_per_game: 285, touchdowns: 2.1 } },
    { name: 'Josh Allen', team: 'Buffalo Bills', position: 'QB', stats: { yards_per_game: 275, touchdowns: 2.3 } },
    { name: 'Lamar Jackson', team: 'Baltimore Ravens', position: 'QB', stats: { yards_per_game: 240, touchdowns: 1.8 } },
    { name: 'LeBron James', team: 'Los Angeles Lakers', position: 'SF', stats: { points_per_game: 25.5, assists_per_game: 7.2, rebounds_per_game: 8.1 } },
    { name: 'Stephen Curry', team: 'Golden State Warriors', position: 'PG', stats: { points_per_game: 26.4, assists_per_game: 5.1, rebounds_per_game: 4.5 } },
  ]

  const searchPlayers = (query: string) => {
    if (!query) return []
    return mockPlayers.filter(p => 
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.team.toLowerCase().includes(query.toLowerCase())
    )
  }

  const getStatValue = (player: Player, stat: string): number => {
    return player.stats[stat] || 0
  }

  const getStatLabel = (stat: string): string => {
    const labels: { [key: string]: string } = {
      points_per_game: 'Points/Game',
      yards_per_game: 'Yards/Game',
      assists_per_game: 'Assists/Game',
      rebounds_per_game: 'Rebounds/Game',
      goals_per_game: 'Goals/Game',
      touchdowns: 'Touchdowns/Game'
    }
    return labels[stat] || stat
  }

  const getRelevantStats = (): string[] => {
    if (sport === 'nfl') return ['yards_per_game', 'touchdowns']
    if (sport === 'nba') return ['points_per_game', 'assists_per_game', 'rebounds_per_game']
    if (sport === 'mlb') return ['hits', 'home_runs', 'rbis']
    if (sport === 'nhl') return ['goals_per_game', 'assists_per_game']
    return ['points_per_game']
  }

  const relevantStats = getRelevantStats()

  return (
    <div className="bg-latte-50 rounded-lg p-6 border-4 border-amber-300 shadow-xl">
      <div className="flex items-center mb-6">
        <Users className="text-amber-600 mr-3" size={28} />
        <h2 className="text-2xl font-heading font-bold text-gray-900 tracking-tight">Player Comparison</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Player 1 */}
        <div>
          <div className="relative mb-4">
            <input
              type="text"
              placeholder="Search Player 1..."
              value={search1}
              onChange={(e) => setSearch1(e.target.value)}
              className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-warm-400 focus:border-warm-500"
            />
            {search1 && searchPlayers(search1).length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-latte-50 border-2 border-warm-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                {searchPlayers(search1).map((player, idx) => (
                  <div
                    key={idx}
                    onClick={() => {
                      setPlayer1(player)
                      setSearch1('')
                    }}
                    className="p-3 hover:bg-warm-50 cursor-pointer border-b border-warm-100 last:border-b-0"
                  >
                    <div className="font-semibold text-gray-900">{player.name}</div>
                    <div className="text-xs text-gray-800">{player.team} • {player.position}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {player1 && (
            <div className="bg-warm-50 p-4 rounded-lg border-2 border-warm-400">
              <div className="font-bold text-gray-900 text-lg mb-1">{player1.name}</div>
              <div className="text-sm text-gray-900 mb-3">{player1.team} • {player1.position}</div>
              <div className="space-y-2">
                {relevantStats.map(stat => (
                  <div key={stat} className="flex justify-between text-sm">
                    <span className="text-gray-900 font-medium">{getStatLabel(stat)}:</span>
                    <span className="text-gray-900 font-bold">{getStatValue(player1, stat).toFixed(1)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Player 2 */}
        <div>
          <div className="relative mb-4">
            <input
              type="text"
              placeholder="Search Player 2..."
              value={search2}
              onChange={(e) => setSearch2(e.target.value)}
              className="w-full px-4 py-2 border-2 border-cozy-300 rounded-lg focus:ring-2 focus:ring-cozy-400 focus:border-cozy-500"
            />
            {search2 && searchPlayers(search2).length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-latte-50 border-2 border-cozy-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                {searchPlayers(search2).map((player, idx) => (
                  <div
                    key={idx}
                    onClick={() => {
                      setPlayer2(player)
                      setSearch2('')
                    }}
                    className="p-3 hover:bg-cozy-50 cursor-pointer border-b border-cozy-100 last:border-b-0"
                  >
                    <div className="font-semibold text-gray-900">{player.name}</div>
                    <div className="text-xs text-cozy-600">{player.team} • {player.position}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {player2 && (
            <div className="bg-cozy-50 p-4 rounded-lg border-2 border-cozy-400">
              <div className="font-bold text-gray-900 text-lg mb-1">{player2.name}</div>
              <div className="text-sm text-gray-900 mb-3">{player2.team} • {player2.position}</div>
              <div className="space-y-2">
                {relevantStats.map(stat => (
                  <div key={stat} className="flex justify-between text-sm">
                    <span className="text-gray-900 font-medium">{getStatLabel(stat)}:</span>
                    <span className="text-gray-900 font-bold">{getStatValue(player2, stat).toFixed(1)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Comparison Results */}
      {player1 && player2 && (
        <div className="mt-6 p-4 bg-gradient-to-r from-amber-50 to-warm-50 rounded-lg border-2 border-amber-400">
          <h3 className="text-sm font-bold text-gray-900 mb-4 flex items-center">
            <Target className="mr-2" size={16} />
            Head-to-Head Comparison
          </h3>
          <div className="space-y-3">
            {relevantStats.map(stat => {
              const val1 = getStatValue(player1, stat)
              const val2 = getStatValue(player2, stat)
              const diff = val1 - val2
              const winner = diff > 0 ? player1 : player2
              const percentDiff = val2 > 0 ? (Math.abs(diff) / val2) * 100 : 0

              return (
                <div key={stat} className="bg-latte-50/60 p-3 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-gray-900">{getStatLabel(stat)}</span>
                    <span className={`text-xs font-bold ${diff > 0 ? 'text-gray-900' : 'text-gray-900'}`}>
                      {diff > 0 ? player1.name : player2.name} leads by {Math.abs(diff).toFixed(1)} ({percentDiff.toFixed(1)}%)
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-warm-200 rounded-full h-4 relative overflow-hidden">
                      <div
                        className={`h-full ${diff > 0 ? 'bg-warm-500' : 'bg-warm-300'}`}
                        style={{ width: `${val1 > val2 ? 50 + (percentDiff / 2) : 50 - (percentDiff / 2)}%` }}
                      />
                    </div>
                    <div className="flex-1 bg-cozy-200 rounded-full h-4 relative overflow-hidden">
                      <div
                        className={`h-full ${diff < 0 ? 'bg-cozy-500' : 'bg-cozy-300'}`}
                        style={{ width: `${val2 > val1 ? 50 + (percentDiff / 2) : 50 - (percentDiff / 2)}%` }}
                      />
                    </div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-900 mt-1">
                    <span>{val1.toFixed(1)}</span>
                    <span>{val2.toFixed(1)}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

