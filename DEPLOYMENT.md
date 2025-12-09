# Deployment Guide - Free Cloud Hosting with Custom Domain

This guide will help you deploy your sports analytics app to free cloud hosting services with your own custom domain.

## Architecture

- **Frontend (Next.js)**: Deploy to Vercel (free tier, excellent Next.js support)
- **Backend (FastAPI)**: Deploy to Render (free tier, supports Python/FastAPI)
- **Custom Domain**: Configure DNS to point to your deployments

---

## Step 1: Deploy Backend to Render

### 1.1 Create Render Account
1. Go to [https://render.com](https://render.com)
2. Sign up for a free account (GitHub login recommended)

### 1.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Jmanjw93/Sports_App`
3. Configure the service:
   - **Name**: `sports-analytics-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

### 1.3 Set Environment Variables
In Render dashboard, go to "Environment" tab and add:
```
PYTHON_VERSION=3.11
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com,https://your-app.vercel.app
PORT=10000
```

### 1.4 Deploy
1. Click "Create Web Service"
2. Render will automatically deploy your backend
3. Wait for deployment to complete
4. Copy your backend URL (e.g., `https://sports-analytics-api.onrender.com`)

### 1.5 Custom Domain (Backend) - Optional
1. In Render dashboard, go to "Settings" → "Custom Domains"
2. Add your subdomain (e.g., `api.your-domain.com`)
3. Follow DNS instructions to add CNAME record

---

## Step 2: Deploy Frontend to Vercel

### 2.1 Create Vercel Account
1. Go to [https://vercel.com](https://vercel.com)
2. Sign up for a free account (GitHub login recommended)

### 2.2 Import Project
1. Click "Add New" → "Project"
2. Import your GitHub repository: `Jmanjw93/Sports_App`
3. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

### 2.3 Set Environment Variables
In Vercel dashboard, go to "Settings" → "Environment Variables" and add:
```
NEXT_PUBLIC_API_URL=https://sports-analytics-api.onrender.com
```
(Replace with your actual Render backend URL)

### 2.4 Deploy
1. Click "Deploy"
2. Vercel will automatically build and deploy your frontend
3. Wait for deployment to complete
4. Copy your frontend URL (e.g., `https://sports-app.vercel.app`)

### 2.5 Custom Domain (Frontend)
1. In Vercel dashboard, go to "Settings" → "Domains"
2. Add your domain (e.g., `your-domain.com` and `www.your-domain.com`)
3. Follow DNS instructions:
   - Add A record pointing to Vercel's IP addresses
   - Or add CNAME record pointing to your Vercel deployment URL

---

## Step 3: Configure DNS for Custom Domain

### 3.1 Domain Setup
You'll need to configure DNS records with your domain registrar:

#### For Frontend (Main Domain)
```
Type: A Record
Name: @
Value: 76.76.21.21 (Vercel's IP - check Vercel dashboard for current IPs)

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

#### For Backend (Subdomain) - Optional
```
Type: CNAME
Name: api
Value: your-backend-service.onrender.com
```

### 3.2 Update Environment Variables
After setting up custom domains, update:

**Vercel (Frontend)**:
```
NEXT_PUBLIC_API_URL=https://api.your-domain.com
```
(Or keep using Render URL if not using custom backend domain)

**Render (Backend)**:
```
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

---

## Step 4: Update Code for Production

### 4.1 Update Frontend API URL
The frontend is already configured to use `NEXT_PUBLIC_API_URL` environment variable, which will be set in Vercel.

### 4.2 Update Backend CORS
The backend CORS is configured in `app/config.py`. Update it to allow your production domains.

---

## Step 5: Verify Deployment

1. **Test Frontend**: Visit your Vercel URL or custom domain
2. **Test Backend**: Visit `https://your-backend-url.onrender.com/health`
3. **Test API Connection**: Make a prediction in the frontend and verify it connects to backend

---

## Free Tier Limitations

### Vercel (Frontend)
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Custom domains
- ⚠️ Sleeps after 30 days of inactivity (wakes on first request)

### Render (Backend)
- ✅ 750 hours/month free
- ✅ Sleeps after 15 minutes of inactivity
- ✅ Wakes automatically on request (may take 30-60 seconds)
- ⚠️ For always-on, consider upgrading to paid tier

### Alternative: Railway (Backend)
If you prefer always-on backend:
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo
3. Deploy backend service
4. Free tier: $5 credit/month (usually enough for small apps)

---

## Troubleshooting

### Backend Not Responding
- Check Render logs for errors
- Verify environment variables are set
- Ensure `requirements.txt` includes all dependencies
- Check that PORT environment variable is set

### Frontend Can't Connect to Backend
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check CORS settings in backend
- Ensure backend URL is accessible (test in browser)

### Custom Domain Not Working
- DNS changes can take 24-48 hours to propagate
- Use [whatsmydns.net](https://www.whatsmydns.net) to check DNS propagation
- Verify DNS records match Vercel/Render instructions exactly

---

## Monitoring & Updates

### Automatic Deployments
Both Vercel and Render automatically deploy when you push to GitHub:
```bash
git push origin main
```

### View Logs
- **Vercel**: Dashboard → Your Project → "Deployments" → Click deployment → "Logs"
- **Render**: Dashboard → Your Service → "Logs" tab

### Manual Redeploy
- **Vercel**: Dashboard → "Deployments" → "Redeploy"
- **Render**: Dashboard → "Manual Deploy" → "Deploy latest commit"

---

## Security Notes

1. **Environment Variables**: Never commit API keys or secrets to GitHub
2. **CORS**: Keep CORS origins restricted to your domains
3. **HTTPS**: Both Vercel and Render provide free SSL certificates
4. **Rate Limiting**: Consider adding rate limiting for production use

---

## Next Steps

1. Set up monitoring (optional): Add error tracking (Sentry, etc.)
2. Set up CI/CD: Already automatic with GitHub integration
3. Add database (optional): For persistent storage, consider:
   - Render PostgreSQL (free tier)
   - Supabase (free tier)
   - Railway PostgreSQL (free tier)

---

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Custom Domain Setup**: Check respective platform documentation

