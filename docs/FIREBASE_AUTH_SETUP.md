# Firebase Authentication Setup Guide

This guide will help you integrate Firebase Authentication into the Person Detection & Identification System.

---

## 📋 Prerequisites

- Firebase account (free tier is sufficient)
- Node.js backend running
- Frontend accessible via browser

---

## 🔥 Step 1: Create Firebase Project

### 1.1 Go to Firebase Console
Visit: https://console.firebase.google.com/

### 1.2 Create New Project
1. Click "Add project"
2. Enter project name: `person-detection-system`
3. Disable Google Analytics (optional)
4. Click "Create project"

---

## 🔑 Step 2: Enable Authentication

### 2.1 Navigate to Authentication
1. In Firebase Console, click "Authentication" in left sidebar
2. Click "Get started"

### 2.2 Enable Sign-in Methods
1. Go to "Sign-in method" tab
2. Enable **Email/Password**:
   - Click on "Email/Password"
   - Toggle "Enable"
   - Click "Save"
3. (Optional) Enable **Google** sign-in:
   - Click on "Google"
   - Toggle "Enable"
   - Enter support email
   - Click "Save"

---

## 🔧 Step 3: Get Firebase Configuration

### 3.1 Register Web App
1. In Project Overview, click the **Web** icon (</>)
2. Enter app nickname: `person-detection-web`
3. Click "Register app"

### 3.2 Copy Configuration
You'll see configuration like this:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

**Save this configuration!**

---

## 🔐 Step 4: Get Service Account Key (Backend)

### 4.1 Go to Project Settings
1. Click gear icon ⚙️ next to "Project Overview"
2. Click "Project settings"

### 4.2 Generate Service Account Key
1. Go to "Service accounts" tab
2. Click "Generate new private key"
3. Click "Generate key"
4. Save the JSON file as `firebase-credentials.json`

### 4.3 Move to Backend Directory
```bash
# Move the downloaded file to backend-api folder
mv ~/Downloads/your-project-firebase-adminsdk-xxxxx.json backend-api/firebase-credentials.json
```

---

## 📝 Step 5: Configure Backend

### 5.1 Update .env File
Edit `backend-api/.env`:
```env
PORT=3000
NODE_ENV=development

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/person_detection

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_EXPIRE=7d

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# Face Recognition Configuration
FACE_MATCH_THRESHOLD=0.6
```

### 5.2 Restart Backend Server
```bash
cd backend-api
# Stop current server (Ctrl+C)
node server.js
```

You should see:
```
✅ Firebase initialized
```

---

## 🌐 Step 6: Configure Frontend

### 6.1 Update Firebase Config
Edit `frontend/js/firebaseConfig.js`:

Replace the placeholder config with your actual Firebase config:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

### 6.2 Add Firebase SDK to HTML
Edit `frontend/index.html` and add before closing `</body>` tag:

```html
<!-- Firebase SDK -->
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>

<!-- Firebase Config -->
<script src="js/firebaseConfig.js"></script>

<!-- Other scripts -->
<script src="js/config.js"></script>
<script src="js/api.js"></script>
<script src="js/auth.js"></script>
<script src="js/dashboard.js"></script>
<script src="js/persons.js"></script>
<script src="js/reports.js"></script>
<script src="js/alerts.js"></script>
<script src="js/app.js"></script>
```

---

## 🧪 Step 7: Test Firebase Authentication

### 7.1 Test Backend Endpoints

**Test Firebase Login** (after creating a user):
```powershell
# First, create a user in Firebase Console or use the register endpoint
# Then get the ID token and test:

$body = @{
    idToken = "YOUR_FIREBASE_ID_TOKEN_HERE"
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://localhost:3000/api/auth/firebase-login' -Method Post -Body $body -ContentType 'application/json'
```

**Test Firebase Register**:
```powershell
$body = @{
    email = "test@example.com"
    password = "test123456"
    fullName = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri 'http://localhost:3000/api/auth/firebase-register' -Method Post -Body $body -ContentType 'application/json'
```

### 7.2 Test Frontend Login

1. Open `http://localhost:8080`
2. You should see the login page
3. Enter email and password
4. Click "Login with Firebase" (if button added)

---

## 🎨 Step 8: Update Login UI (Optional)

### 8.1 Add Firebase Login Button

Edit `frontend/index.html` login form:

```html
<form id="loginForm">
    <div class="form-group">
        <label for="username">
            <i class="fas fa-user"></i> Email/Username
        </label>
        <input type="text" id="username" name="username" required>
    </div>
    <div class="form-group">
        <label for="password">
            <i class="fas fa-lock"></i> Password
        </label>
        <input type="password" id="password" name="password" required>
    </div>
    
    <!-- Regular Login -->
    <button type="submit" class="btn btn-primary">
        <i class="fas fa-sign-in-alt"></i> Login
    </button>
    
    <!-- Firebase Login (if configured) -->
    <button type="button" id="firebaseLoginBtn" class="btn btn-secondary" style="margin-top: 10px;">
        <i class="fab fa-google"></i> Sign in with Google
    </button>
</form>
```

### 8.2 Add Firebase Login Handler

Edit `frontend/js/auth.js` and add:

```javascript
// Firebase login handler
document.addEventListener('DOMContentLoaded', () => {
    const firebaseLoginBtn = document.getElementById('firebaseLoginBtn');
    
    if (firebaseLoginBtn) {
        firebaseLoginBtn.addEventListener('click', async () => {
            if (!isFirebaseAvailable()) {
                alert('Firebase is not configured');
                return;
            }
            
            try {
                const result = await firebaseSignInWithGoogle();
                
                if (result.success) {
                    // Store token and user data
                    localStorage.setItem(CONFIG.TOKEN_KEY, result.token);
                    localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(result.user));
                    
                    // Redirect to dashboard
                    authManager.showDashboard();
                    dashboardManager.init();
                } else {
                    alert('Firebase login failed: ' + result.error);
                }
            } catch (error) {
                alert('Firebase login error: ' + error.message);
            }
        });
    }
});
```

---

## 📊 Step 9: Verify Integration

### 9.1 Check Backend
```bash
# Backend should show:
✅ Connected to MongoDB
✅ Firebase initialized
🚀 Server running on port 3000
```

### 9.2 Check Frontend Console
Open browser console (F12) and check for:
```
Firebase initialized successfully
```

### 9.3 Test Complete Flow

1. **Register User**:
   - Use Firebase Console or API
   - Create user with email/password

2. **Login**:
   - Use frontend login form
   - Or use Google sign-in button

3. **Verify**:
   - Check MongoDB for user record
   - Check Firebase Console for user
   - Verify JWT token generated

---

## 🔄 API Endpoints

### Firebase Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/firebase-login` | POST | Login with Firebase ID token |
| `/api/auth/firebase-register` | POST | Register user in Firebase & MongoDB |
| `/api/auth/verify-firebase-token` | POST | Verify Firebase ID token |

### Request/Response Examples

**Firebase Login**:
```json
// Request
POST /api/auth/firebase-login
{
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
}

// Response
{
  "message": "Firebase login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "user": {
    "id": "user_id",
    "username": "user",
    "email": "user@example.com",
    "role": "viewer"
  },
  "firebaseVerified": true
}
```

**Firebase Register**:
```json
// Request
POST /api/auth/firebase-register
{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "fullName": "New User"
}

// Response
{
  "message": "User registered successfully with Firebase",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "user": {
    "id": "user_id",
    "username": "newuser",
    "email": "newuser@example.com",
    "role": "viewer"
  },
  "firebaseUid": "firebase_uid_here"
}
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit `firebase-credentials.json` to git
- Add to `.gitignore`:
```
firebase-credentials.json
*-firebase-adminsdk-*.json
```

### 2. Firebase Rules
Set up Firebase Security Rules in Firebase Console:
```javascript
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

### 3. CORS Configuration
Update backend CORS if needed:
```javascript
app.use(cors({
  origin: ['http://localhost:8080', 'https://yourdomain.com'],
  credentials: true
}));
```

---

## 🐛 Troubleshooting

### Issue: "Firebase not initialized"
**Solution**: Check if `firebase-credentials.json` exists and path in `.env` is correct

### Issue: "Invalid ID token"
**Solution**: 
- Token might be expired
- Check Firebase project ID matches
- Verify API key is correct

### Issue: "User already exists"
**Solution**: User email already registered. Use login instead of register.

### Issue: Frontend can't connect
**Solution**:
- Check Firebase SDK scripts are loaded
- Verify firebaseConfig has correct values
- Check browser console for errors

---

## 📚 Additional Resources

- [Firebase Auth Documentation](https://firebase.google.com/docs/auth)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Firebase Web SDK](https://firebase.google.com/docs/web/setup)

---

## ✅ Checklist

- [ ] Firebase project created
- [ ] Email/Password authentication enabled
- [ ] Firebase web app registered
- [ ] Service account key downloaded
- [ ] `firebase-credentials.json` in backend folder
- [ ] `.env` file updated
- [ ] Frontend `firebaseConfig.js` updated
- [ ] Firebase SDK scripts added to HTML
- [ ] Backend restarted
- [ ] Firebase initialization confirmed
- [ ] Test user created
- [ ] Login tested successfully

---

## 🎯 Quick Start Commands

```bash
# 1. Setup backend
cd backend-api
# Add firebase-credentials.json file
# Update .env file
node server.js

# 2. Setup frontend
cd frontend
# Update firebaseConfig.js
# Update index.html with Firebase SDK
python -m http.server 8080

# 3. Test
# Open http://localhost:8080
# Login with Firebase credentials
```

---

**Setup Complete!** 🎉

Your system now supports both traditional JWT authentication and Firebase Authentication!

---

**Last Updated**: October 12, 2025  
**Firebase SDK Version**: 9.22.0  
**Status**: Ready for Production
