'use client'

import { useState } from 'react'

interface InteractiveBallProps {
  className: string
  width: number
  height: number
  viewBox: string
  opacity: number
  animationDelay?: string
  children: React.ReactNode
  ballType: string
}

export default function InteractiveBall({
  className,
  width,
  height,
  viewBox,
  opacity,
  animationDelay,
  children,
  ballType
}: InteractiveBallProps) {
  const [clicked, setClicked] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const handleClick = () => {
    setClicked(true)
    setTimeout(() => setClicked(false), 600)
  }

  return (
    <svg
      className={`absolute ${className} interactive-ball ${clicked ? 'ball-clicked' : ''}`}
      width={width}
      height={height}
      viewBox={viewBox}
      style={{
        opacity: isHovered ? 0.4 : opacity,
        animationDelay: animationDelay || '0s',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        transform: isHovered ? 'scale(1.3)' : 'scale(1)',
        filter: isHovered ? 'brightness(1.5)' : 'brightness(1)',
        zIndex: isHovered ? 1 : 0
      }}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <title>{`${ballType} - Click to interact!`}</title>
      {children}
    </svg>
  )
}

