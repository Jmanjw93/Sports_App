'use client'

export default function SkeletonLoader() {
  return (
    <div className="animate-pulse">
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
        <div className="h-6 bg-slate-700 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-slate-700 rounded w-1/2 mb-2"></div>
        <div className="h-4 bg-slate-700 rounded w-2/3 mb-4"></div>
        <div className="h-20 bg-slate-700 rounded mb-4"></div>
        <div className="h-4 bg-slate-700 rounded w-1/3"></div>
      </div>
    </div>
  )
}

export function GameCardSkeleton() {
  return (
    <div className="animate-pulse bg-white rounded-lg p-6 border-4 border-sky-200">
      <div className="flex items-center justify-between mb-4">
        <div className="h-5 bg-sky-200 rounded w-32"></div>
        <div className="h-4 bg-mint-200 rounded w-20"></div>
      </div>
      <div className="h-6 bg-sky-300 rounded w-40 mb-2"></div>
      <div className="h-6 bg-mint-300 rounded w-40 mb-4"></div>
      <div className="space-y-2 mb-4">
        <div className="h-3 bg-coral-200 rounded w-full"></div>
        <div className="h-3 bg-rose-200 rounded w-3/4"></div>
      </div>
      <div className="h-10 bg-gradient-to-r from-sky-300 to-mint-300 rounded"></div>
    </div>
  )
}

