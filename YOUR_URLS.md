# 🔗 Your Server URLs

## Backend (Render)
**URL:** `https://sports-app-ncya.onrender.com`

**Test Endpoints:**
- Health: `https://sports-app-ncya.onrender.com/health`
- Root: `https://sports-app-ncya.onrender.com/`
- Games: `https://sports-app-ncya.onrender.com/api/games/?sport=nfl`

## Frontend (Vercel)
**URL:** `https://sports-app-taupe.vercel.app` (or check your Vercel dashboard for the exact URL)

---

## ✅ Configuration Checklist

### Render (Backend) - CORS Configuration
1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/environment
2. Set `CORS_ORIGINS` to your Vercel frontend URL:
   ```
   https://sports-app-taupe.vercel.app
   ```
   (Or your actual Vercel URL if different)

### Vercel (Frontend) - API URL Configuration
1. Go to: https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/settings/environment-variables
2. Set `NEXT_PUBLIC_API_URL` to:
   ```
   https://sports-app-ncya.onrender.com
   ```
   (No trailing slash!)

---

## 🧪 Test Your Backend

### Test Health Endpoint:
Visit: https://sports-app-ncya.onrender.com/health

**Expected:** `{"status": "healthy"}`

### Test Root Endpoint:
Visit: https://sports-app-ncya.onrender.com/

**Expected:** API information JSON

---

## 🚀 Next Steps

1. ✅ Backend URL: `https://sports-app-ncya.onrender.com`
2. ⏳ Configure Vercel with this URL (see above)
3. ⏳ Configure Render CORS with your Vercel URL
4. ⏳ Test the connection

---

**Your backend is ready! Now let's connect the frontend! 🎉**




