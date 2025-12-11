/**
 * Utility functions for storing and retrieving locked predictions
 */

export interface LockedPrediction {
  game_id: string
  sport: string
  home_team: string
  away_team: string
  game_date: string
  predicted_winner: string
  home_win_probability: number
  away_win_probability: number
  confidence: number
  weather_impact: any
  key_factors: string[]
  locked_at: string
  actual_winner?: string
  actual_home_score?: number
  actual_away_score?: number
  is_correct?: boolean
  analyzed?: boolean
}

const STORAGE_KEY = 'locked_predictions'

export const saveLockedPrediction = (prediction: LockedPrediction): void => {
  try {
    const existing = getLockedPredictions()
    // Check if prediction already exists for this game
    const index = existing.findIndex(p => p.game_id === prediction.game_id)
    
    if (index >= 0) {
      // Update existing prediction
      existing[index] = { ...prediction, locked_at: existing[index].locked_at }
    } else {
      // Add new prediction
      existing.push(prediction)
    }
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(existing))
  } catch (error) {
    console.error('Error saving locked prediction:', error)
  }
}

export const getLockedPredictions = (): LockedPrediction[] => {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    return data ? JSON.parse(data) : []
  } catch (error) {
    console.error('Error retrieving locked predictions:', error)
    return []
  }
}

export const getLockedPrediction = (game_id: string): LockedPrediction | null => {
  const predictions = getLockedPredictions()
  return predictions.find(p => p.game_id === game_id) || null
}

export const isPredictionLocked = (game_id: string): boolean => {
  const predictions = getLockedPredictions()
  return predictions.some(p => p.game_id === game_id)
}

export const removeLockedPrediction = (game_id: string): void => {
  try {
    const existing = getLockedPredictions()
    const filtered = existing.filter(p => p.game_id !== game_id)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered))
  } catch (error) {
    console.error('Error removing locked prediction:', error)
  }
}

export const updatePredictionResult = (
  game_id: string,
  actual_winner: string,
  actual_home_score?: number,
  actual_away_score?: number
): void => {
  try {
    const predictions = getLockedPredictions()
    const index = predictions.findIndex(p => p.game_id === game_id)
    
    if (index >= 0) {
      const prediction = predictions[index]
      const is_correct = prediction.predicted_winner === actual_winner
      
      predictions[index] = {
        ...prediction,
        actual_winner,
        actual_home_score,
        actual_away_score,
        is_correct,
        analyzed: true
      }
      
      localStorage.setItem(STORAGE_KEY, JSON.stringify(predictions))
    }
  } catch (error) {
    console.error('Error updating prediction result:', error)
  }
}

export const getPredictionAccuracy = (): {
  total: number
  correct: number
  incorrect: number
  accuracy: number
} => {
  const predictions = getLockedPredictions()
  const analyzed = predictions.filter(p => p.analyzed)
  const correct = analyzed.filter(p => p.is_correct).length
  
  return {
    total: analyzed.length,
    correct,
    incorrect: analyzed.length - correct,
    accuracy: analyzed.length > 0 ? (correct / analyzed.length) * 100 : 0
  }
}

export const getPredictionsBySport = (sport: string): LockedPrediction[] => {
  return getLockedPredictions().filter(p => p.sport === sport)
}

