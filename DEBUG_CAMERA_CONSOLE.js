// ============================================
// CAMERA SECTION DEBUGGING SCRIPT
// Copy and paste this entire script into your browser console (F12)
// ============================================

console.clear();
console.log('%c🔍 CAMERA SECTION DIAGNOSTIC TOOL', 'font-size: 20px; font-weight: bold; color: #2563eb;');
console.log('%c================================================\n', 'color: #64748b;');

// 1. CHECK CAMERA MANAGER
console.log('%c1️⃣ CAMERA MANAGER STATUS', 'font-size: 16px; font-weight: bold; color: #10b981;');
console.log('   CameraManager exists:', !!window.cameraManager);
console.log('   Cameras loaded:', window.cameraManager?.cameras?.length || 0);
if (window.cameraManager?.cameras) {
    console.log('   Camera details:', window.cameraManager.cameras.map(c => ({
        name: c.name,
        streamUrl: c.streamUrl,
        status: c.status
    })));
}
console.log('');

// 2. CHECK DOM ELEMENTS
console.log('%c2️⃣ DOM ELEMENTS CHECK', 'font-size: 16px; font-weight: bold; color: #10b981;');
const camerasView = document.getElementById('camerasView');
const cameraGrid = document.getElementById('cameraGrid');
const addButton = document.getElementById('addCameraBtn');
const sectionHeader = document.querySelector('#camerasView .section-header');

console.log('   camerasView exists:', !!camerasView);
console.log('   cameraGrid exists:', !!cameraGrid);
console.log('   addButton exists:', !!addButton);
console.log('   sectionHeader exists:', !!sectionHeader);
console.log('');

// 3. CHECK VISIBILITY
console.log('%c3️⃣ VISIBILITY STATUS', 'font-size: 16px; font-weight: bold; color: #10b981;');
if (camerasView) {
    const viewStyles = window.getComputedStyle(camerasView);
    console.log('   📺 camerasView:');
    console.log('      ├─ Has "active" class:', camerasView.classList.contains('active'));
    console.log('      ├─ display:', viewStyles.display);
    console.log('      ├─ visibility:', viewStyles.visibility);
    console.log('      ├─ opacity:', viewStyles.opacity);
    console.log('      └─ Is visible:', viewStyles.display !== 'none' && viewStyles.visibility !== 'hidden');
} else {
    console.log('   ❌ camerasView NOT FOUND');
}
console.log('');

if (addButton) {
    const btnStyles = window.getComputedStyle(addButton);
    const rect = addButton.getBoundingClientRect();
    console.log('   🔘 addButton:');
    console.log('      ├─ display:', btnStyles.display);
    console.log('      ├─ visibility:', btnStyles.visibility);
    console.log('      ├─ opacity:', btnStyles.opacity);
    console.log('      ├─ Position:', { top: rect.top, left: rect.left, width: rect.width, height: rect.height });
    console.log('      ├─ In viewport:', rect.top >= 0 && rect.left >= 0 && rect.bottom <= window.innerHeight && rect.right <= window.innerWidth);
    console.log('      └─ Is visible:', btnStyles.display !== 'none' && btnStyles.visibility !== 'hidden' && rect.width > 0 && rect.height > 0);
} else {
    console.log('   ❌ addButton NOT FOUND');
}
console.log('');

if (cameraGrid) {
    const gridStyles = window.getComputedStyle(cameraGrid);
    console.log('   📊 cameraGrid:');
    console.log('      ├─ display:', gridStyles.display);
    console.log('      ├─ visibility:', gridStyles.visibility);
    console.log('      ├─ innerHTML length:', cameraGrid.innerHTML.length);
    console.log('      ├─ Children count:', cameraGrid.children.length);
    console.log('      └─ Is visible:', gridStyles.display !== 'none' && gridStyles.visibility !== 'hidden');
} else {
    console.log('   ❌ cameraGrid NOT FOUND');
}
console.log('');

// 4. CHECK PARENT CHAIN
console.log('%c4️⃣ PARENT CHAIN ANALYSIS', 'font-size: 16px; font-weight: bold; color: #10b981;');
if (camerasView) {
    let parent = camerasView.parentElement;
    let level = 1;
    while (parent && level <= 5) {
        const styles = window.getComputedStyle(parent);
        const isHidden = styles.display === 'none' || styles.visibility === 'hidden';
        console.log(`   Level ${level}: ${parent.tagName}${parent.id ? '#' + parent.id : ''}${parent.className ? '.' + parent.className.split(' ').join('.') : ''}`);
        console.log(`      ├─ display: ${styles.display}`);
        console.log(`      ├─ visibility: ${styles.visibility}`);
        console.log(`      └─ ${isHidden ? '❌ HIDDEN!' : '✅ Visible'}`);
        parent = parent.parentElement;
        level++;
    }
} else {
    console.log('   ❌ Cannot check - camerasView not found');
}
console.log('');

// 5. CHECK ALL VIEWS
console.log('%c5️⃣ ALL VIEWS STATUS', 'font-size: 16px; font-weight: bold; color: #10b981;');
const allViews = document.querySelectorAll('.view');
allViews.forEach(view => {
    const styles = window.getComputedStyle(view);
    const isActive = view.classList.contains('active');
    const isVisible = styles.display !== 'none';
    console.log(`   ${isActive ? '✅' : '⬜'} ${view.id}:`, {
        active: isActive,
        display: styles.display,
        visible: isVisible
    });
});
console.log('');

// 6. CHECK NAVIGATION
console.log('%c6️⃣ NAVIGATION STATUS', 'font-size: 16px; font-weight: bold; color: #10b981;');
console.log('   App exists:', !!window.app);
console.log('   Current view:', window.app?.currentView || 'unknown');
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    const page = link.getAttribute('data-page');
    const isActive = link.classList.contains('active');
    console.log(`   ${isActive ? '✅' : '⬜'} ${page}`);
});
console.log('');

// 7. RECOMMENDATIONS
console.log('%c7️⃣ RECOMMENDATIONS', 'font-size: 16px; font-weight: bold; color: #f59e0b;');
const issues = [];

if (!camerasView) {
    issues.push('❌ CRITICAL: camerasView element not found in DOM');
} else if (!camerasView.classList.contains('active')) {
    issues.push('⚠️ camerasView is not active - click "Cameras" in navigation');
} else if (window.getComputedStyle(camerasView).display === 'none') {
    issues.push('❌ CRITICAL: camerasView has display:none even though it has active class');
}

if (!addButton) {
    issues.push('❌ CRITICAL: addButton element not found in DOM');
} else {
    const rect = addButton.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) {
        issues.push('⚠️ addButton has zero dimensions - parent might be hidden');
    }
}

if (!cameraGrid) {
    issues.push('❌ CRITICAL: cameraGrid element not found in DOM');
} else if (cameraGrid.children.length === 0) {
    issues.push('⚠️ cameraGrid has no children - cameras might not be rendered');
}

if (!window.cameraManager) {
    issues.push('❌ CRITICAL: CameraManager not initialized');
} else if (!window.cameraManager.cameras || window.cameraManager.cameras.length === 0) {
    issues.push('⚠️ No cameras loaded - check API connection');
}

if (issues.length === 0) {
    console.log('%c   ✅ No issues detected! Everything looks good.', 'color: #10b981;');
} else {
    console.log('%c   Issues found:', 'color: #ef4444; font-weight: bold;');
    issues.forEach(issue => console.log(`   ${issue}`));
}
console.log('');

// 8. QUICK FIXES
console.log('%c8️⃣ QUICK FIX COMMANDS', 'font-size: 16px; font-weight: bold; color: #8b5cf6;');
console.log('   Run these commands to try fixing issues:\n');
console.log('   // Navigate to cameras view:');
console.log('   window.app?.navigateTo("cameras");\n');
console.log('   // Manually load cameras:');
console.log('   window.cameraManager?.loadCameras();\n');
console.log('   // Force show camerasView:');
console.log('   document.getElementById("camerasView")?.classList.add("active");\n');
console.log('   // Check if button is clickable:');
console.log('   document.getElementById("addCameraBtn")?.click();\n');

console.log('%c================================================', 'color: #64748b;');
console.log('%c✅ DIAGNOSTIC COMPLETE', 'font-size: 16px; font-weight: bold; color: #10b981;');
console.log('%cIf issues persist, share this output with your developer.\n', 'color: #64748b;');
