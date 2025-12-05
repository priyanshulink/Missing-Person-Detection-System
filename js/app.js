/**
 * Main Application
 * Initializes all modules and handles navigation
 */

class App {
    constructor() {
        this.currentView = 'dashboard';
    }

    init() {
        this.setupNavigation();
        this.initializeModules();
        this.requestNotificationPermission();
    }

    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const page = link.getAttribute('data-page');
                this.navigateTo(page);
                
                // Update active link
                navLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }

    navigateTo(page) {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });

        // Show selected view
        const viewMap = {
            'dashboard': 'dashboardView',
            'persons': 'personsView',
            'reports': 'reportsView',
            'alerts': 'alertsView',
            'cameras': 'camerasView'
        };

        const viewId = viewMap[page];
        if (viewId) {
            document.getElementById(viewId).classList.add('active');
            this.currentView = page;
            
            // Initialize view-specific functionality
            this.initializeView(page);
        }
    }

    initializeView(page) {
        switch(page) {
            case 'dashboard':
                if (dashboardManager) {
                    dashboardManager.init();
                }
                break;
            case 'persons':
                if (personsManager) {
                    personsManager.init();
                }
                break;
            case 'reports':
                if (reportsManager) {
                    reportsManager.init();
                }
                break;
            case 'alerts':
                if (alertsManager) {
                    alertsManager.init();
                }
                break;
            case 'cameras':
                if (window.cameraManager) {
                    window.cameraManager.loadCameras();
                }
                break;
        }
    }

    initializeModules() {
        // Initialize modules only if authenticated
        if (authManager.isAuthenticated()) {
            // Initialize dashboard by default
            if (dashboardManager) {
                dashboardManager.init();
            }
            
            // Initialize alerts manager for real-time updates
            if (alertsManager) {
                alertsManager.init();
            }
        }
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            setTimeout(() => {
                Notification.requestPermission().then(permission => {
                    console.log('Notification permission:', permission);
                });
            }, 2000);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    
    // Wait for auth to initialize first
    setTimeout(() => {
        if (authManager.isAuthenticated()) {
            app.init();
        }
    }, 100);
    
    // Store app globally
    window.app = app;
});
