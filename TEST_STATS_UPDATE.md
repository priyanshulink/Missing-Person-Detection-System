# 🔧 Test Camera Stats Update

## Quick Diagnostic

### Step 1: Open Browser Console (F12)

### Step 2: Run This Command

```javascript
// Check if stats elements exist
console.log('Stats Elements Check:', {
  totalCameras: document.getElementById('totalCameras'),
  activeCameras: document.getElementById('activeCameras'),
  inactiveCameras: document.getElementById('inactiveCameras'),
  camerasView: document.getElementById('camerasView'),
  viewActive: document.getElementById('camerasView')?.classList.contains('active')
});

// Check camera manager
console.log('Camera Manager:', {
  exists: !!window.cameraManager,
  cameras: window.cameraManager?.cameras,
  camerasLength: window.cameraManager?.cameras?.length
});

// Manually trigger update
if (window.cameraManager) {
  window.cameraManager.updateStats();
}
```

### Step 3: Force Navigate and Update

```javascript
// Navigate to cameras and force update
window.app?.navigateTo('cameras');
setTimeout(() => {
  window.cameraManager?.loadCameras();
}, 500);
```

### Step 4: Manually Set Stats (Test)

```javascript
// Manually set stats to verify elements work
document.getElementById('totalCameras').textContent = '99';
document.getElementById('activeCameras').textContent = '88';
document.getElementById('inactiveCameras').textContent = '11';
```

If you can see "99", "88", "11" after running Step 4, the elements exist and work.

## Expected Console Output

After navigating to cameras, you should see:

```
📊 === UPDATE STATS CALLED ===
📊 Current cameras array: [{...}, {...}, ...]
📊 Cameras length: 6
📊 DOM Elements: {totalCamerasEl: true, activeCamerasEl: true, inactiveCamerasEl: true}
📊 Camera statuses: [{name: "...", status: "active", isActive: true}, ...]
📊 Calculated stats: {total: 6, active: 5, inactive: 1}
📊 DOM updated with values: {total: "6", active: "5", inactive: "1"}
✅ Stats updated: Total=6, Active=5, Inactive=1
```

## Common Issues

### Issue 1: Stats elements not found
```
❌ Stats elements not found in DOM!
```

**Cause:** camerasView is not active when updateStats is called

**Fix:** Make sure you navigate to cameras section first:
```javascript
window.app.navigateTo('cameras');
```

### Issue 2: updateStats not called
**Check console for:** `📊 === UPDATE STATS CALLED ===`

**If missing:** The function isn't being called. Manually trigger:
```javascript
window.cameraManager.updateStats();
```

### Issue 3: Stats show 0 but cameras exist
**Check:**
```javascript
console.log('Cameras:', window.cameraManager.cameras);
```

If cameras array is empty, they didn't load. Run:
```javascript
window.cameraManager.loadCameras();
```

## Full Reset Test

```javascript
// Complete reset and reload
window.app.navigateTo('cameras');
setTimeout(() => {
  window.cameraManager.loadCameras().then(() => {
    console.log('Cameras loaded, stats should update');
  });
}, 1000);
```

## Check Stats Visibility

```javascript
// Verify stats section is visible
const statsSection = document.querySelector('.cameras-stats');
console.log('Stats section:', {
  exists: !!statsSection,
  display: statsSection ? getComputedStyle(statsSection).display : 'N/A',
  visible: statsSection ? getComputedStyle(statsSection).display !== 'none' : false
});
```
