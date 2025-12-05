/**
 * Authentication Module
 */

class AuthManager {
    constructor() {
        this.token = null;
        this.user = null;
    }

    init() {
        // Check if user is already logged in
        this.token = localStorage.getItem(CONFIG.TOKEN_KEY);
        const userData = localStorage.getItem(CONFIG.USER_KEY);
        
        if (this.token && userData) {
            this.user = JSON.parse(userData);
            this.showDashboard();
        } else {
            this.showLogin();
        }
    }

    async login(username, password) {
        try {
            const response = await api.login(username, password);
            
            this.token = response.token;
            this.user = response.user;
            
            // Store in localStorage
            localStorage.setItem(CONFIG.TOKEN_KEY, this.token);
            localStorage.setItem(CONFIG.USER_KEY, JSON.stringify(this.user));
            
            this.showDashboard();
            
            // Initialize dashboard after login
            if (window.dashboardManager) {
                dashboardManager.init();
            }
            
            // Auto-start surveillance on login
            this.startSurveillance();
            
            return true;
        } catch (error) {
            throw error;
        }
    }

    async logout() {
        try {
            // Call backend logout to stop surveillance
            if (this.token) {
                await fetch(`${CONFIG.API_URL}/api/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                        'Content-Type': 'application/json'
                    }
                });
            }
        } catch (error) {
            console.error('Logout API error:', error);
        }
        
        // Clear local data
        this.token = null;
        this.user = null;
        
        localStorage.removeItem(CONFIG.TOKEN_KEY);
        localStorage.removeItem(CONFIG.USER_KEY);
        
        // Disconnect socket
        if (window.socket) {
            socket.disconnect();
        }
        
        console.log('✅ Logged out - Surveillance stopped');
        this.showLogin();
    }

    showLogin() {
        document.getElementById('loginPage').classList.add('active');
        document.getElementById('dashboardPage').classList.remove('active');
    }

    showDashboard() {
        document.getElementById('loginPage').classList.remove('active');
        document.getElementById('dashboardPage').classList.add('active');
        
        // Update user info in navbar
        const userInfo = document.getElementById('userInfo');
        if (userInfo && this.user) {
            userInfo.textContent = this.user.username;
        }
    }

    isAuthenticated() {
        return !!this.token;
    }

    getUser() {
        return this.user;
    }

    startSurveillance() {
        // Trigger surveillance start via API
        fetch(`${CONFIG.API_BASE_URL}/api/surveillance/start`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('✅ Surveillance started:', data.message);
        })
        .catch(error => {
            console.error('⚠️  Could not start surveillance:', error);
        });
    }
}

// Create global instance
const authManager = new AuthManager();

// Login form handler
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            loginError.textContent = '';
            
            try {
                await authManager.login(username, password);
            } catch (error) {
                loginError.textContent = error.message || 'Login failed';
            }
        });
    }
    
    // Logout button handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            authManager.logout();
        });
    }
    
    // Initialize auth
    authManager.init();
});
