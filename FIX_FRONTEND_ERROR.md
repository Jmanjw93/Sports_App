# 🔧 Fix: "Backend server is not responding" Error

## ❌ The Problem

Your frontend is trying to connect to `localhost:8001` instead of your Render backend.

This happens because `NEXT_PUBLIC_API_URL` is not set in Vercel, or the frontend wasn't redeployed after setting it.

---

## ✅ The Solution

### Step 1: Set Environment Variable in Vercel

1. **Go to:** https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/settings/environment-variables

2. **Find or Add:** `NEXT_PUBLIC_API_URL`

3. **Set Value to:**
   ```
   https://sports-app-ncya.onrender.com
   ```
   ⚠️ **Important:** 
   - No trailing slash!
   - No quotes!
   - Just the URL exactly as shown above

4. **Make sure these are checked:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development

5. **Click "Save"**

---

### Step 2: Redeploy Frontend (CRITICAL!)

**This is the most important step!** The environment variable won't work until you redeploy.

1. **Go to:** https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/deployments

2. **Find your latest deployment**

3. **Click the three dots (⋯) on the right**

4. **Click "Redeploy"**

5. **Wait 2-3 minutes** for the deployment to complete

6. **Visit your frontend URL again**

---

## 🧪 Verify It's Fixed

### After Redeploying:

1. **Visit your frontend:** `https://sports-7t1fit3av-jmanjw93s-projects.vercel.app`

2. **Open browser console:** Press **F12**

3. **Go to "Network" tab**

4. **Try to load games or make a prediction**

5. **Check the Network tab:**
   - ✅ Should see requests to: `https://sports-app-ncya.onrender.com`
   - ❌ Should NOT see requests to: `localhost:8001`

6. **Check Console tab:**
   - ✅ No errors about backend connection
   - ❌ No CORS errors

---

## 🔍 How to Check if Environment Variable is Set

### In Vercel Dashboard:

1. Go to: Settings → Environment Variables
2. Look for `NEXT_PUBLIC_API_URL`
3. Should show: `https://sports-app-ncya.onrender.com`

### In Browser (After Redeploy):

1. Open browser console (F12)
2. Type: `console.log(process.env.NEXT_PUBLIC_API_URL)`
3. Should show: `https://sports-app-ncya.onrender.com`
4. If it shows `undefined` or `http://localhost:8001`, the variable isn't set or frontend wasn't redeployed

---

## ⚠️ Common Mistakes

### ❌ Wrong:
- `https://sports-app-ncya.onrender.com/` (trailing slash)
- `"https://sports-app-ncya.onrender.com"` (quotes)
- `http://sports-app-ncya.onrender.com` (http instead of https)
- Forgot to redeploy after setting

### ✅ Correct:
- `https://sports-app-ncya.onrender.com` (exactly like this)

---

## 🆘 Still Not Working?

### Check 1: Environment Variable
- Go to Vercel → Settings → Environment Variables
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Make sure it's enabled for Production

### Check 2: Deployment
- Go to Vercel → Deployments
- Make sure latest deployment is "Ready" (not "Building" or "Error")
- If it's an old deployment, redeploy

### Check 3: Browser Cache
- Hard refresh: **Ctrl+F5** (Windows) or **Cmd+Shift+R** (Mac)
- Or clear browser cache

### Check 4: Check Logs
- Vercel Dashboard → Deployments → Click deployment → "Logs"
- Look for any build errors

---

## 📝 Quick Checklist

- [ ] Set `NEXT_PUBLIC_API_URL` in Vercel = `https://sports-app-ncya.onrender.com`
- [ ] Enabled for Production, Preview, Development
- [ ] Clicked "Save"
- [ ] Redeployed frontend in Vercel
- [ ] Waited for deployment to complete
- [ ] Tested frontend - error should be gone

---

**The key is: Set the variable AND redeploy! Without redeploying, the old code with localhost will still be running.**

