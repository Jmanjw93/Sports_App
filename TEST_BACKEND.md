# 🔍 How to Test Your Backend

## ⚠️ Important: Health Endpoint is on BACKEND, not Frontend

The `/health` endpoint is on your **Render backend**, not your Vercel frontend.

---

## Step 1: Get Your Backend URL

1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg
2. Look at the top of the page for your **Public URL**
3. It should look like: `https://sports-app-ncya.onrender.com`
4. **Copy this URL**

---

## Step 2: Test Backend Health Endpoint

Visit this URL in your browser:
```
https://your-backend-url.onrender.com/health
```

**Replace `your-backend-url` with your actual Render URL**

**Expected Response:**
```json
{"status": "healthy"}
```

---

## Step 3: Test Backend Root Endpoint

Visit:
```
https://your-backend-url.onrender.com/
```

**Expected Response:**
```json
{
  "message": "Sports Analytics API",
  "version": "1.0.0",
  "endpoints": {
    "games": "/api/games",
    "predictions": "/api/predictions",
    "odds": "/api/odds",
    "bets": "/api/bets"
  }
}
```

---

## Step 4: Test API Endpoint

Try:
```
https://your-backend-url.onrender.com/api/games/?sport=nfl&days_ahead=7
```

This should return a list of games (or an empty array if no games).

---

## Common Issues

### Issue 1: Backend is Sleeping (Free Tier)
- **Symptom**: First request takes 30-60 seconds
- **Solution**: This is normal - wait for it to wake up
- **Test**: Try the request again after waiting

### Issue 2: 404 Not Found
- **Symptom**: Getting 404 on backend URL
- **Possible Causes**:
  - Wrong URL (check Render dashboard)
  - Service not deployed
  - Service failed to start

### Issue 3: Connection Timeout
- **Symptom**: Request times out
- **Possible Causes**:
  - Backend crashed
  - Check Render logs for errors

---

## How to Check Backend Status

1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg
2. Check the status:
   - ✅ **"Live"** = Backend is running
   - ⚠️ **"Sleeping"** = Free tier, will wake on request
   - ❌ **"Error"** = Backend has issues

---

## How to Check Backend Logs

1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/logs
2. Look for:
   - Red error messages
   - Import errors
   - Startup errors

---

## Quick Test Checklist

- [ ] Got backend URL from Render dashboard
- [ ] Tested `/health` endpoint → Returns `{"status": "healthy"}`
- [ ] Tested `/` endpoint → Returns API info
- [ ] Backend status shows "Live" or "Sleeping"
- [ ] No errors in Render logs

---

**Remember: Frontend URL ≠ Backend URL**

- **Frontend**: `https://sports-app-taupe.vercel.app` (or similar)
- **Backend**: `https://sports-app-ncya.onrender.com` (or similar)

Test the **backend URL** for the health endpoint!


