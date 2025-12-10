'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { Users, TrendingUp, Target, Award, GraduationCap, Trophy, Calendar, ChevronDown, ChevronUp } from 'lucide-react'

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

interface PlayerFacts {
  name: string
  sport: string
  college: string
  draft_info: {
    year: number
    round: number
    pick: number
  }
  achievements: string[]
  career_highlights: string[]
  notable_stats: string[]
}

interface MatchupHistory {
  player1_name: string
  player2_name: string
  total_games: number
  professional_games: number
  college_games: number
  player1_wins: number
  player2_wins: number
  player1_record: string
  player2_record: string
  player1_win_rate: number
  player2_win_rate: number
  professional_matchups: any[]
  college_matchups: any[]
  player1_avg_stats: any
  player2_avg_stats: any
  recent_trend: string
}

interface ComparisonData {
  player1: PlayerFacts
  player2: PlayerFacts
  head_to_head: MatchupHistory
  summary: {
    total_matchups: number
    player1_advantage: boolean
    player2_advantage: boolean
    even_matchup: boolean
  }
}

export default function PlayerComparison({ sport = 'nfl' }: PlayerComparisonProps) {
  const [player1, setPlayer1] = useState<Player | null>(null)
  const [player2, setPlayer2] = useState<Player | null>(null)
  const [search1, setSearch1] = useState('')
  const [search2, setSearch2] = useState('')
  const [loading, setLoading] = useState(false)
  const [comparisonData, setComparisonData] = useState<ComparisonData | null>(null)
  const [loadingComparison, setLoadingComparison] = useState(false)
  const [showHistorical, setShowHistorical] = useState(false)

  const mockPlayers: { [key: string]: Player[] } = {
    nfl: [
      { name: 'Patrick Mahomes', team: 'Kansas City Chiefs', position: 'QB', stats: { yards_per_game: 285, touchdowns: 2.1 } },
      { name: 'Josh Allen', team: 'Buffalo Bills', position: 'QB', stats: { yards_per_game: 275, touchdowns: 2.3 } },
      { name: 'Lamar Jackson', team: 'Baltimore Ravens', position: 'QB', stats: { yards_per_game: 240, touchdowns: 1.8 } },
      { name: 'Travis Kelce', team: 'Kansas City Chiefs', position: 'TE', stats: { yards_per_game: 75, touchdowns: 0.8 } },
      { name: 'Tyreek Hill', team: 'Miami Dolphins', position: 'WR', stats: { yards_per_game: 95, touchdowns: 0.9 } },
    ],
    nba: [
      { name: 'LeBron James', team: 'Los Angeles Lakers', position: 'SF', stats: { points_per_game: 25.5, assists_per_game: 7.2, rebounds_per_game: 8.1 } },
      { name: 'Stephen Curry', team: 'Golden State Warriors', position: 'PG', stats: { points_per_game: 26.4, assists_per_game: 5.1, rebounds_per_game: 4.5 } },
      { name: 'Kevin Durant', team: 'Phoenix Suns', position: 'PF', stats: { points_per_game: 28.2, assists_per_game: 5.0, rebounds_per_game: 6.8 } },
      { name: 'Giannis Antetokounmpo', team: 'Milwaukee Bucks', position: 'PF', stats: { points_per_game: 30.4, assists_per_game: 5.7, rebounds_per_game: 11.5 } },
    ],
    mlb: [
      { name: 'Aaron Judge', team: 'New York Yankees', position: 'OF', stats: { hits: 158, home_runs: 62, rbis: 131 } },
      { name: 'Shohei Ohtani', team: 'Los Angeles Angels', position: 'DH/P', stats: { hits: 138, home_runs: 44, rbis: 95 } },
    ],
    nhl: [
      { name: 'Connor McDavid', team: 'Edmonton Oilers', position: 'C', stats: { goals_per_game: 0.68, assists_per_game: 1.54 } },
      { name: 'Nathan MacKinnon', team: 'Colorado Avalanche', position: 'C', stats: { goals_per_game: 0.58, assists_per_game: 1.12 } },
    ]
  }

  const searchPlayers = (query: string) => {
    if (!query) return []
    const players = mockPlayers[sport] || []
    return players.filter(p => 
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.team.toLowerCase().includes(query.toLowerCase())
    )
  }


  const getRelevantStats = (): string[] => {
    if (sport === 'nfl') return ['yards_per_game', 'touchdowns']
    if (sport === 'nba') return ['points_per_game', 'assists_per_game', 'rebounds_per_game']
    if (sport === 'mlb') return ['hits', 'home_runs', 'rbis']
    if (sport === 'nhl') return ['goals_per_game', 'assists_per_game']
    return ['points_per_game']
  }

  const getStatValue = (player: Player, stat: string): number => {
    // Handle different stat naming conventions
    if (stat === 'touchdowns' && player.stats.touchdowns !== undefined) {
      return player.stats.touchdowns
    }
    return player.stats[stat] || 0
  }

  const getStatLabel = (stat: string): string => {
    const labels: { [key: string]: string } = {
      points_per_game: 'Points/Game',
      yards_per_game: 'Yards/Game',
      assists_per_game: 'Assists/Game',
      rebounds_per_game: 'Rebounds/Game',
      goals_per_game: 'Goals/Game',
      touchdowns: 'Touchdowns/Game',
      hits: 'Hits',
      home_runs: 'Home Runs',
      rbis: 'RBIs'
    }
    return labels[stat] || stat.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  const relevantStats = getRelevantStats()

  const fetchComparisonData = async () => {
    if (!player1 || !player2) return

    try {
      setLoadingComparison(true)
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'}/api/player-comparison/compare`,
        {
          params: {
            player1: player1.name,
            player2: player2.name,
            sport: sport,
            include_college: true
          }
        }
      )
      setComparisonData(response.data)
      setShowHistorical(true)
    } catch (err) {
      console.error('Error fetching comparison data:', err)
    } finally {
      setLoadingComparison(false)
    }
  }

  useEffect(() => {
    if (player1 && player2) {
      fetchComparisonData()
    } else {
      setComparisonData(null)
      setShowHistorical(false)
    }
  }, [player1, player2, sport])

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

      {/* Historical Matchups & Facts */}
      {player1 && player2 && comparisonData && (
        <div className="mt-6 space-y-4">
          {/* Head-to-Head Historical Matchups */}
          <div className="p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg border-2 border-purple-400">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900 flex items-center">
                <Target className="mr-2" size={20} />
                Historical Head-to-Head Matchups
              </h3>
              <button
                onClick={() => setShowHistorical(!showHistorical)}
                className="text-sm text-purple-700 hover:text-purple-900 flex items-center gap-1"
              >
                {showHistorical ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                {showHistorical ? 'Hide' : 'Show'} Details
              </button>
            </div>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-white/80 rounded p-3">
                <div className="text-sm text-gray-600">Total Matchups</div>
                <div className="text-2xl font-bold text-gray-900">
                  {comparisonData.head_to_head.total_games}
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {comparisonData.head_to_head.professional_games} Pro • {comparisonData.head_to_head.college_games} College
                </div>
              </div>
              <div className="bg-white/80 rounded p-3">
                <div className="text-sm text-gray-600">Record</div>
                <div className="text-lg font-bold text-gray-900">
                  {player1.name}: {comparisonData.head_to_head.player1_record}
                </div>
                <div className="text-lg font-bold text-gray-900">
                  {player2.name}: {comparisonData.head_to_head.player2_record}
                </div>
              </div>
            </div>

            {showHistorical && (
              <div className="space-y-3">
                {/* Professional Matchups */}
                {comparisonData.head_to_head.professional_matchups.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Professional Matchups</h4>
                    <div className="space-y-2">
                      {comparisonData.head_to_head.professional_matchups.slice(-5).reverse().map((matchup, idx) => (
                        <div key={idx} className="bg-white/60 rounded p-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-700">{matchup.game_date}</span>
                            <span className={`font-bold ${matchup.winner === 'player1' ? 'text-purple-700' : 'text-indigo-700'}`}>
                              {matchup.winner === 'player1' ? player1.name : player2.name} won
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* College Matchups */}
                {comparisonData.head_to_head.college_matchups.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                      <GraduationCap className="mr-1" size={16} />
                      College Matchups
                    </h4>
                    <div className="space-y-2">
                      {comparisonData.head_to_head.college_matchups.map((matchup, idx) => (
                        <div key={idx} className="bg-white/60 rounded p-2 text-sm">
                          <div className="flex justify-between">
                            <div>
                              <span className="text-gray-700">{matchup.game_date}</span>
                              <span className="text-gray-600 ml-2">• {matchup.college}</span>
                            </div>
                            <span className={`font-bold ${matchup.winner === 'player1' ? 'text-purple-700' : 'text-indigo-700'}`}>
                              {matchup.winner === 'player1' ? player1.name : player2.name} won
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Average Stats in Matchups */}
                {Object.keys(comparisonData.head_to_head.player1_avg_stats).length > 0 && (
                  <div className="mt-4 p-3 bg-white/80 rounded">
                    <h4 className="font-semibold text-gray-900 mb-2">Average Stats in Matchups</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-xs text-gray-600 mb-1">{player1.name}</div>
                        {Object.entries(comparisonData.head_to_head.player1_avg_stats).map(([stat, value]) => (
                          <div key={stat} className="text-sm text-gray-900">
                            {stat}: {String(value)}
                          </div>
                        ))}
                      </div>
                      <div>
                        <div className="text-xs text-gray-600 mb-1">{player2.name}</div>
                        {Object.entries(comparisonData.head_to_head.player2_avg_stats).map(([stat, value]) => (
                          <div key={stat} className="text-sm text-gray-900">
                            {stat}: {String(value)}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Player Facts */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Player 1 Facts */}
            <div className="p-4 bg-gradient-to-r from-warm-50 to-amber-50 rounded-lg border-2 border-warm-400">
              <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <Trophy className="mr-2" size={20} />
                {player1.name} - Additional Facts
              </h3>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-semibold text-gray-700">College:</span>
                  <span className="text-gray-900 ml-2">{comparisonData.player1.college}</span>
                </div>
                <div>
                  <span className="font-semibold text-gray-700">Draft:</span>
                  <span className="text-gray-900 ml-2">
                    {comparisonData.player1.draft_info.year} - Round {comparisonData.player1.draft_info.round}, Pick {comparisonData.player1.draft_info.pick}
                  </span>
                </div>
                <div>
                  <span className="font-semibold text-gray-700">Achievements:</span>
                  <ul className="list-disc list-inside text-gray-900 ml-2 mt-1">
                    {comparisonData.player1.achievements.map((ach, idx) => (
                      <li key={idx}>{ach}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <span className="font-semibold text-gray-700">Career Highlights:</span>
                  <ul className="list-disc list-inside text-gray-900 ml-2 mt-1">
                    {comparisonData.player1.career_highlights.map((hl, idx) => (
                      <li key={idx}>{hl}</li>
                    ))}
                  </ul>
                </div>
                {comparisonData.player1.notable_stats.length > 0 && (
                  <div>
                    <span className="font-semibold text-gray-700">Notable Stats:</span>
                    <ul className="list-disc list-inside text-gray-900 ml-2 mt-1">
                      {comparisonData.player1.notable_stats.map((stat, idx) => (
                        <li key={idx}>{stat}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            {/* Player 2 Facts */}
            <div className="p-4 bg-gradient-to-r from-cozy-50 to-amber-50 rounded-lg border-2 border-cozy-400">
              <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <Trophy className="mr-2" size={20} />
                {player2.name} - Additional Facts
              </h3>
              <div className="space-y-2 text-sm">
                <div>
                  <span className="font-semibold text-gray-700">College:</span>
                  <span className="text-gray-900 ml-2">{comparisonData.player2.college}</span>
                </div>
                <div>
                  <span className="font-semibold text-gray-700">Draft:</span>
                  <span className="text-gray-900 ml-2">
                    {comparisonData.player2.draft_info.year} - Round {comparisonData.player2.draft_info.round}, Pick {comparisonData.player2.draft_info.pick}
                  </span>
                </div>
                <div>
                  <span className="font-semibold text-gray-700">Achievements:</span>
                  <ul className="list-disc list-inside text-gray-900 ml-2 mt-1">
                    {comparisonData.player2.achievements.map((ach, idx) => (
                      <li key={idx}>{ach}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <span className="font-semibold text-gray-700">Career Highlights:</span>
                  <ul className="list-disc list-inside text-gray-900 ml-2 mt-1">
                    {comparisonData.player2.career_highlights.map((hl, idx) => (
                      <li key={idx}>{hl}</li>
                    ))}
                  </ul>
                </div>
                {comparisonData.player2.notable_stats.length > 0 && (
                  <div>
                    <span className="font-semibold text-gray-700">Notable Stats:</span>
                    <ul className="list-disc list-inside text-gray-900 ml-2 mt-1">
                      {comparisonData.player2.notable_stats.map((stat, idx) => (
                        <li key={idx}>{stat}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Comparison Results */}
      {player1 && player2 && (
        <div className="mt-6 p-4 bg-gradient-to-r from-amber-50 to-warm-50 rounded-lg border-2 border-amber-400">
          <h3 className="text-sm font-bold text-gray-900 mb-4 flex items-center">
            <Target className="mr-2" size={16} />
            Head-to-Head Comparison
          </h3>
          {loadingComparison && (
            <div className="text-center py-4">
              <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-amber-600"></div>
              <p className="mt-2 text-sm text-gray-700">Loading historical data...</p>
            </div>
          )}
          <div className="space-y-3">
            {relevantStats.map(stat => {
              const val1 = getStatValue(player1, stat)
              const val2 = getStatValue(player2, stat)
              const diff = val1 - val2
              const winner = diff > 0 ? player1 : player2
              const maxVal = Math.max(val1, val2, 1) // Prevent division by zero
              const percentDiff = maxVal > 0 ? (Math.abs(diff) / maxVal) * 100 : 0
              
              // Calculate bar widths as percentages of the max value
              const val1Percent = maxVal > 0 ? (val1 / maxVal) * 100 : 0
              const val2Percent = maxVal > 0 ? (val2 / maxVal) * 100 : 0

              return (
                <div key={stat} className="bg-latte-50/60 p-3 rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-semibold text-gray-900">{getStatLabel(stat)}</span>
                    {diff !== 0 && (
                      <span className="text-xs font-bold text-gray-900">
                        {diff > 0 ? player1.name : player2.name} leads by {Math.abs(diff).toFixed(1)} 
                        {percentDiff > 0 && ` (${percentDiff.toFixed(1)}%)`}
                      </span>
                    )}
                    {diff === 0 && (
                      <span className="text-xs font-bold text-gray-600">Tied</span>
                    )}
                  </div>
                  <div className="flex items-center space-x-2 mb-1">
                    <div className="flex-1 bg-warm-200 rounded-full h-4 relative overflow-hidden">
                      <div
                        className={`h-full ${diff > 0 ? 'bg-warm-500' : diff < 0 ? 'bg-warm-300' : 'bg-warm-400'}`}
                        style={{ width: `${Math.min(val1Percent, 100)}%` }}
                      />
                    </div>
                    <div className="flex-1 bg-cozy-200 rounded-full h-4 relative overflow-hidden">
                      <div
                        className={`h-full ${diff < 0 ? 'bg-cozy-500' : diff > 0 ? 'bg-cozy-300' : 'bg-cozy-400'}`}
                        style={{ width: `${Math.min(val2Percent, 100)}%` }}
                      />
                    </div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-900">
                    <span className="font-semibold">{player1.name}: {val1.toFixed(stat === 'touchdowns' || stat.includes('per_game') ? 1 : 0)}</span>
                    <span className="font-semibold">{player2.name}: {val2.toFixed(stat === 'touchdowns' || stat.includes('per_game') ? 1 : 0)}</span>
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

