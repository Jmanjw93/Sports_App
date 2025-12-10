# 🎯 Final Setup Steps - Connect Everything

## ✅ Your Backend URL
**Backend:** `https://sports-app-ncya.onrender.com`

---

## Step 1: Configure Vercel (Frontend) - 2 minutes

### Set Environment Variable:

1. **Go to:** https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/settings/environment-variables

2. **Find or Add:** `NEXT_PUBLIC_API_URL`

3. **Set Value to:**
   ```
   https://sports-app-ncya.onrender.com
   ```
   ⚠️ **Important:** No trailing slash!

4. **Make sure these are checked:**
   - ✅ Production
   - ✅ Preview  
   - ✅ Development

5. **Click "Save"**

6. **Redeploy Frontend:**
   - Go to "Deployments" tab
   - Click three dots (⋯) on latest deployment
   - Click "Redeploy"
   - Wait 2-3 minutes

---

## Step 2: Configure Render (Backend) - CORS - 1 minute

### Set CORS Environment Variable:

1. **Go to:** https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/environment

2. **Find or Add:** `CORS_ORIGINS`

3. **Set Value to your Vercel frontend URL:**
   ```
   https://sports-app-taupe.vercel.app
   ```
   (Or check your Vercel dashboard for your actual frontend URL)

4. **Click "Save Changes"**

5. **Wait ~1 minute** for Render to redeploy automatically

---

## Step 3: Test Everything - 2 minutes

### Test 1: Backend Health
Visit: https://sports-app-ncya.onrender.com/health

**Expected:** `{"status": "healthy"}`

✅ If this works, your backend is running!

### Test 2: Frontend
Visit your Vercel frontend URL (e.g., `https://sports-app-taupe.vercel.app`)

**Expected:** App loads without errors

### Test 3: Connection
1. Open your frontend
2. Press **F12** (browser console)
3. Go to **"Network"** tab
4. Try to load games or make a prediction
5. Look for API requests to: `https://sports-app-ncya.onrender.com`

**Expected:** 
- ✅ Requests show `200 OK` status
- ✅ No CORS errors in Console tab
- ✅ Data loads successfully

---

## 🎉 Success Checklist

- [ ] Backend health check works: `https://sports-app-ncya.onrender.com/health`
- [ ] `NEXT_PUBLIC_API_URL` set in Vercel = `https://sports-app-ncya.onrender.com`
- [ ] Frontend redeployed in Vercel
- [ ] `CORS_ORIGINS` set in Render = your Vercel URL
- [ ] Frontend loads without errors
- [ ] API requests work (check browser Network tab)
- [ ] No CORS errors in browser console

---

## 🆘 Troubleshooting

### If Frontend Still Shows Error:
1. **Check Vercel Environment Variable:**
   - Make sure `NEXT_PUBLIC_API_URL` is set correctly
   - Make sure you redeployed after setting it

2. **Check Browser Console (F12):**
   - Look for error messages
   - Check Network tab for failed requests

### If You See CORS Errors:
1. **Check Render CORS_ORIGINS:**
   - Should include your exact Vercel URL
   - No trailing slashes
   - Wait for Render to finish redeploying

2. **Test Backend Directly:**
   - Visit: `https://sports-app-ncya.onrender.com/health`
   - Should work without CORS issues

---

## 📝 Quick Reference

**Backend URL:** `https://sports-app-ncya.onrender.com`

**Frontend URL:** Check your Vercel dashboard (likely `https://sports-app-taupe.vercel.app`)

**Vercel Config:** `NEXT_PUBLIC_API_URL` = `https://sports-app-ncya.onrender.com`

**Render Config:** `CORS_ORIGINS` = Your Vercel frontend URL

---

**Follow these steps and your app will be fully connected! 🚀**


