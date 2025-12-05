# Clear Browser Cache to See Camera Name Changes

## The Issue

You're seeing "Camera: cam02" instead of "Camera: Library Hall Camera" because your browser is using cached (old) JavaScript files.

## Quick Fix - Force Refresh

### Option 1: Hard Refresh (Easiest)
Press these keys while on the dashboard:

**Windows:**
```
Ctrl + Shift + R
or
Ctrl + F5
```

**Mac:**
```
Cmd + Shift + R
```

### Option 2: Clear Cache in Browser

**Chrome/Edge:**
1. Press `F12` to open Developer Tools
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

**Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cached Web Content"
3. Click "Clear Now"

### Option 3: Incognito/Private Mode
Open the dashboard in a new incognito/private window:
```
Ctrl + Shift + N (Chrome/Edge)
Ctrl + Shift + P (Firefox)
```

Then go to: `http://localhost:8080`

## After Clearing Cache

You should now see:

**Before (Old - Cached):**
```
Om Singh
Camera: cam02
10/29/2025, 10:03:40 PM
Status: pending
```

**After (New - Updated):**
```
Om Singh
📹 Library Hall Camera
📍 Library First Floor
🕐 10/29/2025, 10:03:40 PM
✓ Status: pending
```

## Why This Happened

Browsers cache JavaScript files for faster loading. When we updated the code, your browser was still using the old cached version.

## Permanent Fix Applied

I've added version parameters to the JavaScript files (`?v=2`), so future updates will automatically load the new version.

## Verify It's Working

1. Clear browser cache (Ctrl + Shift + R)
2. Refresh the dashboard
3. Check the Match Reports section
4. You should see "Library Hall Camera" instead of "cam02"

## Still Showing cam02?

If it's still showing the camera ID after clearing cache:

1. Close all browser windows
2. Reopen browser
3. Go to http://localhost:8080
4. Login again

Or try a different browser to confirm the fix is working.
