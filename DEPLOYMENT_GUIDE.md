# Backend Deployment Guide

This guide will help you deploy the Missing Person Detection System backend to Render.com (free tier).

## Prerequisites

- GitHub account (already done ✓)
- MongoDB Atlas account (free - we'll create this)
- Render.com account (free)

## Step 1: Set Up MongoDB Atlas (Free Cloud Database)

### 1.1 Create Account
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up with Google/GitHub or email
3. Choose **FREE** tier (M0 Sandbox)

### 1.2 Create Cluster
1. Click **"Build a Database"**
2. Select **FREE** (Shared, M0)
3. Choose region closest to you (e.g., Singapore, Mumbai, etc.)
4. Click **"Create"**

### 1.3 Set Up Database Access
1. Go to **"Database Access"** (left sidebar)
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Username: `admin` (or your choice)
5. Password: Click **"Autogenerate Secure Password"** and **SAVE IT**
6. Database User Privileges: **"Atlas Admin"**
7. Click **"Add User"**

### 1.4 Set Up Network Access
1. Go to **"Network Access"** (left sidebar)
2. Click **"Add IP Address"**
3. Click **"Allow Access From Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

### 1.5 Get Connection String
1. Go to **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Copy the connection string (looks like):
   ```
   mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password
6. Change the database name to `/person_detection` before `?retryWrites`:
   ```
   mongodb+srv://admin:yourpassword@cluster0.xxxxx.mongodb.net/person_detection?retryWrites=true&w=majority
   ```
7. **SAVE THIS CONNECTION STRING** - you'll need it for Render

## Step 2: Deploy Backend to Render.com

### 2.1 Create Render Account
1. Go to https://render.com/
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest)
4. Authorize Render to access your repositories

### 2.2 Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository: **Missing-Person-Detection-System**
4. Click **"Connect"**

### 2.3 Configure Service
Fill in these settings:

**Basic Settings:**
- **Name**: `missing-person-detection-api`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Node`
- **Build Command**: 
  ```
  cd backend-api && npm install
  ```
- **Start Command**: 
  ```
  cd backend-api && node server.js
  ```

**Advanced Settings:**
- **Plan**: Select **"Free"**
- **Auto-Deploy**: Yes (recommended)

### 2.4 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

1. **MONGODB_URI**
   - Key: `MONGODB_URI`
   - Value: `mongodb+srv://admin:yourpassword@cluster0.xxxxx.mongodb.net/person_detection?retryWrites=true&w=majority`
   - (Use your actual connection string from Step 1.5)

2. **JWT_SECRET**
   - Key: `JWT_SECRET`
   - Value: `your-super-secret-jwt-key-change-this-in-production`
   - (Or click "Generate" to auto-generate)

3. **PORT**
   - Key: `PORT`
   - Value: `3000`

4. **NODE_ENV**
   - Key: `NODE_ENV`
   - Value: `production`

5. **ALLOWED_ORIGINS**
   - Key: `ALLOWED_ORIGINS`
   - Value: `https://priyanshulink.github.io`

### 2.5 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Once deployed, you'll see a URL like: `https://missing-person-detection-api.onrender.com`
4. **SAVE THIS URL** - you'll need it for frontend

## Step 3: Update Frontend Configuration

### 3.1 Update config.js
1. Open `js/config.js` in your project
2. Replace `'https://your-backend-url.com'` with your actual Render URL:
   ```javascript
   API_BASE_URL: isGitHubPages ? 'https://missing-person-detection-api.onrender.com' : 'http://localhost:3000',
   SOCKET_URL: isGitHubPages ? 'https://missing-person-detection-api.onrender.com' : 'http://localhost:3000',
   ```

### 3.2 Commit and Push
```bash
git add js/config.js
git commit -m "Update backend URL for production"
git push
```

### 3.3 Wait for GitHub Pages to Update
- GitHub Pages will auto-deploy (2-3 minutes)
- Visit: https://priyanshulink.github.io/Missing-Person-Detection-System/

## Step 4: Test Your Deployment

### 4.1 Test Backend
Visit your Render URL in browser:
```
https://missing-person-detection-api.onrender.com/health
```
Should return: `{"status":"ok"}`

### 4.2 Test Frontend
1. Visit: https://priyanshulink.github.io/Missing-Person-Detection-System/
2. Try to login with default credentials:
   - Email: `ompriyanshu12@gmail.com`
   - Password: `pradeep3133`

## Troubleshooting

### Backend Issues

**Error: "Application failed to respond"**
- Check Render logs: Dashboard → Your Service → Logs
- Verify MongoDB connection string is correct
- Ensure all environment variables are set

**Error: "MongoServerError: bad auth"**
- Password in connection string is incorrect
- Create new database user in MongoDB Atlas

**Error: "Cannot connect to database"**
- Check Network Access in MongoDB Atlas
- Ensure 0.0.0.0/0 is allowed

### Frontend Issues

**Error: "Failed to fetch"**
- Backend URL in `js/config.js` is wrong
- Backend is not deployed yet
- CORS is blocking requests

**Login doesn't work**
- Check browser console for errors
- Verify backend URL is correct
- Check backend logs on Render

## Important Notes

### Free Tier Limitations

**Render.com Free Tier:**
- ✅ Suitable for demo/portfolio projects
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds
- ✅ 750 hours/month free
- ✅ Auto-deploys from GitHub

**MongoDB Atlas Free Tier:**
- ✅ 512 MB storage (plenty for demo)
- ✅ Shared cluster
- ✅ Permanent free tier

### Production Considerations

For a production system, consider:
- Paid hosting for faster response times
- Dedicated database cluster
- SSL certificates (Render provides free)
- Environment-specific configurations
- Backup strategies

## Next Steps

Once deployed:

1. ✅ Add missing persons through the dashboard
2. ✅ Configure cameras
3. ✅ Test face recognition
4. ✅ Monitor alerts

## Support

If you encounter issues:
1. Check Render logs
2. Check MongoDB Atlas metrics
3. Check browser console for frontend errors
4. Review this guide again

## Success!

Once everything is deployed:
- Frontend: https://priyanshulink.github.io/Missing-Person-Detection-System/
- Backend: https://your-service-name.onrender.com
- Database: MongoDB Atlas (cloud)

Your Missing Person Detection System is now live on the internet! 🎉
