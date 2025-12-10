/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed 'standalone' output mode - Vercel uses default Next.js output
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
  },
}

module.exports = nextConfig
