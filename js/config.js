/**
 * Configuration
 */

// Detect if running on GitHub Pages or localhost
const isGitHubPages = window.location.hostname === 'priyanshulink.github.io';

const CONFIG = {
    // Use your deployed backend URL when on GitHub Pages, localhost for development
    API_BASE_URL: isGitHubPages ? 'https://missing-person-detection-system.onrender.com' : 'http://localhost:3000',
    SOCKET_URL: isGitHubPages ? 'https://missing-person-detection-system.onrender.com' : 'http://localhost:3000',
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
