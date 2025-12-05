// Camera Management
class CameraManager {
    constructor() {
        this.cameras = [];
        this.initEventListeners();
        // Don't load cameras immediately - wait for view to be active
        // loadCameras() will be called by app.js when navigating to cameras view
    }

    initEventListeners() {
        console.log('🔧 Initializing CameraManager event listeners...');
        
        // Add Camera Button
        const addButton = document.getElementById('addCameraBtn');
        const camerasView = document.getElementById('camerasView');
        
        console.log('📍 Add Camera Button:', addButton);
        console.log('📍 Cameras View:', camerasView);
        console.log('📍 Cameras View Active:', camerasView?.classList.contains('active'));
        console.log('📍 Cameras View Display:', camerasView ? window.getComputedStyle(camerasView).display : 'N/A');
        
        if (addButton) {
            addButton.addEventListener('click', (e) => {
                console.log('🖱️ Add Camera button clicked');
                this.showAddCameraModal();
            });
            
            // Log button visibility details
            const buttonStyles = window.getComputedStyle(addButton);
            console.log('🔍 Button Styles:', {
                display: buttonStyles.display,
                visibility: buttonStyles.visibility,
                opacity: buttonStyles.opacity,
                position: buttonStyles.position,
                zIndex: buttonStyles.zIndex
            });
            
            const rect = addButton.getBoundingClientRect();
            console.log('🔍 Button Position:', {
                top: rect.top,
                left: rect.left,
                width: rect.width,
                height: rect.height,
                inViewport: rect.top >= 0 && rect.left >= 0 && rect.bottom <= window.innerHeight && rect.right <= window.innerWidth
            });
        } else {
            console.error('❌ Add Camera button not found in the DOM');
        }

        // Save Camera Form
        document.getElementById('saveCameraBtn')?.addEventListener('click', (e) => {
            e.preventDefault();
            this.saveCamera();
        });

        // Test Camera Connection
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('test-camera-btn')) {
                const cameraId = e.target.dataset.id;
                this.testCameraConnection(cameraId);
            } else if (e.target.classList.contains('delete-camera-btn')) {
                const cameraId = e.target.dataset.id;
                if (confirm('Are you sure you want to delete this camera?')) {
                    this.deleteCamera(cameraId);
                }
            }
        });
    }

    async loadCameras() {
        try {
            console.log('📹 Loading cameras...');
            
            // Ensure the cameras view and button are visible
            this.ensureViewVisible();
            
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/cameras`);
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Cameras data:', data);
            
            if (data && Array.isArray(data.cameras)) {
                this.cameras = data.cameras;
                console.log(`✅ Loaded ${this.cameras.length} cameras`);
                this.renderCameras();
                this.updateStats();
            } else {
                console.error('Invalid cameras data format:', data);
                throw new Error('Invalid cameras data format');
            }
        } catch (error) {
            console.error('ERROR: Failed to load cameras', error);
            showNotification(`Failed to load cameras: ${error.message}`, 'error');
        }
    }

    ensureViewVisible() {
        console.log('🔍 Ensuring cameras view is visible...');
        
        const camerasView = document.getElementById('camerasView');
        const addButton = document.getElementById('addCameraBtn');
        const cameraGrid = document.getElementById('cameraGrid');
        
        if (camerasView) {
            // Make sure the view is active
            if (!camerasView.classList.contains('active')) {
                console.log('⚠️ Cameras view not active, activating...');
                camerasView.classList.add('active');
            }
            console.log('✅ Cameras view is active');
        }
        
        if (addButton) {
            console.log('✅ Add Camera button found and should be visible');
            console.log('   Button display:', window.getComputedStyle(addButton).display);
            console.log('   Button position:', addButton.getBoundingClientRect());
        } else {
            console.error('❌ Add Camera button NOT found!');
        }
        
        if (cameraGrid) {
            console.log('✅ Camera grid found');
        }
    }

    renderCameras() {
        console.log('\n🎬 === renderCameras called ===');
        const cameraGrid = document.getElementById('cameraGrid');
        const camerasView = document.getElementById('camerasView');
        const addButton = document.getElementById('addCameraBtn');
        const sectionHeader = document.querySelector('#camerasView .section-header');
        
        // Detailed element checks
        console.log('📦 Camera grid element:', cameraGrid);
        console.log('📦 Camera grid parent:', cameraGrid?.parentElement?.id);
        console.log('📦 Cameras view element:', camerasView);
        console.log('📦 Section header:', sectionHeader);
        console.log('📦 Add button element:', addButton);
        
        // Visibility checks
        console.log('\n👁️ VISIBILITY CHECKS:');
        console.log('  ├─ Cameras view active class:', camerasView?.classList.contains('active'));
        console.log('  ├─ Cameras view display:', camerasView ? window.getComputedStyle(camerasView).display : 'N/A');
        console.log('  ├─ Camera grid display:', cameraGrid ? window.getComputedStyle(cameraGrid).display : 'N/A');
        console.log('  ├─ Section header display:', sectionHeader ? window.getComputedStyle(sectionHeader).display : 'N/A');
        console.log('  └─ Add button display:', addButton ? window.getComputedStyle(addButton).display : 'N/A');
        
        // Check all parent visibility
        if (camerasView) {
            let parent = camerasView.parentElement;
            let level = 1;
            console.log('\n🔗 PARENT CHAIN:');
            while (parent && level <= 5) {
                const styles = window.getComputedStyle(parent);
                console.log(`  Level ${level}: ${parent.tagName}#${parent.id || 'no-id'}.${parent.className}`);
                console.log(`    └─ display: ${styles.display}, visibility: ${styles.visibility}`);
                parent = parent.parentElement;
                level++;
            }
        }
        
        console.log('\n📊 Number of cameras:', this.cameras.length);
        
        if (!cameraGrid) {
            console.error('❌ Camera grid element not found!');
            return;
        }

        if (this.cameras.length === 0) {
            console.log('⚠️ No cameras to display');
            cameraGrid.innerHTML = '<p class="no-data">No cameras configured. Click "Add Camera" to get started.</p>';
            return;
        }
        
        console.log('📹 Cameras to render:', this.cameras);

        cameraGrid.innerHTML = this.cameras.map((camera, index) => {
            console.log(`Rendering camera ${index + 1}:`, camera.name, camera.streamUrl);
            
            // Process stream URL to handle common issues
            let streamUrl = camera.streamUrl || '';
            let showVideo = false;
            
            // Validate stream URL is not just a number or invalid string
            if (streamUrl && streamUrl !== '0' && streamUrl.length > 5) {
                // Convert https to http for local IPs to avoid certificate issues
                if (streamUrl.match(/^https?:\/\/(\d{1,3}\.){3}\d{1,3}/)) {
                    streamUrl = streamUrl.replace('https://', 'http://');
                }
                
                // Check if it's a valid URL
                try {
                    const url = new URL(streamUrl);
                    showVideo = url.protocol.startsWith('http');
                    console.log(`Camera ${camera.name}: Valid URL, showVideo=${showVideo}`);
                } catch (e) {
                    console.warn(`Camera ${camera.name}: Invalid stream URL:`, streamUrl);
                    streamUrl = ''; // Reset to empty to show placeholder
                }
            } else {
                console.warn(`Camera ${camera.name}: Invalid or missing stream URL:`, streamUrl);
                streamUrl = ''; // Reset to empty to show placeholder
            }
            
            return `
            <div class="camera-card" data-id="${camera._id}">
                <div class="camera-preview">
                    <div class="camera-status ${camera.status === 'active' ? 'online' : 'offline'}">
                        ${camera.status === 'active' ? 'Online' : 'Offline'}
                    </div>
                    ${showVideo ? 
                        `<img src="${streamUrl}" 
                              alt="${camera.name}" 
                              onerror="this.onerror=null; this.parentElement.innerHTML = 
                                '<div class=\'camera-placeholder\'><i class=\'fas fa-wifi-slash\'></i><p>Stream Unavailable</p></div>'"
                              loading="lazy">` :
                        `<div class="camera-placeholder">
                            <i class="fas fa-video-slash"></i>
                            <p>${streamUrl ? 'Invalid stream URL' : 'No stream URL'}</p>
                        </div>`
                    }
                </div>
                <div class="camera-info">
                    <h3>${camera.name}</h3>
                    <p><i class="fas fa-map-marker-alt"></i> ${camera.location || 'No location'}</p>
                    <p><i class="fas fa-link"></i> ${camera.streamUrl || 'No stream URL'}</p>
                </div>
                <div class="camera-actions">
                    <button class="btn btn-sm btn-secondary test-camera-btn" data-id="${camera._id}">
                        <i class="fas fa-plug"></i> Test
                    </button>
                    <button class="btn btn-sm btn-danger delete-camera-btn" data-id="${camera._id}">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>`;
        }).join('');
        
        console.log('\n✅ Cameras rendered successfully');
        console.log('📏 Camera grid HTML length:', cameraGrid.innerHTML.length);
        console.log('📏 Camera grid children count:', cameraGrid.children.length);
        
        // Final visibility check after render
        console.log('\n🔍 POST-RENDER CHECK:');
        console.log('  ├─ Grid innerHTML exists:', cameraGrid.innerHTML.length > 0);
        console.log('  ├─ Grid has children:', cameraGrid.children.length > 0);
        console.log('  └─ Grid is visible:', window.getComputedStyle(cameraGrid).display !== 'none');
    }

    updateStats() {
        console.log('📊 === UPDATE STATS CALLED ===');
        console.log('📊 Current cameras array:', this.cameras);
        console.log('📊 Cameras length:', this.cameras.length);
        
        const totalCamerasEl = document.getElementById('totalCameras');
        const activeCamerasEl = document.getElementById('activeCameras');
        const inactiveCamerasEl = document.getElementById('inactiveCameras');
        
        console.log('📊 DOM Elements:', {
            totalCamerasEl: !!totalCamerasEl,
            activeCamerasEl: !!activeCamerasEl,
            inactiveCamerasEl: !!inactiveCamerasEl
        });
        
        if (!totalCamerasEl || !activeCamerasEl || !inactiveCamerasEl) {
            console.error('❌ Stats elements not found in DOM!');
            console.log('Checking if camerasView is active:', document.getElementById('camerasView')?.classList.contains('active'));
            return;
        }
        
        // Calculate stats
        const total = this.cameras.length;
        
        // Debug each camera's status
        console.log('📊 Camera statuses:', this.cameras.map(c => ({
            name: c.name,
            status: c.status,
            isActive: c.isActive
        })));
        
        const active = this.cameras.filter(cam => 
            cam.status === 'active' || cam.status === 'online' || cam.isActive === true
        ).length;
        const inactive = total - active;
        
        console.log('📊 Calculated stats:', { total, active, inactive });
        
        // Update DOM
        totalCamerasEl.textContent = total;
        activeCamerasEl.textContent = active;
        inactiveCamerasEl.textContent = inactive;
        
        console.log('📊 DOM updated with values:', {
            total: totalCamerasEl.textContent,
            active: activeCamerasEl.textContent,
            inactive: inactiveCamerasEl.textContent
        });
        
        console.log(`✅ Stats updated: Total=${total}, Active=${active}, Inactive=${inactive}`);
    }

    showAddCameraModal() {
        // Create modal if it doesn't exist
        if (!document.getElementById('addCameraModal')) {
            const modal = document.createElement('div');
            modal.id = 'addCameraModal';
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h2>Add New Camera</h2>
                    <form id="cameraForm">
                        <div class="form-group">
                            <label for="cameraName">Camera Name</label>
                            <input type="text" id="cameraName" required>
                        </div>
                        <div class="form-group">
                            <label for="cameraLocation">Location</label>
                            <input type="text" id="cameraLocation" required>
                        </div>
                        <div class="form-group">
                            <label for="streamUrl">Stream URL</label>
                            <input type="url" id="streamUrl" placeholder="e.g., rtsp:// or http://" required>
                        </div>
                        <div class="form-actions">
                            <button type="button" class="btn btn-secondary" id="cancelCameraBtn">Cancel</button>
                            <button type="submit" class="btn btn-primary" id="saveCameraBtn">Save Camera</button>
                        </div>
                    </form>
                </div>
            `;
            document.body.appendChild(modal);

            // Add event listeners for the new modal
            document.getElementById('cancelCameraBtn').addEventListener('click', () => {
                modal.remove();
            });

            document.getElementById('cameraForm').addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveCamera();
            });
        }

        // Show the modal
        document.getElementById('addCameraModal').style.display = 'flex';
    }

    async saveCamera() {
        const name = document.getElementById('cameraName').value;
        const location = document.getElementById('cameraLocation').value;
        const streamUrl = document.getElementById('streamUrl').value;
        
        if (!name || !location || !streamUrl) {
            showNotification('Please fill in all fields', 'error');
            return;
        }

        // Generate a unique cameraId
        const cameraId = `cam_${Date.now()}`;
        
        const newCamera = {
            name,
            location,
            streamUrl,
            status: 'active',
            description: `${name} camera`,
            isActive: true,
            cameraId: cameraId
        };

        console.log('Saving camera:', newCamera);

        try {
            const token = localStorage.getItem(CONFIG.TOKEN_KEY);
            if (!token) {
                throw new Error('You must be logged in to add a camera');
            }

            const response = await fetch(`${CONFIG.API_BASE_URL}/api/cameras`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(newCamera)
            });

            console.log('Save response status:', response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Error response:', errorData);
                console.error('Response status:', response.status);
                console.error('Response text:', response.statusText);
                
                if (response.status === 401) {
                    throw new Error('Session expired. Please log in again.');
                } else if (response.status === 403) {
                    throw new Error('You do not have permission to add cameras. Your account must have admin or operator role.');
                } else if (response.status === 400) {
                    throw new Error(errorData.error || 'Invalid camera data');
                } else if (response.status === 500) {
                    throw new Error(errorData.error || 'Server error. Please check the server logs for details.');
                } else {
                    throw new Error(errorData.error || errorData.message || `Failed to save camera: ${response.status} ${response.statusText}`);
                }
            }

            const result = await response.json();
            console.log('Save successful:', result);

            // Close modal and refresh list
            const modal = document.getElementById('addCameraModal');
            if (modal) modal.remove();
            
            this.loadCameras();
            showNotification('Camera added successfully', 'success');

        } catch (error) {
            console.error('Error saving camera:', error);
            
            if (error.message.includes('Failed to fetch')) {
                showNotification('Cannot connect to the server. Please check your connection.', 'error');
            } else if (error.message.includes('Session expired')) {
                showNotification('Your session has expired. Please log in again.', 'error');
                // Redirect to login page or show login modal
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 2000);
            } else {
                showNotification(error.message || 'Failed to save camera', 'error');
            }
        }
    }

    async updateCameraStatus(cameraId, status) {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/cameras/${cameraId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem(CONFIG.TOKEN_KEY) || ''}`
                },
                body: JSON.stringify({ status })
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error updating camera status:', errorText);
                throw new Error('Failed to update camera status');
            }

            // Update local state
            const camera = this.cameras.find(c => c._id === cameraId);
            if (camera) {
                camera.status = status;
            }

        } catch (error) {
            console.error('Error updating camera status:', error);
            throw error;
        }
    }

    async testCameraConnection(cameraId) {
        const camera = this.cameras.find(c => c._id === cameraId);
        if (!camera) return;

        const statusElement = document.querySelector(`.camera-card[data-id="${cameraId}"] .camera-status`);
        const testButton = document.querySelector(`.test-camera-btn[data-id="${cameraId}"]`);
        
        if (statusElement && testButton) {
            statusElement.textContent = 'Testing...';
            statusElement.className = 'camera-status testing';
            testButton.disabled = true;
            testButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing';
            
            try {
                // Test the stream URL
                const testImage = new Image();
                testImage.onload = async () => {
                    // Stream is working, update status
                    camera.status = 'active';
                    statusElement.textContent = 'Online';
                    statusElement.className = 'camera-status online';
                    testButton.innerHTML = '<i class="fas fa-sync-alt"></i> Test Again';
                    testButton.disabled = false;
                    
                    // Update status in the backend
                    await this.updateCameraStatus(cameraId, 'active');
                };
                
                testImage.onerror = async () => {
                    // Stream is not working
                    camera.status = 'inactive';
                    statusElement.textContent = 'Offline';
                    statusElement.className = 'camera-status offline';
                    testButton.innerHTML = '<i class="fas fa-sync-alt"></i> Test Again';
                    testButton.disabled = false;
                    
                    // Update status in the backend
                    await this.updateCameraStatus(cameraId, 'inactive');
                };
                
                // Add a timestamp to prevent caching
                testImage.src = `${camera.streamUrl}${camera.streamUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
                
            } catch (error) {
                console.error('Error testing camera:', error);
                statusElement.textContent = 'Error';
                statusElement.className = 'camera-status error';
                testButton.innerHTML = '<i class="fas fa-sync-alt"></i> Test Again';
                testButton.disabled = false;
            }
        }
    }

    async deleteCamera(cameraId) {
        if (!confirm('Are you sure you want to delete this camera?')) {
            return;
        }

        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/cameras/${cameraId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem(CONFIG.TOKEN_KEY) || ''}`
                }
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error deleting camera:', errorText);
                throw new Error('Failed to delete camera');
            }

            // Remove from local state
            this.cameras = this.cameras.filter(camera => camera._id !== cameraId);
            this.renderCameras();
            this.updateStats();
            
            showNotification('Camera deleted successfully', 'success');

        } catch (error) {
            console.error('Error deleting camera:', error);
            showNotification(`Failed to delete camera: ${error.message}`, 'error');
        }
    }
}

// Helper function to show notifications
function showNotification(message, type = 'info') {
    // You can implement a notification system here or use an existing one
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Create a better notification UI instead of alert
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#2563eb'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Initialize CameraManager when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('=== CameraManager Initialization ===');
    
    // Always initialize the CameraManager
    if (!window.cameraManager) {
        window.cameraManager = new CameraManager();
        console.log('CameraManager initialized and ready');
    }
});
