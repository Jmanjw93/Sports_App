# 🔧 Configuration Values for Your Servers

Based on your URLs, here are the **exact values** you need to set:

---

## 📍 Your Server URLs

### Backend (Render)
- **Service ID**: `srv-d4s9imvdiees73a98brg`
- **URL**: `https://sports-app-ncya.onrender.com` ✅

### Frontend (Vercel)
- **Project**: `sports-app`
- **URL**: `https://sports-app-taupe.vercel.app` (from your GitHub repo)

---

## ⚙️ Step 1: Configure Render (Backend)

1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg
2. Click **"Environment"** tab
3. Find or add `CORS_ORIGINS`
4. Set value to:
   ```
   https://sports-app-taupe.vercel.app
   ```
5. Click **"Save Changes"**
6. Wait ~1 minute for redeploy

---

## ⚙️ Step 2: Configure Vercel (Frontend)

1. Go to: https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW
2. Click **"Settings"** → **"Environment Variables"**
3. Find or add `NEXT_PUBLIC_API_URL`
4. Set value to your Render backend URL:
   ```
   https://sports-app-ncya.onrender.com
   ```
   (**NO trailing slash**)
5. Make sure it's enabled for: ✅ Production, ✅ Preview, ✅ Development
6. Click **"Save"**
7. Go to **"Deployments"** tab
8. Click **"Redeploy"** on the latest deployment

---

## 🔍 How to Find Your Exact URLs

### Render Backend URL:
1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg
2. Look at the top of the page - you'll see your **Public URL**
3. It should look like: `https://sports-app-xxxxx.onrender.com`

### Vercel Frontend URL:
1. Go to: https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW
2. Look at the top - you'll see your **Production URL**
3. It should be: `https://sports-app-taupe.vercel.app` (from your GitHub)

---

## ✅ Quick Checklist

- [ ] Got Render backend URL
- [ ] Set `CORS_ORIGINS` in Render = your Vercel URL
- [ ] Set `NEXT_PUBLIC_API_URL` in Vercel = your Render URL
- [ ] Redeployed frontend in Vercel
- [ ] Tested the app

---

## 🧪 Test Commands

### Test Backend:
Visit: `https://your-backend-url.onrender.com/health`
Should return: `{"status": "healthy"}`

### Test Frontend:
Visit: `https://sports-app-taupe.vercel.app`
Should load your app

### Test Connection:
1. Open browser console (F12)
2. Go to "Network" tab
3. Make a prediction in the app
4. Check if API calls go to your Render backend

---

## 🆘 If It Still Doesn't Work

1. **Check Render Logs**: Render Dashboard → Your Service → "Logs"
2. **Check Vercel Logs**: Vercel Dashboard → Your Project → "Deployments" → Click deployment → "Logs"
3. **Browser Console**: Press F12 → Check "Console" and "Network" tabs for errors

---

**After setting these values, your app should be fully connected! 🎉**

