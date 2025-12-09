# 🚀 Quick Deployment Guide

Your app is ready to deploy to free cloud hosting with custom domain support!

## 📋 What's Been Set Up

✅ **Backend Configuration** (Render)
- `backend/render.yaml` - Render deployment config
- `backend/Procfile` - Process file for Render
- `backend/requirements.txt` - Python dependencies
- `backend/runtime.txt` - Python version
- Health check endpoint at `/health`

✅ **Frontend Configuration** (Vercel)
- `frontend/vercel.json` - Vercel deployment config
- `frontend/next.config.js` - Next.js production config
- Environment variable support

✅ **Documentation**
- `DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_QUICKSTART.md` - Quick 10-minute setup

---

## 🎯 Next Steps

### 1. Deploy Backend (5 minutes)
1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect repo: `Jmanjw93/Sports_App`
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `CORS_ORIGINS=https://your-app.vercel.app`
6. Deploy and copy your backend URL

### 2. Deploy Frontend (5 minutes)
1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Click "Add New" → "Project"
3. Import repo: `Jmanjw93/Sports_App`
4. Settings:
   - **Root Directory**: `frontend`
   - **Framework**: Next.js (auto-detected)
5. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`
6. Deploy and copy your frontend URL

### 3. Add Custom Domain (Optional)
- **Frontend**: Vercel Dashboard → Settings → Domains → Add your domain
- **Backend**: Render Dashboard → Settings → Custom Domains → Add subdomain

---

## 📚 Full Documentation

See `DEPLOYMENT.md` for:
- Detailed step-by-step instructions
- Custom domain DNS setup
- Troubleshooting guide
- Free tier limitations
- Security best practices

---

## 🆓 Free Tier Benefits

- **Vercel**: Unlimited deployments, 100GB bandwidth, custom domains
- **Render**: 750 hours/month, auto-scaling, free SSL
- **Both**: Automatic deployments on git push

---

## ✅ Verification

After deployment, test:
1. Backend: `https://your-backend.onrender.com/health` → Should return `{"status": "healthy"}`
2. Frontend: Visit your Vercel URL → Should load the app
3. API Connection: Make a prediction → Should connect to backend

---

## 🔄 Automatic Updates

Both platforms auto-deploy when you push to GitHub:
```bash
git push origin main
```

Your app will automatically update! 🎉

