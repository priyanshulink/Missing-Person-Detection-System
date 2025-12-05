/**
 * Backend API Server
 * Node.js + Express backend for person identification system
 */

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const http = require('http');
const socketIo = require('socket.io');
require('dotenv').config();

// Import routes
const authRoutes = require('./routes/auth');
const personRoutes = require('./routes/persons');
const recognitionRoutes = require('./routes/recognition');
const reportRoutes = require('./routes/reports');
const uploadRoutes = require('./routes/upload');
const surveillanceRoutes = require('./routes/surveillance');
const cameraRoutes = require('./routes/cameras');

// Import services (Firebase optional for notifications only)
const { initializeFirebase } = require('./services/firebase');

// Initialize Express app
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(morgan('combined'));

// Make io accessible to routes
app.set('io', io);

// MongoDB connection
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/person_detection';

mongoose.connect(MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log('✅ Connected to MongoDB');
})
.catch((err) => {
  console.error('❌ MongoDB connection error:', err);
  process.exit(1);
});

// Initialize Firebase
try {
  initializeFirebase();
  console.log('✅ Firebase initialized');
} catch (error) {
  console.warn('⚠️  Firebase initialization failed:', error.message);
}

// Socket.io connection handling
io.on('connection', (socket) => {
  console.log('🔌 New client connected:', socket.id);
  
  socket.on('disconnect', () => {
    console.log('🔌 Client disconnected:', socket.id);
  });
  
  socket.on('subscribe', (data) => {
    console.log('📡 Client subscribed:', data);
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/persons', personRoutes);
app.use('/api/recognition', recognitionRoutes);
app.use('/api/reports', reportRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/surveillance', surveillanceRoutes);
// Camera routes (MongoDB based)
app.use('/api/cameras', cameraRoutes);

// Serve uploaded files
app.use('/uploads', express.static('uploads'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    mongodb: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected'
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Person Detection & Identification API',
    version: '1.0.0',
    endpoints: {
      auth: '/api/auth',
      persons: '/api/persons',
      recognition: '/api/recognition',
      reports: '/api/reports',
      health: '/health'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(err.status || 500).json({
    error: {
      message: err.message || 'Internal server error',
      status: err.status || 500
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: {
      message: 'Endpoint not found',
      status: 404
    }
  });
});

// Start server
const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
    mongoose.connection.close(false, () => {
      console.log('MongoDB connection closed');
      process.exit(0);
    });
  });
});

module.exports = { app, io };
