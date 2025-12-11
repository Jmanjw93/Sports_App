# ⚡ Quick Setup: Connect Frontend & Backend

## 🎯 2-Minute Setup

### 1. Get Your URLs

**Backend (Render):**
- Go to: https://dashboard.render.com
- Click your service → Copy the URL
- Example: `https://sports-app-ncya.onrender.com`

**Frontend (Vercel):**
- Go to: https://vercel.com/dashboard
- Click your project → Copy the URL
- Example: `https://sports-app-taupe.vercel.app`

---

### 2. Configure Render (Backend)

1. Render Dashboard → Your Service → **"Environment"** tab
2. Find `CORS_ORIGINS`
3. Set value to your **Vercel URL**:
   ```
   https://sports-app-taupe.vercel.app
   ```
4. Click **"Save Changes"**
5. Wait ~1 minute for redeploy

---

### 3. Configure Vercel (Frontend)

1. Vercel Dashboard → Your Project → **"Settings"** → **"Environment Variables"**
2. Find `NEXT_PUBLIC_API_URL`
3. Set value to your **Render URL** (no trailing slash):
   ```
   https://sports-app-ncya.onrender.com
   ```
4. Click **"Save"**
5. Go to **"Deployments"** → Click **"Redeploy"** on latest deployment

---

### 4. Test

1. Visit your Vercel URL
2. Try making a prediction
3. Check browser console (F12) for errors

---

## ✅ Done!

Your app should now be connected. If you see errors, check `SETUP_PUBLIC_SERVERS.md` for troubleshooting.




