'use client'

import InteractiveBall from './InteractiveBall'

export default function BackgroundDesign() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 pulse-background">
      {/* WEHUF Background Text - Bottom Right with Loading Bar */}
      <div className="absolute bottom-8 right-8">
        <div className="relative">
          {/* Loading Bar Container - Horizontal */}
          <div className="absolute inset-0 overflow-hidden" style={{ 
            width: 'clamp(20rem, 60vw, 50rem)',
            height: 'clamp(4rem, 15vw, 12rem)',
            transform: 'rotate(-15deg)',
            transformOrigin: 'center'
          }}>
            {/* Top Loading Bar */}
            <div 
              className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-warm-400/80 to-transparent loading-bar-horizontal"
              style={{
                animationDelay: '0s',
                boxShadow: '0 0 15px rgba(242, 109, 29, 0.6)'
              }}
            />
            {/* Middle Loading Bar */}
            <div 
              className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-amber-400/80 to-transparent loading-bar-horizontal"
              style={{
                animationDelay: '1s',
                transform: 'translateY(-50%)',
                boxShadow: '0 0 15px rgba(245, 158, 11, 0.6)'
              }}
            />
            {/* Bottom Loading Bar */}
            <div 
              className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-cozy-400/80 to-transparent loading-bar-horizontal"
              style={{
                animationDelay: '2s',
                boxShadow: '0 0 15px rgba(242, 109, 29, 0.6)'
              }}
            />
          </div>

          {/* Vertical Loading Bars */}
          <div className="absolute inset-0 overflow-hidden" style={{ 
            width: 'clamp(20rem, 60vw, 50rem)',
            height: 'clamp(4rem, 15vw, 12rem)',
            transform: 'rotate(-15deg)',
            transformOrigin: 'center'
          }}>
            {/* Left Loading Bar */}
            <div 
              className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-transparent via-amber-400/70 to-transparent loading-bar-vertical"
              style={{
                animationDelay: '0.5s',
                boxShadow: '0 0 15px rgba(245, 158, 11, 0.6)'
              }}
            />
            {/* Right Loading Bar */}
            <div 
              className="absolute right-0 top-0 bottom-0 w-1 bg-gradient-to-b from-transparent via-terracotta-400/70 to-transparent loading-bar-vertical"
              style={{
                animationDelay: '1.5s',
                boxShadow: '0 0 15px rgba(239, 68, 68, 0.6)'
              }}
            />
          </div>

          {/* WEHUF Text with Glow */}
          <div 
            className="font-black text-warm-300/30 select-none wehuf-glow relative z-10"
            style={{ 
              fontFamily: 'var(--font-comfortaa), system-ui, sans-serif',
              letterSpacing: '0.05em',
              transform: 'rotate(-15deg)',
              fontSize: 'clamp(4rem, 15vw, 12rem)',
              lineHeight: '1',
              color: '#f97316',
              position: 'relative',
              textShadow: '0 0 30px rgba(249, 115, 22, 0.2)'
            }}
          >
            WEHUF
            {/* Animated overlay effect on text */}
            <div 
              className="absolute inset-0 bg-gradient-to-r from-transparent via-amber-300/40 to-transparent loading-bar-horizontal"
              style={{
                mixBlendMode: 'overlay',
                animationDelay: '0.3s',
                pointerEvents: 'none'
              }}
            />
          </div>
        </div>
      </div>

      {/* Chain Logo with NBA and NFL Teams */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 opacity-10 w-full max-w-4xl" style={{ maxHeight: '600px', height: '100%' }}>
        <svg width="800" height="600" viewBox="0 0 800 600" className="w-full h-full" preserveAspectRatio="xMidYMid meet">
          {/* Chain Links - More detailed design */}
          <g stroke="currentColor" strokeWidth="4" fill="none" className="text-warm-300/30">
            {/* Top Row - NFL Links */}
            <g>
              <ellipse cx="150" cy="150" rx="70" ry="35" />
              <ellipse cx="150" cy="150" rx="50" ry="25" />
              <ellipse cx="400" cy="150" rx="70" ry="35" />
              <ellipse cx="400" cy="150" rx="50" ry="25" />
              <ellipse cx="650" cy="150" rx="70" ry="35" />
              <ellipse cx="650" cy="150" rx="50" ry="25" />
            </g>
            
            {/* Middle Row - NBA Links */}
            <g>
              <ellipse cx="275" cy="300" rx="70" ry="35" />
              <ellipse cx="275" cy="300" rx="50" ry="25" />
              <ellipse cx="525" cy="300" rx="70" ry="35" />
              <ellipse cx="525" cy="300" rx="50" ry="25" />
            </g>
            
            {/* Bottom Row - NFL Links */}
            <g>
              <ellipse cx="150" cy="450" rx="70" ry="35" />
              <ellipse cx="150" cy="450" rx="50" ry="25" />
              <ellipse cx="400" cy="450" rx="70" ry="35" />
              <ellipse cx="400" cy="450" rx="50" ry="25" />
              <ellipse cx="650" cy="450" rx="70" ry="35" />
              <ellipse cx="650" cy="450" rx="50" ry="25" />
            </g>
            
            {/* Vertical Connecting Links */}
            <path d="M 150 185 L 205 265" strokeWidth="3" />
            <path d="M 400 185 L 345 265" strokeWidth="3" />
            <path d="M 400 185 L 455 265" strokeWidth="3" />
            <path d="M 650 185 L 595 265" strokeWidth="3" />
            
            <path d="M 275 335 L 205 415" strokeWidth="3" />
            <path d="M 275 335 L 345 415" strokeWidth="3" />
            <path d="M 525 335 L 455 415" strokeWidth="3" />
            <path d="M 525 335 L 595 415" strokeWidth="3" />
            
            {/* Horizontal Connecting Links */}
            <path d="M 220 150 L 330 150" strokeWidth="3" />
            <path d="M 470 150 L 580 150" strokeWidth="3" />
            <path d="M 345 300 L 455 300" strokeWidth="3" />
            <path d="M 220 450 L 330 450" strokeWidth="3" />
            <path d="M 470 450 L 580 450" strokeWidth="3" />
          </g>
          
          {/* NFL Labels in Chain Links */}
          <g className="text-warm-400/60 text-sm font-black">
            <text x="150" y="155" textAnchor="middle" className="fill-current" fontSize="16">NFL</text>
            <text x="400" y="155" textAnchor="middle" className="fill-current" fontSize="16">NFL</text>
            <text x="650" y="155" textAnchor="middle" className="fill-current" fontSize="16">NFL</text>
            <text x="150" y="455" textAnchor="middle" className="fill-current" fontSize="16">NFL</text>
            <text x="400" y="455" textAnchor="middle" className="fill-current" fontSize="16">NFL</text>
            <text x="650" y="455" textAnchor="middle" className="fill-current" fontSize="16">NFL</text>
          </g>
          
          {/* NBA Labels in Chain Links */}
          <g className="text-amber-400/60 text-sm font-black">
            <text x="275" y="305" textAnchor="middle" className="fill-current" fontSize="16">NBA</text>
            <text x="525" y="305" textAnchor="middle" className="fill-current" fontSize="16">NBA</text>
          </g>
        </svg>
      </div>

      {/* Additional decorative elements - Bright happy with pulse */}
      <div className="absolute top-20 left-20 w-32 h-32 border-4 border-amber-300/40 rounded-full hidden md:block pulse-glow"></div>
      <div className="absolute bottom-20 right-20 w-40 h-40 border-4 border-warm-300/40 rounded-full hidden md:block pulse-glow" style={{ animationDelay: '1s' }}></div>
      <div className="absolute top-1/4 right-1/4 w-24 h-24 border-4 border-cozy-300/40 rounded-full hidden lg:block pulse-glow" style={{ animationDelay: '2s' }}></div>
      
      {/* Nature pattern overlay */}
      <div className="absolute inset-0 opacity-5 pointer-events-none">
        <svg width="100%" height="100%" className="absolute inset-0">
          <pattern id="wood-grain" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
            <path d="M0,50 Q25,30 50,50 T100,50" stroke="#8b5a3c" strokeWidth="1" fill="none" opacity="0.3"/>
            <path d="M0,70 Q25,50 50,70 T100,70" stroke="#6b4423" strokeWidth="1" fill="none" opacity="0.2"/>
          </pattern>
          <rect width="100%" height="100%" fill="url(#wood-grain)"/>
        </svg>
      </div>
      
      {/* Gradient overlay for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-warm-200/20 pointer-events-none"></div>

      {/* Animated Sports Balls - Interactive */}
      <div className="absolute inset-0 overflow-hidden" style={{ pointerEvents: 'none' }}>
        {/* Basketball 1 */}
        <InteractiveBall
          className="ball-throw-1"
          width={80}
          height={80}
          viewBox="0 0 80 80"
          opacity={0.15}
          ballType="Basketball"
        >
          <circle cx="40" cy="40" r="38" fill="none" stroke="currentColor" strokeWidth="2" className="text-cozy-500" />
          <path d="M 40 2 Q 20 20, 40 40 Q 60 20, 40 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
          <path d="M 40 2 Q 20 20, 40 40 Q 60 20, 40 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" transform="rotate(120 40 40)" />
          <path d="M 40 2 Q 20 20, 40 40 Q 60 20, 40 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" transform="rotate(240 40 40)" />
          <line x1="40" y1="2" x2="40" y2="78" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
        </InteractiveBall>

        {/* Football 1 */}
        <InteractiveBall
          className="ball-throw-2"
          width={100}
          height={60}
          viewBox="0 0 100 60"
          opacity={0.12}
          ballType="Football"
        >
          <ellipse cx="50" cy="30" rx="48" ry="28" fill="none" stroke="currentColor" strokeWidth="2" className="text-warm-500" />
          <line x1="50" y1="2" x2="50" y2="58" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 50 2 Q 30 15, 20 30 Q 30 45, 50 58" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 50 2 Q 70 15, 80 30 Q 70 45, 50 58" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <line x1="20" y1="30" x2="80" y2="30" stroke="currentColor" strokeWidth="1" className="text-warm-500" />
        </InteractiveBall>

        {/* Baseball 1 */}
        <InteractiveBall
          className="ball-throw-3"
          width={60}
          height={60}
          viewBox="0 0 60 60"
          opacity={0.15}
          ballType="Baseball"
        >
          <circle cx="30" cy="30" r="28" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <path d="M 30 2 Q 15 15, 2 30 Q 15 45, 30 58 Q 45 45, 58 30 Q 45 15, 30 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
          <line x1="30" y1="2" x2="30" y2="58" stroke="currentColor" strokeWidth="1" className="text-amber-500" />
          <line x1="2" y1="30" x2="58" y2="30" stroke="currentColor" strokeWidth="1" className="text-amber-500" />
        </InteractiveBall>

        {/* Hockey Puck 1 */}
        <InteractiveBall
          className="ball-throw-4"
          width={80}
          height={40}
          viewBox="0 0 80 40"
          opacity={0.12}
          ballType="Hockey Puck"
        >
          <ellipse cx="40" cy="20" rx="38" ry="18" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <ellipse cx="40" cy="20" rx="30" ry="14" fill="none" stroke="currentColor" strokeWidth="1" className="text-amber-500" />
          <line x1="10" y1="20" x2="70" y2="20" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
        </InteractiveBall>

        {/* Basketball 2 */}
        <InteractiveBall
          className="ball-throw-5"
          width={70}
          height={70}
          viewBox="0 0 70 70"
          opacity={0.1}
          ballType="Basketball"
        >
          <circle cx="35" cy="35" r="33" fill="none" stroke="currentColor" strokeWidth="2" className="text-cozy-500" />
          <path d="M 35 2 Q 18 18, 35 35 Q 52 18, 35 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
          <path d="M 35 2 Q 18 18, 35 35 Q 52 18, 35 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" transform="rotate(120 35 35)" />
          <path d="M 35 2 Q 18 18, 35 35 Q 52 18, 35 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" transform="rotate(240 35 35)" />
          <line x1="35" y1="2" x2="35" y2="68" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
        </InteractiveBall>

        {/* Football 2 */}
        <InteractiveBall
          className="ball-throw-6"
          width={90}
          height={55}
          viewBox="0 0 90 55"
          opacity={0.1}
          animationDelay="5s"
          ballType="Football"
        >
          <ellipse cx="45" cy="27.5" rx="43" ry="25" fill="none" stroke="currentColor" strokeWidth="2" className="text-warm-500" />
          <line x1="45" y1="2.5" x2="45" y2="52.5" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 45 2.5 Q 28 13, 18 27.5 Q 28 42, 45 52.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 45 2.5 Q 62 13, 72 27.5 Q 62 42, 45 52.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
        </InteractiveBall>

        {/* Baseball 2 */}
        <InteractiveBall
          className="ball-throw-7"
          width={55}
          height={55}
          viewBox="0 0 55 55"
          opacity={0.12}
          animationDelay="3s"
          ballType="Baseball"
        >
          <circle cx="27.5" cy="27.5" r="26" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <path d="M 27.5 1.5 Q 14 13, 1.5 27.5 Q 14 42, 27.5 53.5 Q 41 42, 53.5 27.5 Q 41 13, 27.5 1.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
        </InteractiveBall>

        {/* Basketball 3 */}
        <InteractiveBall
          className="ball-throw-8"
          width={65}
          height={65}
          viewBox="0 0 65 65"
          opacity={0.12}
          animationDelay="2s"
          ballType="Basketball"
        >
          <circle cx="32.5" cy="32.5" r="31" fill="none" stroke="currentColor" strokeWidth="2" className="text-cozy-500" />
          <path d="M 32.5 1.5 Q 16 16, 32.5 32.5 Q 49 16, 32.5 1.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
          <path d="M 32.5 1.5 Q 16 16, 32.5 32.5 Q 49 16, 32.5 1.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" transform="rotate(120 32.5 32.5)" />
          <line x1="32.5" y1="1.5" x2="32.5" y2="63.5" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
        </InteractiveBall>

        {/* Football 3 */}
        <InteractiveBall
          className="ball-throw-9"
          width={85}
          height={50}
          viewBox="0 0 85 50"
          opacity={0.1}
          animationDelay="4s"
          ballType="Football"
        >
          <ellipse cx="42.5" cy="25" rx="41" ry="23" fill="none" stroke="currentColor" strokeWidth="2" className="text-warm-500" />
          <line x1="42.5" y1="2" x2="42.5" y2="48" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 42.5 2 Q 26 12, 18 25 Q 26 38, 42.5 48" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 42.5 2 Q 59 12, 67 25 Q 59 38, 42.5 48" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
        </InteractiveBall>

        {/* Baseball 3 */}
        <InteractiveBall
          className="ball-throw-10"
          width={50}
          height={50}
          viewBox="0 0 50 50"
          opacity={0.12}
          animationDelay="1s"
          ballType="Baseball"
        >
          <circle cx="25" cy="25" r="23" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <path d="M 25 2 Q 12 12, 2 25 Q 12 38, 25 48 Q 38 38, 48 25 Q 38 12, 25 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
        </InteractiveBall>

        {/* Hockey Puck 2 */}
        <InteractiveBall
          className="ball-throw-1"
          width={75}
          height={38}
          viewBox="0 0 75 38"
          opacity={0.1}
          animationDelay="6s"
          ballType="Hockey Puck"
        >
          <ellipse cx="37.5" cy="19" rx="36" ry="17" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <ellipse cx="37.5" cy="19" rx="28" ry="13" fill="none" stroke="currentColor" strokeWidth="1" className="text-amber-500" />
          <line x1="9" y1="19" x2="66" y2="19" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
        </InteractiveBall>

        {/* Basketball 4 */}
        <InteractiveBall
          className="ball-throw-2"
          width={75}
          height={75}
          viewBox="0 0 75 75"
          opacity={0.1}
          animationDelay="7s"
          ballType="Basketball"
        >
          <circle cx="37.5" cy="37.5" r="35" fill="none" stroke="currentColor" strokeWidth="2" className="text-cozy-500" />
          <path d="M 37.5 2.5 Q 20 20, 37.5 37.5 Q 55 20, 37.5 2.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
          <path d="M 37.5 2.5 Q 20 20, 37.5 37.5 Q 55 20, 37.5 2.5" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" transform="rotate(120 37.5 37.5)" />
          <line x1="37.5" y1="2.5" x2="37.5" y2="72.5" stroke="currentColor" strokeWidth="1.5" className="text-cozy-500" />
        </InteractiveBall>

        {/* Football 4 */}
        <InteractiveBall
          className="ball-throw-3"
          width={95}
          height={58}
          viewBox="0 0 95 58"
          opacity={0.12}
          animationDelay="8s"
          ballType="Football"
        >
          <ellipse cx="47.5" cy="29" rx="45" ry="26" fill="none" stroke="currentColor" strokeWidth="2" className="text-warm-500" />
          <line x1="47.5" y1="3" x2="47.5" y2="55" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 47.5 3 Q 30 14, 20 29 Q 30 44, 47.5 55" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
          <path d="M 47.5 3 Q 65 14, 75 29 Q 65 44, 47.5 55" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-warm-500" />
        </InteractiveBall>

        {/* Baseball 4 */}
        <InteractiveBall
          className="ball-throw-4"
          width={58}
          height={58}
          viewBox="0 0 58 58"
          opacity={0.1}
          animationDelay="9s"
          ballType="Baseball"
        >
          <circle cx="29" cy="29" r="27" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <path d="M 29 2 Q 15 14, 2 29 Q 15 44, 29 56 Q 43 44, 56 29 Q 43 14, 29 2" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
        </InteractiveBall>

        {/* Hockey Puck 3 */}
        <InteractiveBall
          className="ball-throw-5"
          width={70}
          height={35}
          viewBox="0 0 70 35"
          opacity={0.12}
          animationDelay="10s"
          ballType="Hockey Puck"
        >
          <ellipse cx="35" cy="17.5" rx="33" ry="15" fill="none" stroke="currentColor" strokeWidth="2" className="text-amber-500" />
          <ellipse cx="35" cy="17.5" rx="26" ry="12" fill="none" stroke="currentColor" strokeWidth="1" className="text-amber-500" />
          <line x1="9" y1="17.5" x2="61" y2="17.5" stroke="currentColor" strokeWidth="1.5" className="text-amber-500" />
        </InteractiveBall>
      </div>
    </div>
  )
}

