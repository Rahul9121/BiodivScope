# 🚀 Railway Backend Deployment Guide

## Current Status
✅ Frontend deployed on Vercel
🔄 Backend deployment to Railway (in progress)

## Pre-requisites
1. GitHub repository: https://github.com/Rahul9121/BiodivScope
2. Railway account: [railway.app](https://railway.app)
3. Code updated with Railway configuration

## Step-by-Step Railway Deployment

### Step 1: Login to Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with your GitHub account
3. Click "New Project"

### Step 2: Create PostgreSQL Database
1. Click "Add Service" → "Database" → "PostgreSQL"
2. Railway will automatically provision a PostgreSQL database
3. The `DATABASE_URL` environment variable will be automatically set

### Step 3: Deploy Backend Service
1. Click "Add Service" → "GitHub Repository"
2. Select your `BiodivScope` repository
3. **IMPORTANT**: Set the root directory to `FullStackApp/backend`
4. Railway will auto-detect Python and use the configuration files

### Step 4: Configure Environment Variables
In Railway dashboard, go to your backend service → Variables and add:

```env
FLASK_ENV=production
SECRET_KEY=your_super_secure_secret_key_change_this_immediately
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

**Replace `your-vercel-app.vercel.app` with your actual Vercel domain**

### Step 5: Monitor Deployment
1. Check the deployment logs in Railway dashboard
2. Look for successful startup messages
3. Test the health endpoint: `https://your-app.railway.app/health`

## Expected Deployment Files Used

Railway will use these files for deployment:
- `FullStackApp/backend/app_railway.py` - Main application file
- `FullStackApp/backend/requirements.txt` - Python dependencies
- `FullStackApp/backend/nixpacks.toml` - Build configuration
- `FullStackApp/backend/railway.json` - Railway-specific settings

## Health Check Endpoint

Your backend will be available at: `https://your-project-name.railway.app`

Test with:
```bash
curl https://your-project-name.railway.app/health
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

## Connect Frontend to Backend

After successful Railway deployment:

1. **Update Vercel Environment Variables**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Update `REACT_APP_API_BASE_URL` to your Railway URL:
   ```env
   REACT_APP_API_BASE_URL=https://your-project-name.railway.app
   ```

2. **Update Railway CORS**:
   - Add your Vercel domain to `CORS_ORIGINS` in Railway:
   ```env
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

## Troubleshooting

### Common Issues:

1. **Build Failure**: Check Railway logs for missing dependencies
2. **Health Check Failure**: Ensure `/health` endpoint is accessible
3. **CORS Errors**: Verify CORS_ORIGINS matches your Vercel domain exactly
4. **Database Connection**: Railway automatically provides DATABASE_URL

### GitHub Actions Issues Fixed:
- Updated workflow to match current project structure
- Added conditional tests (skips if no tests exist)
- Fixed dependency installation paths

## Next Steps After Successful Deployment

1. **Test the full application flow**:
   - Frontend on Vercel connects to backend on Railway
   - Database operations work correctly
   - CORS is properly configured

2. **Set up monitoring**:
   - Monitor Railway logs for errors
   - Check Vercel analytics for frontend performance

3. **Database initialization**:
   - Use Railway PostgreSQL console to run any required SQL scripts
   - Or implement database initialization in your Flask app

## Files Modified for This Deployment

- `.github/workflows/deploy.yml` - Fixed GitHub Actions
- `railway.toml` - Root-level Railway configuration
- `FullStackApp/backend/requirements.txt` - Added all necessary dependencies
- `FullStackApp/backend/nixpacks.toml` - Updated to use app_railway.py
- `RAILWAY_DEPLOYMENT_STEPS.md` - This guide

## Environment Variables Summary

### Railway (Backend):
```env
FLASK_ENV=production
SECRET_KEY=your_super_secure_secret_key
CORS_ORIGINS=https://your-vercel-app.vercel.app
DATABASE_URL=postgresql://... (auto-provided)
```

### Vercel (Frontend):
```env
REACT_APP_API_BASE_URL=https://your-railway-app.railway.app
REACT_APP_ENVIRONMENT=production
```

## Support

If you encounter issues:
1. Check Railway deployment logs
2. Verify environment variables are set correctly
3. Test health endpoint accessibility
4. Ensure CORS configuration matches your domains
