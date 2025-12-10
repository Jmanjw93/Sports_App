# 🚀 Setup Guide: Connect Frontend & Backend Public Servers

This guide will help you connect your Vercel frontend to your Render backend.

---

## 📋 Prerequisites

- ✅ Backend deployed on Render
- ✅ Frontend deployed on Vercel
- ✅ Both services are "Live" and accessible

---

## Step 1: Get Your URLs

### Backend URL (Render)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your service: `Sports_App`
3. Copy your **Public URL** (e.g., `https://sports-app-ncya.onrender.com`)

### Frontend URL (Vercel)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click on your project: `sports-app`
3. Copy your **Production URL** (e.g., `https://sports-app-taupe.vercel.app`)

---

## Step 2: Configure Backend CORS (Render)

1. **Go to Render Dashboard** → Your Service → **"Environment"** tab
2. **Find or Add** `CORS_ORIGINS` environment variable
3. **Set the value** to your Vercel URL:
   ```
   https://sports-app-taupe.vercel.app
   ```
   (Replace with your actual Vercel URL)

4. **If you want to allow multiple origins**, separate them with commas:
   ```
   https://sports-app-taupe.vercel.app,https://www.yourdomain.com,https://yourdomain.com
   ```

5. **Click "Save Changes"**
6. **Wait for redeploy** (~1 minute) - Render will automatically redeploy

---

## Step 3: Configure Frontend API URL (Vercel)

1. **Go to Vercel Dashboard** → Your Project → **"Settings"** → **"Environment Variables"**
2. **Find or Add** `NEXT_PUBLIC_API_URL` environment variable
3. **Set the value** to your Render backend URL:
   ```
   https://sports-app-ncya.onrender.com
   ```
   (Replace with your actual Render URL - **NO trailing slash**)

4. **Make sure it's enabled for:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development

5. **Click "Save"**
6. **Redeploy** your frontend:
   - Go to "Deployments" tab
   - Click the three dots (⋯) on the latest deployment
   - Click "Redeploy"

---

## Step 4: Test the Connection

### Test Backend
1. Visit: `https://your-backend-url.onrender.com/health`
2. Should see: `{"status": "healthy"}`

### Test Frontend
1. Visit your Vercel URL
2. The app should load
3. Try making a prediction
4. Open browser console (F12) to check for errors

### Test API Connection
1. Open browser console (F12)
2. Go to "Network" tab
3. Make a prediction in the app
4. Look for API requests to your Render backend
5. Check if they return `200 OK` status

---

## Step 5: Troubleshooting

### Issue: CORS Errors
**Error**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solution**:
1. Verify `CORS_ORIGINS` in Render includes your exact Vercel URL
2. Make sure there are no trailing slashes
3. Wait for Render to finish redeploying
4. Clear browser cache and try again

### Issue: Frontend Can't Connect
**Error**: `Network Error` or `Failed to fetch`

**Solution**:
1. Check `NEXT_PUBLIC_API_URL` in Vercel matches your Render URL
2. Test backend directly: `https://your-backend.onrender.com/health`
3. Check Render logs for errors
4. Verify backend is "Live" (not sleeping)

### Issue: Backend Returns 404
**Error**: `404 Not Found` on API calls

**Solution**:
1. Check the API endpoint path is correct
2. Backend endpoints should be: `/api/games`, `/api/predictions`, etc.
3. Make sure you're using the full URL: `https://backend-url.onrender.com/api/...`

### Issue: Backend is Sleeping (Free Tier)
**Symptom**: First request takes 30-60 seconds

**Solution**:
- This is normal for Render free tier
- Backend wakes up automatically on first request
- Consider upgrading to paid tier for always-on service

---

## Step 6: Verify Everything Works

### ✅ Checklist

- [ ] Backend health check works: `https://backend.onrender.com/health`
- [ ] Frontend loads: `https://frontend.vercel.app`
- [ ] Frontend can fetch games from backend
- [ ] Predictions work
- [ ] No CORS errors in browser console
- [ ] No network errors in browser console

---

## Quick Reference

### Backend (Render)
- **URL**: `https://sports-app-ncya.onrender.com`
- **Health Check**: `https://sports-app-ncya.onrender.com/health`
- **CORS Variable**: `CORS_ORIGINS` = your Vercel URL

### Frontend (Vercel)
- **URL**: `https://sports-app-taupe.vercel.app`
- **API Variable**: `NEXT_PUBLIC_API_URL` = your Render URL

---

## Need Help?

1. **Check Render Logs**: Render Dashboard → Your Service → "Logs"
2. **Check Vercel Logs**: Vercel Dashboard → Your Project → "Deployments" → Click deployment → "Logs"
3. **Browser Console**: Press F12 → Check "Console" and "Network" tabs

---

## Next Steps (Optional)

### Add Custom Domain
- **Frontend**: Vercel → Settings → Domains
- **Backend**: Render → Settings → Custom Domains

### Monitor Performance
- Set up error tracking (Sentry, etc.)
- Monitor API response times
- Track deployment status

---

**Your app should now be fully connected and working! 🎉**


