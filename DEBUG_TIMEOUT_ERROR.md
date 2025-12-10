# 🔍 Debug: Timeout Error (Backend Not Responding)

## What the Error Means

The error `timeout of 10000ms exceeded` with code `ECONNABORTED` means:
- ✅ Frontend IS trying to connect to backend
- ❌ Backend is NOT responding within 10 seconds

This could mean:
1. Backend is sleeping (free tier - takes 30-60 seconds to wake up)
2. Backend is down/crashed
3. CORS is blocking the request
4. Wrong URL being used

---

## Step 1: Check What URL It's Actually Using

The error message should show the API URL. But let's check the Network tab:

1. **Open Developer Tools (F12)**
2. **Go to "Network" tab** (not Console)
3. **Try to load games** (or refresh the page)
4. **Look for the failed request:**
   - What URL is it trying to connect to?
   - Is it `localhost:8001` or `https://sports-app-ncya.onrender.com`?

---

## Step 2: Test Backend Directly

### Test Backend Health:
Visit in your browser: `https://sports-app-ncya.onrender.com/health`

**What happens?**
- ✅ Returns `{"status": "healthy"}` = Backend is working
- ⏳ Takes 30-60 seconds then works = Backend was sleeping (normal for free tier)
- ❌ Error or timeout = Backend has issues

---

## Step 3: Check Render Status

1. **Go to:** https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg
2. **Check status:**
   - ✅ "Live" = Backend is running
   - ⚠️ "Sleeping" = Free tier, will wake on request (30-60 sec delay)
   - ❌ "Error" = Backend crashed

---

## Step 4: Check Render Logs

1. **Go to:** https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/logs
2. **Look for:**
   - Red error messages
   - Import errors
   - Startup errors
   - Any recent errors

---

## Common Issues & Fixes

### Issue 1: Backend is Sleeping (Free Tier)

**Symptom:** First request takes 30-60 seconds, then works

**Solution:** 
- This is normal for Render free tier
- Wait for backend to wake up
- Or upgrade to paid tier for always-on

**Test:** Visit `https://sports-app-ncya.onrender.com/health` and wait 30-60 seconds

---

### Issue 2: Backend Crashed

**Symptom:** Backend health check fails, Render shows "Error"

**Solution:**
1. Check Render logs for errors
2. Fix the error
3. Redeploy backend

---

### Issue 3: CORS Blocking Request

**Symptom:** Request goes to correct URL but fails with CORS error

**Solution:**
1. Check `CORS_ORIGINS` in Render
2. Should include your Vercel URL: `https://sports-7t1fit3av-jmanjw93s-projects.vercel.app`
3. Save and wait for redeploy

---

### Issue 4: Wrong URL Being Used

**Symptom:** Network tab shows requests to `localhost:8001`

**Solution:**
1. Environment variable not set in Vercel
2. Or frontend wasn't redeployed after setting it
3. Set variable and redeploy

---

## Quick Test Checklist

- [ ] Test backend directly: `https://sports-app-ncya.onrender.com/health`
- [ ] Check Render status (Live/Sleeping/Error)
- [ ] Check Render logs for errors
- [ ] Check Network tab - what URL is it using?
- [ ] Check CORS_ORIGINS in Render includes Vercel URL

---

## What to Tell Me

Please check and tell me:

1. **What happens when you visit:** `https://sports-app-ncya.onrender.com/health`?
   - Does it work?
   - How long does it take?

2. **In Network tab, what URL is the failed request trying to connect to?**

3. **What's the status in Render dashboard?** (Live/Sleeping/Error)

4. **Any errors in Render logs?**

This will help me figure out the exact issue!


