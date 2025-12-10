# Quick Start Deployment Guide

## 🚀 Deploy in 10 Minutes

### Prerequisites
- GitHub account with your repo: `Jmanjw93/Sports_App`
- Domain name (optional but recommended)

---

## Backend Deployment (Render) - 5 minutes

1. **Sign up**: Go to [render.com](https://render.com) and sign up with GitHub

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect repo: `Jmanjw93/Sports_App`
   - Settings:
     - **Name**: `sports-analytics-api`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables** (in Render dashboard):
   ```
   PYTHON_VERSION=3.11
   PORT=10000
   CORS_ORIGINS=https://your-app.vercel.app
   ```

4. **Deploy**: Click "Create Web Service"
   - Copy your backend URL: `https://sports-analytics-api.onrender.com`

---

## Frontend Deployment (Vercel) - 5 minutes

1. **Sign up**: Go to [vercel.com](https://vercel.com) and sign up with GitHub

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import: `Jmanjw93/Sports_App`
   - Settings:
     - **Root Directory**: `frontend`
     - **Framework**: Next.js (auto-detected)

3. **Environment Variables** (in Vercel dashboard):
   ```
   NEXT_PUBLIC_API_URL=https://sports-analytics-api.onrender.com
   ```
   (Use your actual Render backend URL)

4. **Deploy**: Click "Deploy"
   - Copy your frontend URL: `https://sports-app.vercel.app`

---

## Custom Domain Setup

### Frontend (Vercel)
1. Vercel Dashboard → Your Project → "Settings" → "Domains"
2. Add your domain: `your-domain.com`
3. Follow DNS instructions:
   - Add A record: `@` → `76.76.21.21` (check Vercel for current IPs)
   - Add CNAME: `www` → `cname.vercel-dns.com`
4. Update environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://api.your-domain.com
   ```
   (Or keep using Render URL)

### Backend (Render) - Optional
1. Render Dashboard → Your Service → "Settings" → "Custom Domains"
2. Add subdomain: `api.your-domain.com`
3. Add CNAME record in DNS:
   - `api` → `your-service.onrender.com`

---

## Verify Deployment

1. **Test Backend**: Visit `https://your-backend.onrender.com/health`
   - Should return: `{"status": "healthy"}`

2. **Test Frontend**: Visit your Vercel URL
   - Should load the app
   - Try making a prediction to test API connection

---

## Automatic Updates

Both platforms auto-deploy on git push:
```bash
git push origin main
```

---

## Free Tier Notes

- **Vercel**: Free forever, sleeps after 30 days inactivity
- **Render**: Free tier sleeps after 15 min, wakes on request (30-60 sec delay)
- **Custom Domains**: Free on both platforms
- **SSL/HTTPS**: Automatic and free

---

## Troubleshooting

**Backend not responding?**
- Check Render logs
- Verify PORT environment variable
- Check requirements.txt has all dependencies

**Frontend can't connect?**
- Verify NEXT_PUBLIC_API_URL in Vercel
- Check CORS_ORIGINS in Render includes your frontend URL
- Test backend URL directly in browser

**Custom domain not working?**
- DNS changes take 24-48 hours
- Verify DNS records match platform instructions
- Check [whatsmydns.net](https://www.whatsmydns.net) for propagation

---

## Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Support**: Check platform documentation for detailed guides


