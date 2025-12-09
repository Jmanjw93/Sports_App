'use client'

interface ConfidenceBarProps {
  value: number // 0-1
  label?: string
  showValue?: boolean
  size?: 'sm' | 'md' | 'lg'
}

export default function ConfidenceBar({ 
  value, 
  label, 
  showValue = true,
  size = 'md'
}: ConfidenceBarProps) {
  const percentage = Math.round(value * 100)
  const height = size === 'sm' ? 'h-2' : size === 'lg' ? 'h-4' : 'h-3'
  
  // Color based on confidence level - bright happy colors
  const getColor = () => {
    if (percentage >= 70) return 'bg-mint-500'
    if (percentage >= 50) return 'bg-sky-500'
    if (percentage >= 30) return 'bg-coral-500'
    return 'bg-rose-500'
  }
  
  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-sky-700 font-semibold">{label}</span>
          {showValue && (
            <span className="text-xs font-bold text-sky-600">{percentage}%</span>
          )}
        </div>
      )}
      <div className={`w-full bg-sky-200 rounded-full ${height} overflow-hidden shadow-inner`}>
        <div
          className={`${getColor()} ${height} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

