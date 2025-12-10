# ✅ Verify Your Connection

After configuring both servers, use this guide to verify everything works.

---

## Step 1: Test Backend Health

1. Open your browser
2. Visit: `https://your-backend-url.onrender.com/health`
   (Replace with your actual Render URL)
3. You should see: `{"status": "healthy"}`

**If this doesn't work:**
- Check Render dashboard - is the service "Live"?
- Check Render logs for errors
- Verify the URL is correct

---

## Step 2: Test Frontend

1. Visit: `https://sports-app-taupe.vercel.app`
2. The app should load
3. You should see the sports analytics interface

**If this doesn't work:**
- Check Vercel dashboard - is the deployment successful?
- Check Vercel logs for errors
- Verify the URL is correct

---

## Step 3: Test API Connection

1. Open your frontend: `https://sports-app-taupe.vercel.app`
2. Open browser console: Press **F12**
3. Go to **"Network"** tab
4. Try to make a prediction or load games
5. Look for API requests in the Network tab
6. Check if they're going to your Render backend URL

**What to look for:**
- ✅ Requests to `https://your-backend.onrender.com/api/...`
- ✅ Status code: `200 OK`
- ❌ CORS errors in Console tab
- ❌ Network errors (red requests)

---

## Step 4: Check for Errors

### In Browser Console (F12):
- **Console Tab**: Look for red error messages
- **Network Tab**: Look for failed requests (red)

### Common Errors:

#### CORS Error:
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```
**Fix**: Make sure `CORS_ORIGINS` in Render includes your exact Vercel URL

#### Network Error:
```
Failed to fetch
NetworkError when attempting to fetch resource
```
**Fix**: 
- Check `NEXT_PUBLIC_API_URL` in Vercel matches your Render URL
- Verify backend is running (test `/health` endpoint)

#### 404 Not Found:
```
404 Not Found
```
**Fix**: Check the API endpoint path is correct

---

## Step 5: Verify Environment Variables

### In Render:
1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/environment
2. Verify `CORS_ORIGINS` is set to your Vercel URL
3. Should look like: `https://sports-app-taupe.vercel.app`

### In Vercel:
1. Go to: https://vercel.com/jmanjw93s-projects/sports-app/89Spn3nUXysiYX1wBJVbqQDf3HdW/settings/environment-variables
2. Verify `NEXT_PUBLIC_API_URL` is set to your Render URL
3. Should look like: `https://sports-app-ncya.onrender.com` (no trailing slash)

---

## ✅ Success Indicators

Your app is working if:
- ✅ Backend health check returns `{"status": "healthy"}`
- ✅ Frontend loads without errors
- ✅ API requests in Network tab show `200 OK`
- ✅ No CORS errors in console
- ✅ Predictions/games load successfully

---

## 🆘 Still Having Issues?

1. **Double-check URLs**: Make sure there are no typos
2. **Wait for redeploy**: Both services need to redeploy after changes
3. **Clear browser cache**: Hard refresh (Ctrl+F5 or Cmd+Shift+R)
4. **Check logs**: Both Render and Vercel have detailed logs

---

**Once all checks pass, your app is fully connected! 🎉**


