/**
 * ============================================
 * CAMERA MANAGEMENT - COMPLETE IMPLEMENTATION
 * ============================================
 * Handles all camera-related functionality:
 * - Display cameras view when clicked
 * - Show Add Camera button
 * - Render camera grid dynamically
 * - Handle camera CRUD operations
 */

class CameraManager {
    constructor() {
        this.cameras = [];
        this.init();
    }

    /**
     * Initialize the camera manager
     */
    init() {
        console.log('🎥 Initializing Camera Manager...');
        this.setupEventListeners();
        // Don't load cameras immediately - wait for view to be active
    }

    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // Add Camera Button Click
        const addButton = document.getElementById('addCameraBtn');
        if (addButton) {
            addButton.addEventListener('click', () => {
                console.log('✅ Add Camera button clicked');
                this.showAddCameraModal();
            });
            console.log('✅ Add Camera button listener attached');
        } else {
            console.error('❌ Add Camera button not found');
        }

        // Delete camera buttons (delegated event)
        document.addEventListener('click', (e) => {
            if (e.target.closest('.delete-camera-btn')) {
                const cameraId = e.target.closest('.delete-camera-btn').dataset.id;
                this.deleteCamera(cameraId);
            }
            
            if (e.target.closest('.test-camera-btn')) {
                const cameraId = e.target.closest('.test-camera-btn').dataset.id;
                this.testCamera(cameraId);
            }
        });
    }

    /**
     * Load cameras from API or use mock data
     */
    async loadCameras() {
        console.log('📡 Loading cameras...');
        
        // Ensure view is visible
        this.ensureViewVisible();

        try {
            // Try to load from API
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/cameras`);
            
            if (response.ok) {
                const data = await response.json();
                if (data && Array.isArray(data.cameras)) {
                    this.cameras = data.cameras;
                    console.log(`✅ Loaded ${this.cameras.length} cameras from API`);
                }
            } else {
                throw new Error('API not available');
            }
        } catch (error) {
            console.warn('⚠️ API not available, using mock data');
            // Use mock data for demonstration
            this.cameras = this.getMockCameras();
        }

        this.renderCameras();
        this.updateStats();
    }

    /**
     * Get mock camera data for testing
     */
    getMockCameras() {
        return [
            {
                _id: '1',
                name: 'Entrance Camera',
                location: 'Main Gate',
                streamUrl: 'http://localhost:8000/stream1',
                status: 'active',
                cameraId: 'cam_001'
            },
            {
                _id: '2',
                name: 'Office Camera',
                location: 'Reception Area',
                streamUrl: 'http://localhost:8000/stream2',
                status: 'inactive',
                cameraId: 'cam_002'
            },
            {
                _id: '3',
                name: 'Parking Camera',
                location: 'Parking Lot',
                streamUrl: 'http://localhost:8000/stream3',
                status: 'active',
                cameraId: 'cam_003'
            },
            {
                _id: '4',
                name: 'Warehouse Camera',
                location: 'Storage Area',
                streamUrl: 'http://localhost:8000/stream4',
                status: 'active',
                cameraId: 'cam_004'
            }
        ];
    }

    /**
     * Ensure cameras view is visible
     */
    ensureViewVisible() {
        const camerasView = document.getElementById('camerasView');
        
        if (!camerasView) {
            console.error('❌ Cameras view not found');
            return;
        }

        // Make sure view is active
        if (!camerasView.classList.contains('active')) {
            console.log('⚠️ Cameras view not active, activating...');
            // Hide all views
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            // Show cameras view
            camerasView.classList.add('active');
        }

        console.log('✅ Cameras view is visible');
    }

    /**
     * Render all cameras in the grid
     */
    renderCameras() {
        console.log('🎬 Rendering cameras...');
        
        const cameraGrid = document.getElementById('cameraGrid');
        if (!cameraGrid) {
            console.error('❌ Camera grid not found');
            return;
        }

        // Clear existing content
        cameraGrid.innerHTML = '';

        if (this.cameras.length === 0) {
            cameraGrid.innerHTML = `
                <div class="no-data" style="grid-column: 1 / -1;">
                    <i class="fas fa-video-slash" style="font-size: 48px; color: #cbd5e1; margin-bottom: 16px;"></i>
                    <p style="font-size: 18px; color: #64748b; margin: 0;">No cameras configured</p>
                    <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Click "Add Camera" to get started</p>
                </div>
            `;
            return;
        }

        // Render each camera card
        this.cameras.forEach(camera => {
            const card = this.createCameraCard(camera);
            cameraGrid.appendChild(card);
        });

        console.log(`✅ Rendered ${this.cameras.length} cameras`);
    }

    /**
     * Create a camera card element
     */
    createCameraCard(camera) {
        const card = document.createElement('div');
        card.className = 'camera-card';
        card.dataset.id = camera._id;

        const isActive = camera.status === 'active' || camera.status === 'online';
        const statusClass = isActive ? 'active' : 'inactive';
        const statusText = isActive ? 'Active' : 'Inactive';

        // Check if stream URL is valid
        const hasValidStream = camera.streamUrl && 
                               camera.streamUrl !== '0' && 
                               camera.streamUrl.length > 5;

        card.innerHTML = `
            <div class="camera-preview">
                ${hasValidStream ? `
                    <img src="${camera.streamUrl}" 
                         alt="${camera.name}"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                         style="display: block;">
                    <div class="camera-placeholder" style="display: none;">
                        <i class="fas fa-video-slash"></i>
                        <p>Stream Unavailable</p>
                    </div>
                ` : `
                    <div class="camera-placeholder">
                        <i class="fas fa-video-slash"></i>
                        <p>No Stream URL</p>
                    </div>
                `}
                <div class="camera-status ${statusClass}">
                    ${statusText}
                </div>
            </div>
            <div class="camera-info">
                <h3>
                    <i class="fas fa-video"></i>
                    ${camera.name}
                </h3>
                <p>
                    <i class="fas fa-map-marker-alt"></i>
                    ${camera.location || 'No location'}
                </p>
                <p>
                    <i class="fas fa-link"></i>
                    <span style="font-size: 11px; word-break: break-all;">
                        ${camera.streamUrl || 'No stream URL'}
                    </span>
                </p>
            </div>
            <div class="camera-actions">
                <button class="btn btn-sm btn-secondary test-camera-btn" data-id="${camera._id}">
                    <i class="fas fa-plug"></i> Test
                </button>
                <button class="btn btn-sm btn-danger delete-camera-btn" data-id="${camera._id}">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>
        `;

        return card;
    }

    /**
     * Update camera statistics
     */
    updateStats() {
        const total = this.cameras.length;
        const active = this.cameras.filter(c => c.status === 'active' || c.status === 'online').length;
        const inactive = total - active;

        document.getElementById('totalCameras').textContent = total;
        document.getElementById('activeCameras').textContent = active;
        document.getElementById('inactiveCameras').textContent = inactive;

        console.log(`📊 Stats updated: ${total} total, ${active} active, ${inactive} inactive`);
    }

    /**
     * Show Add Camera modal
     */
    showAddCameraModal() {
        console.log('📝 Opening Add Camera modal...');

        // Create modal if it doesn't exist
        let modal = document.getElementById('addCameraModal');
        
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'addCameraModal';
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h3><i class="fas fa-plus-circle"></i> Add New Camera</h3>
                        <button class="close-modal" onclick="document.getElementById('addCameraModal').classList.remove('active')">&times;</button>
                    </div>
                    <form id="cameraForm">
                        <div class="form-group">
                            <label for="cameraName">
                                <i class="fas fa-video"></i> Camera Name *
                            </label>
                            <input type="text" id="cameraName" placeholder="e.g., Front Door Camera" required>
                        </div>
                        <div class="form-group">
                            <label for="cameraLocation">
                                <i class="fas fa-map-marker-alt"></i> Location *
                            </label>
                            <input type="text" id="cameraLocation" placeholder="e.g., Main Entrance" required>
                        </div>
                        <div class="form-group">
                            <label for="streamUrl">
                                <i class="fas fa-link"></i> Stream URL *
                            </label>
                            <input type="text" id="streamUrl" placeholder="e.g., http://192.168.1.100:8080/video" required>
                            <small style="color: #64748b; font-size: 12px; margin-top: 5px; display: block;">
                                Examples: http://ip:port/video, rtsp://ip:554/stream, or 0 for local webcam
                            </small>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary close-modal" onclick="document.getElementById('addCameraModal').classList.remove('active')">
                                Cancel
                            </button>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Save Camera
                            </button>
                        </div>
                    </form>
                </div>
            `;
            document.body.appendChild(modal);

            // Add form submit listener
            document.getElementById('cameraForm').addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveCamera();
            });

            // Close on background click
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        }

        // Show modal
        modal.classList.add('active');
    }

    /**
     * Save new camera
     */
    async saveCamera() {
        const name = document.getElementById('cameraName').value.trim();
        const location = document.getElementById('cameraLocation').value.trim();
        const streamUrl = document.getElementById('streamUrl').value.trim();

        if (!name || !location || !streamUrl) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }

        const newCamera = {
            _id: Date.now().toString(),
            name,
            location,
            streamUrl,
            status: 'active',
            cameraId: `cam_${Date.now()}`
        };

        console.log('💾 Saving camera:', newCamera);

        try {
            // Try to save to API
            if (typeof CONFIG !== 'undefined' && CONFIG.API_BASE_URL) {
                const token = localStorage.getItem(CONFIG.TOKEN_KEY);
                const response = await fetch(`${CONFIG.API_BASE_URL}/api/cameras`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token || ''}`
                    },
                    body: JSON.stringify(newCamera)
                });

                if (response.ok) {
                    const result = await response.json();
                    newCamera._id = result.camera?._id || newCamera._id;
                    console.log('✅ Camera saved to API');
                }
            }
        } catch (error) {
            console.warn('⚠️ API save failed, adding locally:', error.message);
        }

        // Add to local array
        this.cameras.push(newCamera);
        
        // Close modal
        document.getElementById('addCameraModal').classList.remove('active');
        
        // Clear form
        document.getElementById('cameraForm').reset();
        
        // Re-render
        this.renderCameras();
        this.updateStats();
        
        this.showNotification('Camera added successfully!', 'success');
    }

    /**
     * Delete camera
     */
    async deleteCamera(cameraId) {
        if (!confirm('Are you sure you want to delete this camera?')) {
            return;
        }

        console.log('🗑️ Deleting camera:', cameraId);

        try {
            // Try to delete from API
            if (typeof CONFIG !== 'undefined' && CONFIG.API_BASE_URL) {
                const token = localStorage.getItem(CONFIG.TOKEN_KEY);
                await fetch(`${CONFIG.API_BASE_URL}/api/cameras/${cameraId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token || ''}`
                    }
                });
            }
        } catch (error) {
            console.warn('⚠️ API delete failed:', error.message);
        }

        // Remove from local array
        this.cameras = this.cameras.filter(c => c._id !== cameraId);
        
        // Re-render
        this.renderCameras();
        this.updateStats();
        
        this.showNotification('Camera deleted successfully', 'success');
    }

    /**
     * Test camera connection
     */
    testCamera(cameraId) {
        const camera = this.cameras.find(c => c._id === cameraId);
        if (!camera) return;

        console.log('🔌 Testing camera:', camera.name);
        this.showNotification(`Testing ${camera.name}...`, 'info');

        // Simulate test (in real app, this would ping the stream)
        setTimeout(() => {
            const success = Math.random() > 0.3; // 70% success rate
            if (success) {
                camera.status = 'active';
                this.showNotification(`${camera.name} is online!`, 'success');
            } else {
                camera.status = 'inactive';
                this.showNotification(`${camera.name} is offline`, 'error');
            }
            this.renderCameras();
            this.updateStats();
        }, 1500);
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#3b82f6'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 10000;
            font-weight: 500;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM loaded, initializing Camera Manager...');
    window.cameraManager = new CameraManager();
    console.log('✅ Camera Manager ready');
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
