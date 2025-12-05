/**
 * Real-time Alerts Module
 * Handles Socket.io connections and real-time notifications
 */

class AlertsManager {
    constructor() {
        this.alerts = [];
        this.socket = null;
    }

    init() {
        if (!authManager.isAuthenticated()) {
            return;
        }

        this.connectSocket();
        this.renderAlerts();
    }

    connectSocket() {
        // Connect to Socket.io server
        this.socket = io(CONFIG.SOCKET_URL, {
            transports: ['websocket', 'polling']
        });

        this.socket.on('connect', () => {
            console.log('Socket.io connected');
            this.socket.emit('subscribe', { userId: authManager.getUser()?.id });
        });

        this.socket.on('disconnect', () => {
            console.log('Socket.io disconnected');
        });

        // Listen for match_found events
        this.socket.on('match_found', (data) => {
            console.log('Match found:', data);
            this.addAlert(data);
            this.updateAlertBadge();
            this.showNotification(data);
        });

        // Store socket globally for cleanup
        window.socket = this.socket;
    }

    addAlert(data) {
        const alert = {
            id: Date.now(),
            type: 'match_found',
            title: 'Person Identified',
            message: `${data.personName} detected with ${(data.similarity * 100).toFixed(1)}% similarity`,
            cameraId: data.cameraId,
            cameraName: data.cameraName || 'Unknown Camera',
            cameraLocation: data.cameraLocation || 'Unknown Location',
            timestamp: data.timestamp || new Date().toISOString(),
            data: data
        };

        this.alerts.unshift(alert);
        
        // Keep only last 50 alerts
        if (this.alerts.length > 50) {
            this.alerts = this.alerts.slice(0, 50);
        }

        this.renderAlerts();
    }

    renderAlerts() {
        const alertsList = document.getElementById('alertsList');
        
        if (!this.alerts || this.alerts.length === 0) {
            alertsList.innerHTML = '<p class="no-data">No alerts</p>';
            return;
        }

        alertsList.innerHTML = this.alerts.map(alert => `
            <div class="alert-item ${alert.data?.priority === 'critical' ? 'critical' : ''}">
                <div class="alert-header">
                    <div class="alert-title">
                        <i class="fas fa-bell"></i> ${alert.title}
                    </div>
                    <div class="alert-time">
                        ${this.formatDate(alert.timestamp)}
                    </div>
                </div>
                <div class="alert-body">
                    ${alert.message}
                    <br>
                    <small>
                        <i class="fas fa-video"></i> <strong>${alert.cameraName}</strong>
                        <br>
                        <i class="fas fa-map-marker-alt"></i> ${alert.cameraLocation}
                    </small>
                </div>
            </div>
        `).join('');
    }

    updateAlertBadge() {
        const badge = document.getElementById('alertBadge');
        if (badge) {
            badge.textContent = this.alerts.length;
        }
    }

    showNotification(data) {
        // Browser notification
        if ('Notification' in window && Notification.permission === 'granted') {
            const cameraLocation = data.cameraLocation || 'Unknown Location';
            new Notification('Person Identified', {
                body: `${data.personName} detected with ${(data.similarity * 100).toFixed(1)}% similarity at ${cameraLocation}`,
                icon: '/favicon.ico',
                tag: data.reportId
            });
        }

        // Play sound (optional)
        this.playNotificationSound();
    }

    playNotificationSound() {
        // Create and play a simple notification sound
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = 800;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            console.error('Error playing sound:', error);
        }
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;

        // Less than 1 minute
        if (diff < 60000) {
            return 'Just now';
        }

        // Less than 1 hour
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        }

        // Less than 24 hours
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        }

        // More than 24 hours
        return date.toLocaleString();
    }

    clearAlerts() {
        this.alerts = [];
        this.renderAlerts();
        this.updateAlertBadge();
    }
}

// Create global instance
const alertsManager = new AlertsManager();
