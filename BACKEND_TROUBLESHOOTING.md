# 🔧 Backend Troubleshooting Guide

## Common Backend Issues on Render

### Issue 1: Backend Not Starting

**Symptoms:**
- Service shows "Error" or "Failed" status
- Health check fails
- No response from `/health` endpoint

**Solutions:**

1. **Check Render Logs:**
   - Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/logs
   - Look for error messages
   - Common errors:
     - `ModuleNotFoundError` - Missing dependency
     - `ImportError` - Import issue
     - `Port already in use` - Port conflict

2. **Verify Start Command:**
   - Should be: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Check in Render Dashboard → Settings → Start Command

3. **Check Root Directory:**
   - Should be: `backend`
   - Check in Render Dashboard → Settings → Root Directory

---

### Issue 2: Build Fails

**Symptoms:**
- Deployment shows "Build Failed"
- Red error messages in build logs

**Solutions:**

1. **Check requirements.txt:**
   - Make sure all dependencies are listed
   - Verify Python version compatibility

2. **Common Build Errors:**
   - **NumPy issues**: Should use `numpy>=1.26.0` for Python 3.11+
   - **Missing dependencies**: Add to requirements.txt
   - **Python version**: Check runtime.txt has correct version

3. **Fix Build Command:**
   - Should be: `pip install --upgrade pip && pip install -r requirements.txt`
   - Or just: `pip install -r requirements.txt`

---

### Issue 3: Backend Sleeping (Free Tier)

**Symptoms:**
- First request takes 30-60 seconds
- Service shows "Sleeping" status

**Solutions:**
- This is normal for Render free tier
- Backend wakes up automatically on first request
- Consider upgrading to paid tier for always-on service

---

### Issue 4: CORS Errors

**Symptoms:**
- Frontend can't connect to backend
- Browser console shows CORS errors

**Solutions:**

1. **Check CORS_ORIGINS in Render:**
   - Go to: Environment tab
   - Find `CORS_ORIGINS`
   - Should include your Vercel URL: `https://sports-app-taupe.vercel.app`
   - No trailing slashes
   - Multiple origins separated by commas

2. **Verify CORS Configuration:**
   - Check `backend/app/config.py` - CORS should read from environment variable
   - Check `backend/app/main.py` - CORS middleware should be configured

---

### Issue 5: Port Issues

**Symptoms:**
- Service fails to start
- "Port already in use" errors

**Solutions:**
- Use `$PORT` environment variable in start command
- Render automatically sets PORT
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## Step-by-Step Debugging

### Step 1: Check Service Status
1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg
2. Check status:
   - ✅ "Live" = Working
   - ⚠️ "Sleeping" = Free tier, will wake on request
   - ❌ "Error" = Problem

### Step 2: Check Logs
1. Go to: https://dashboard.render.com/web/srv-d4s9imvdiees73a98brg/logs
2. Look for:
   - Red error messages
   - Import errors
   - Missing module errors
   - Port conflicts

### Step 3: Test Health Endpoint
1. Get your backend URL from Render dashboard
2. Visit: `https://your-backend-url.onrender.com/health`
3. Should return: `{"status": "healthy"}`

### Step 4: Check Environment Variables
1. Go to: Environment tab
2. Verify:
   - `CORS_ORIGINS` is set
   - `PYTHON_VERSION` is set (optional)
   - `PORT` is set automatically by Render

### Step 5: Verify Configuration
1. **Root Directory**: Should be `backend`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## Quick Fixes

### Fix 1: Rebuild Service
1. Render Dashboard → Your Service
2. Click "Manual Deploy" → "Deploy latest commit"
3. Wait for build to complete

### Fix 2: Check Requirements
Make sure `backend/requirements.txt` has:
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-multipart>=0.0.6
requests>=2.31.0
python-dateutil>=2.8.2
numpy>=1.26.0
```

### Fix 3: Verify File Structure
Make sure files are in correct locations:
```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   └── ...
├── requirements.txt
├── Procfile
└── runtime.txt
```

---

## Common Error Messages

### "ModuleNotFoundError: No module named 'X'"
**Fix**: Add missing module to `requirements.txt`

### "ImportError: cannot import name 'X'"
**Fix**: Check import paths, verify file structure

### "Port 10000 already in use"
**Fix**: Use `$PORT` instead of hardcoded port

### "Build failed"
**Fix**: Check build logs, verify requirements.txt

---

## Need More Help?

1. **Check Render Documentation**: https://render.com/docs
2. **Check Logs**: Always check logs first - they show the exact error
3. **Test Locally**: Try running backend locally to isolate issues

---

## Quick Checklist

- [ ] Service status is "Live" or "Sleeping" (not "Error")
- [ ] Build completed successfully
- [ ] Health endpoint works: `/health`
- [ ] CORS_ORIGINS is set correctly
- [ ] Start command uses `$PORT`
- [ ] Root directory is `backend`
- [ ] All dependencies in requirements.txt

---

**Share the specific error message from Render logs for more targeted help!**


