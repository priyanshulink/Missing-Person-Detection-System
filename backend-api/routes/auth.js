/**
 * Authentication Routes
 * Handles user registration, login, and token management
 */

const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { authenticate } = require('../middleware/auth');

// Register new user
router.post('/register', async (req, res) => {
  try {
    const { username, email, password, fullName, role } = req.body;
    
    // Validate required fields
    if (!username || !email || !password) {
      return res.status(400).json({
        error: 'Username, email, and password are required'
      });
    }
    
    // Check if user already exists
    const existingUser = await User.findOne({
      $or: [{ email }, { username }]
    });
    
    if (existingUser) {
      return res.status(409).json({
        error: 'User with this email or username already exists'
      });
    }
    
    // Create new user
    const user = new User({
      username,
      email,
      password,
      fullName,
      role: role || 'viewer'
    });
    
    await user.save();
    
    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, role: user.role },
      process.env.JWT_SECRET || 'default_secret',
      { expiresIn: process.env.JWT_EXPIRE || '7d' }
    );
    
    res.status(201).json({
      message: 'User registered successfully',
      token,
      user: user.getPublicProfile()
    });
    
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({
      error: error.message || 'Error registering user'
    });
  }
});

// Login user
router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Validate required fields
    if (!username || !password) {
      return res.status(400).json({
        error: 'Username and password are required'
      });
    }
    
    // Find user by username or email
    const user = await User.findOne({
      $or: [{ username }, { email: username }]
    });
    
    if (!user) {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }
    
    // Check if user is active
    if (!user.isActive) {
      return res.status(403).json({
        error: 'Account is deactivated'
      });
    }
    
    // Verify password
    const isPasswordValid = await user.comparePassword(password);
    
    if (!isPasswordValid) {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }
    
    // Update last login
    user.lastLogin = new Date();
    await user.save();
    
    // Generate JWT token
    const token = jwt.sign(
      { userId: user._id, role: user.role },
      process.env.JWT_SECRET || 'default_secret',
      { expiresIn: process.env.JWT_EXPIRE || '7d' }
    );
    
    res.json({
      message: 'Login successful',
      token,
      user: user.getPublicProfile()
    });
    
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      error: error.message || 'Error logging in'
    });
  }
});

// Get current user profile
router.get('/me', authenticate, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    
    if (!user) {
      return res.status(404).json({
        error: 'User not found'
      });
    }
    
    res.json({
      user: user.getPublicProfile()
    });
    
  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching profile'
    });
  }
});

// Update FCM token
router.post('/fcm-token', authenticate, async (req, res) => {
  try {
    const { fcmToken } = req.body;
    
    if (!fcmToken) {
      return res.status(400).json({
        error: 'FCM token is required'
      });
    }
    
    const user = await User.findById(req.user.userId);
    
    if (!user) {
      return res.status(404).json({
        error: 'User not found'
      });
    }
    
    user.fcmToken = fcmToken;
    await user.save();
    
    res.json({
      message: 'FCM token updated successfully'
    });
    
  } catch (error) {
    console.error('FCM token update error:', error);
    res.status(500).json({
      error: error.message || 'Error updating FCM token'
    });
  }
});

// Logout (client-side token removal, optional server-side tracking)
router.post('/logout', authenticate, async (req, res) => {
  try {
    // Optional: Clear FCM token on logout
    const user = await User.findById(req.user.userId);
    if (user) {
      user.fcmToken = null;
      await user.save();
    }
    
    // Stop surveillance system on logout
    try {
      const surveillanceModule = require('./surveillance');
      const stopped = surveillanceModule.stopProcess();
      if (stopped) {
        console.log('✅ Surveillance stopped on logout');
      }
    } catch (err) {
      console.log('⚠️  Could not stop surveillance on logout:', err.message);
    }
    
    res.json({
      message: 'Logout successful'
    });
    
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({
      error: error.message || 'Error logging out'
    });
  }
});

module.exports = router;
