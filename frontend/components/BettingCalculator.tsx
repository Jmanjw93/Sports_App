'use client'

import { useState } from 'react'
import { Calculator, TrendingUp, DollarSign, AlertCircle, Info } from 'lucide-react'

interface BettingCalculatorProps {
  sport?: string
}

export default function BettingCalculator({ sport = 'nfl' }: BettingCalculatorProps) {
  const [bankroll, setBankroll] = useState(1000)
  const [odds, setOdds] = useState(2.0)
  const [winProbability, setWinProbability] = useState(55)
  const [kellyFraction, setKellyFraction] = useState(0.25)

  // Calculate Kelly percentage
  const calculateKelly = (prob: number, odds: number, fraction: number): number => {
    if (odds <= 1.0) return 0
    const b = odds - 1
    const p = prob / 100
    const q = 1 - p
    const kelly = (b * p - q) / b
    const fractionalKelly = Math.max(0, kelly * fraction)
    return Math.min(fractionalKelly * 100, 5) // Cap at 5%
  }

  // Calculate Expected Value
  const calculateEV = (prob: number, odds: number): number => {
    if (odds <= 1.0) return -100
    const p = prob / 100
    const ev = (p * (odds - 1)) - ((1 - p) * 1)
    return ev * 100
  }

  const kellyPercent = calculateKelly(winProbability, odds, kellyFraction)
  const betAmount = (bankroll * kellyPercent) / 100
  const expectedValue = calculateEV(winProbability, odds)
  const impliedProbability = (1 / odds) * 100
  const edge = winProbability - impliedProbability
  const potentialWin = betAmount * (odds - 1)
  const potentialLoss = betAmount

  const getRecommendation = () => {
    if (expectedValue < 0) return { text: 'Avoid This Bet', color: 'text-terracotta-600', bg: 'bg-terracotta-50', border: 'border-terracotta-400' }
    if (expectedValue > 10) return { text: 'Strong Bet', color: 'text-gray-900', bg: 'bg-amber-50', border: 'border-amber-400' }
    if (expectedValue > 5) return { text: 'Good Bet', color: 'text-gray-900', bg: 'bg-warm-50', border: 'border-warm-400' }
    return { text: 'Moderate Bet', color: 'text-gray-900', bg: 'bg-cozy-50', border: 'border-cozy-400' }
  }

  const recommendation = getRecommendation()

  return (
    <div className="bg-latte-50 rounded-lg p-6 border-4 border-warm-300 shadow-xl">
      <div className="flex items-center mb-6">
        <Calculator className="text-warm-600 mr-3" size={28} />
        <h2 className="text-2xl font-heading font-bold text-gray-900 tracking-tight">Betting Calculator</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Input Section */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">
              Bankroll ($)
            </label>
            <input
              type="number"
              value={bankroll}
              onChange={(e) => setBankroll(Number(e.target.value))}
              className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-500 font-medium"
              min="1"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">
              Decimal Odds
            </label>
            <input
              type="number"
              value={odds}
              onChange={(e) => setOdds(Number(e.target.value))}
              className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-500 font-medium"
              min="1.01"
              step="0.01"
            />
            <p className="text-xs text-sky-500 mt-1">
              Implied Probability: {impliedProbability.toFixed(1)}%
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">
              Win Probability (%)
            </label>
            <input
              type="number"
              value={winProbability}
              onChange={(e) => setWinProbability(Number(e.target.value))}
              className="w-full px-4 py-2 border-2 border-warm-300 rounded-lg focus:ring-2 focus:ring-sky-400 focus:border-sky-500 font-medium"
              min="0"
              max="100"
            />
            <p className="text-xs text-sky-500 mt-1">
              Edge: {edge > 0 ? '+' : ''}{edge.toFixed(1)}%
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-2">
              Kelly Fraction: {(kellyFraction * 100).toFixed(0)}%
            </label>
            <input
              type="range"
              value={kellyFraction}
              onChange={(e) => setKellyFraction(Number(e.target.value))}
              className="w-full"
              min="0.1"
              max="1.0"
              step="0.05"
            />
            <div className="flex justify-between text-xs text-sky-500 mt-1">
              <span>Conservative (10%)</span>
              <span>Full Kelly (100%)</span>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-4">
          <div className={`p-4 rounded-lg border-2 ${recommendation.border} ${recommendation.bg}`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-gray-900">Recommendation</span>
              <span className={`font-bold ${recommendation.color}`}>{recommendation.text}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="bg-amber-50 p-3 rounded-lg border-2 border-mint-400">
              <div className="flex items-center text-xs text-gray-900 font-semibold mb-1">
                <DollarSign size={14} className="mr-1" />
                Bet Amount
              </div>
              <div className="text-xl font-bold text-mint-700">${betAmount.toFixed(2)}</div>
              <div className="text-xs text-gray-900 mt-1">
                {kellyPercent.toFixed(2)}% of bankroll
              </div>
            </div>

            <div className="bg-warm-50 p-3 rounded-lg border-2 border-sky-400">
              <div className="flex items-center text-xs text-gray-900 font-semibold mb-1">
                <TrendingUp size={14} className="mr-1" />
                Expected Value
              </div>
              <div className={`text-xl font-bold ${expectedValue >= 0 ? 'text-gray-900' : 'text-terracotta-600'}`}>
                {expectedValue >= 0 ? '+' : ''}{expectedValue.toFixed(2)}%
              </div>
            </div>

            <div className="bg-cozy-50 p-3 rounded-lg border-2 border-cozy-400">
              <div className="text-xs text-gray-900 font-semibold mb-1">Potential Win</div>
              <div className="text-xl font-bold text-gray-900">+${potentialWin.toFixed(2)}</div>
            </div>

            <div className="bg-rose-100 p-3 rounded-lg border-2 border-rose-400">
              <div className="text-xs text-terracotta-600 font-semibold mb-1">Potential Loss</div>
              <div className="text-xl font-bold text-rose-700">-${potentialLoss.toFixed(2)}</div>
            </div>
          </div>

          <div className="bg-amber-50 p-3 rounded-lg border-2 border-amber-400">
            <div className="flex items-start">
              <Info size={16} className="text-sunny-600 mr-2 mt-0.5" />
              <div className="text-xs text-gray-900">
                <strong>Kelly Criterion</strong> calculates optimal bet sizing based on your edge. 
                Using {kellyFraction * 100}% Kelly is more conservative and reduces volatility.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Risk Analysis */}
      <div className="mt-6 p-4 bg-gradient-to-r from-warm-50 to-amber-50 rounded-lg border-2 border-warm-300">
        <h3 className="text-sm font-bold text-gray-900 mb-3">Risk Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div>
            <span className="font-semibold text-gray-900">ROI if Win:</span>
            <span className="text-gray-900 ml-2">
              {((potentialWin / betAmount) * 100).toFixed(1)}%
            </span>
          </div>
          <div>
            <span className="font-semibold text-gray-900">Risk/Reward:</span>
            <span className="text-gray-900 ml-2">
              1:{(potentialWin / potentialLoss).toFixed(2)}
            </span>
          </div>
          <div>
            <span className="font-semibold text-gray-900">Break-Even:</span>
            <span className="text-gray-900 ml-2">
              {impliedProbability.toFixed(1)}% win rate needed
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

