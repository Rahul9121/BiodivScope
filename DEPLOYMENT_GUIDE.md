# 🚀 BiodivScope Deployment Guide

## Cloud Deployment: Railway + Vercel

This guide will help you deploy your BiodivScope application using:
- **Railway** - Backend API + PostgreSQL database
- **Vercel** - Frontend React app
- **GitHub** - Source code repository

---

## 📋 Prerequisites

1. **GitHub Account** - Your code repository
2. **Railway Account** - [railway.app](https://railway.app) (free tier available)
3. **Vercel Account** - [vercel.com](https://vercel.com) (free tier available)

---

## 🛠️ Step-by-Step Deployment

### Step 1: Push Latest Changes to GitHub

```bash
git add .
git commit -m "feat: prepare for Railway + Vercel deployment"
git push origin main
```

### Step 2: Deploy Backend on Railway

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project"

2. **Create PostgreSQL Database**
   - Click "Add Service" → "Database" → "PostgreSQL"
   - Railway will automatically create and configure the database
   - Note: The `DATABASE_URL` will be automatically provided

3. **Deploy Backend Service**
   - Click "Add Service" → "GitHub Repository"
   - Select your `BiodivScope` repository
   - Set Root Directory: `FullStackApp/backend`
   - Railway will automatically detect it's a Python app

4. **Configure Environment Variables**
   In Railway dashboard, go to your backend service → Variables:
   ```env
   FLASK_ENV=production
   SECRET_KEY=your_super_secure_secret_key_here_change_this
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```
   
   Note: `DATABASE_URL` is automatically provided by Railway

5. **Deploy**
   - Railway will automatically deploy when you push to GitHub
   - Your backend will be available at: `https://your-app.railway.app`

### Step 3: Deploy Frontend on Vercel

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"

2. **Import Repository**
   - Select your `BiodivScope` repository
   - Set Root Directory: `FullStackApp/frontend`
   - Framework Preset: `Create React App`

3. **Configure Environment Variables**
   In Vercel dashboard → Settings → Environment Variables:
   ```env
   REACT_APP_API_BASE_URL=https://your-railway-backend.railway.app
   REACT_APP_ENVIRONMENT=production
   ```

4. **Deploy**
   - Click "Deploy"
   - Your frontend will be available at: `https://your-app.vercel.app`

### Step 4: Update CORS Configuration

1. **Update Railway Backend CORS**
   - Go to Railway → Your Backend Service → Variables
   - Update `CORS_ORIGINS` with your Vercel URL:
   ```env
   CORS_ORIGINS=https://your-actual-vercel-domain.vercel.app,http://localhost:3000
   ```

2. **Redeploy Backend**
   - Railway will automatically redeploy with new environment variables

---

## 🔧 Configuration Files Included

✅ `FullStackApp/backend/railway.json` - Railway deployment config
✅ `FullStackApp/backend/app_railway.py` - Production-ready Flask app
✅ `FullStackApp/backend/config.py` - Environment-based configuration
✅ `vercel.json` - Vercel deployment configuration
✅ `.env.example` files for both frontend and backend

---

## 🗄️ Database Setup

Railway PostgreSQL will be automatically configured. The database will be empty initially, so you'll need to:

1. **Initialize Database Schema**
   - Your app should include database initialization code
   - Or you can run SQL scripts through Railway's PostgreSQL console

2. **Import Your Data**
   - Use Railway's PostgreSQL console to run your data import scripts
   - Or create database migration endpoints in your Flask app

---

## 🔍 Verification Steps

### Backend Health Check
```bash
curl https://your-railway-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "BiodivScope Backend API is running",
  "version": "1.0.0",
  "environment": "production"
}
```

### Frontend Check
- Visit your Vercel URL
- Verify the app loads and can connect to the backend
- Test user registration/login functionality

---

## 🚨 Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Ensure `CORS_ORIGINS` in Railway matches your Vercel domain exactly
   - Include both `https://` and no trailing slash

2. **Database Connection Issues**
   - Railway automatically provides `DATABASE_URL`
   - Check Railway logs for connection errors

3. **Build Failures**
   - Check Railway/Vercel build logs
   - Ensure all dependencies are in `requirements.txt` and `package.json`

4. **Environment Variables**
   - Verify all required env vars are set in both Railway and Vercel
   - Use Railway's variable interpolation: `${{POSTGRES_URL}}`

---

## 📊 Monitoring & Maintenance

- **Railway Logs**: Monitor backend performance and errors
- **Vercel Analytics**: Track frontend performance
- **Database Backups**: Railway provides automatic backups
- **SSL Certificates**: Automatically handled by both platforms

---

## 💰 Cost Considerations

**Free Tier Limits:**
- **Railway**: 500 hours/month, 1GB RAM, 1GB disk
- **Vercel**: Unlimited static deployments, 100GB bandwidth/month

**Upgrade when needed:**
- Railway Pro: $5/month per service
- Vercel Pro: $20/month

---

## 🎉 Your App URLs

After deployment, you'll have:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`
- **Database**: Managed by Railway (internal URL)

---

## 🔄 Auto-Deployment

Both platforms support auto-deployment:
- **Railway**: Deploys on every git push to `main`
- **Vercel**: Deploys on every git push to `main`

Your deployment is now complete! 🚀
