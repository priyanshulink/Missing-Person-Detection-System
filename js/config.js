/**
 * Configuration
 */

// Detect if running on GitHub Pages or localhost
const isGitHubPages = window.location.hostname === 'priyanshulink.github.io';

const CONFIG = {
    // Use production Render backend for both GitHub Pages and local testing
    // Change this back to http://localhost:3000 if you want to run backend locally
    API_BASE_URL: 'https://missing-person-detection-system.onrender.com',
    SOCKET_URL: 'https://missing-person-detection-system.onrender.com',
    TOKEN_KEY: 'auth_token',
    USER_KEY: 'user_data'
};

// Note: For GitHub Pages to work fully, you need to deploy your backend-api to a cloud service like:
// - Heroku (free tier)
// - Railway.app
// - Render.com
// - Vercel
// - AWS/Azure/GCP
// Then replace 'https://your-backend-url.com' with your actual backend URL
