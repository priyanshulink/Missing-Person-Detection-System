/**
 * Authentication Middleware
 * Handles JWT verification and role-based authorization
 */

const jwt = require('jsonwebtoken');
const User = require('../models/User');

/**
 * Authenticate user via JWT token
 */
const authenticate = async (req, res, next) => {
  try {
    // Get token from header
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        error: 'No token provided'
      });
    }
    
    const token = authHeader.substring(7);
    
    // Verify token
    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET || 'default_secret'
    );
    
    // Check if user exists and is active
    const user = await User.findById(decoded.userId);
    
    if (!user || !user.isActive) {
      return res.status(401).json({
        error: 'Invalid token or user inactive'
      });
    }
    
    // Attach user info to request
    req.user = {
      userId: decoded.userId,
      role: decoded.role
    };
    
    next();
    
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        error: 'Invalid token'
      });
    }
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        error: 'Token expired'
      });
    }
    
    console.error('Authentication error:', error);
    res.status(500).json({
      error: 'Authentication failed'
    });
  }
};

/**
 * Authorize user based on roles
 */
const authorize = (roles = []) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        error: 'Not authenticated'
      });
    }
    
    if (roles.length && !roles.includes(req.user.role)) {
      return res.status(403).json({
        error: 'Insufficient permissions'
      });
    }
    
    next();
  };
};

module.exports = {
  authenticate,
  authorize
};
