/**
 * Camera Routes
 * Handles CRUD operations for camera management
 */

const express = require('express');
const router = express.Router();
const Camera = require('../models/Camera');
const { authenticate, authorize } = require('../middleware/auth');

// Get all cameras (no auth required for surveillance system)
router.get('/', async (req, res) => {
  try {
    const { status, location, active, includeInactive } = req.query;
    
    // Build query
    const query = {};
    
    // By default, only show active cameras unless includeInactive=true
    if (includeInactive !== 'true') {
      query.isActive = true;
    }
    
    if (status) {
      query.status = status;
    }
    
    if (location) {
      query.location = { $regex: location, $options: 'i' };
    }
    
    if (active !== undefined) {
      query.isActive = active === 'true';
    }
    
    const cameras = await Camera.find(query)
      .sort({ createdAt: -1 })
      .exec();
    
    res.json({
      cameras,
      total: cameras.length
    });
    
  } catch (error) {
    console.error('Get cameras error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching cameras'
    });
  }
});

// Get single camera by ID or cameraId
router.get('/:id', async (req, res) => {
  try {
    let camera;
    
    // Try to find by MongoDB _id first
    if (req.params.id.match(/^[0-9a-fA-F]{24}$/)) {
      camera = await Camera.findById(req.params.id);
    }
    
    // If not found, try by cameraId
    if (!camera) {
      camera = await Camera.findOne({ cameraId: req.params.id });
    }
    
    if (!camera) {
      return res.status(404).json({
        error: 'Camera not found'
      });
    }
    
    res.json({ camera });
    
  } catch (error) {
    console.error('Get camera error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching camera'
    });
  }
});

// Create new camera
router.post('/', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    console.log('Creating camera with data:', req.body);
    console.log('User info:', req.user);
    
    const cameraData = {
      ...req.body,
      createdBy: req.user?.userId || 'unknown'
    };
    
    // Validate required fields
    if (!cameraData.name || !cameraData.location || !cameraData.streamUrl) {
      return res.status(400).json({
        error: 'Missing required fields: name, location, and streamUrl are required'
      });
    }
    
    // Check if cameraId already exists
    if (cameraData.cameraId) {
      const existing = await Camera.findOne({ cameraId: cameraData.cameraId });
      if (existing) {
        return res.status(400).json({
          error: 'Camera ID already exists'
        });
      }
    }
    
    const camera = new Camera(cameraData);
    await camera.save();
    
    console.log('Camera created successfully:', camera._id);
    
    res.status(201).json({
      message: 'Camera created successfully',
      camera
    });
    
  } catch (error) {
    console.error('Create camera error:', error);
    console.error('Error stack:', error.stack);
    res.status(500).json({
      error: error.message || 'Error creating camera',
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

// Update camera
router.put('/:id', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    let camera;
    
    // Try to find by MongoDB _id first
    if (req.params.id.match(/^[0-9a-fA-F]{24}$/)) {
      camera = await Camera.findById(req.params.id);
    }
    
    // If not found, try by cameraId
    if (!camera) {
      camera = await Camera.findOne({ cameraId: req.params.id });
    }
    
    if (!camera) {
      return res.status(404).json({
        error: 'Camera not found'
      });
    }
    
    // Update fields
    Object.keys(req.body).forEach(key => {
      if (key !== '_id' && key !== 'createdBy' && key !== 'cameraId') {
        camera[key] = req.body[key];
      }
    });
    
    await camera.save();
    
    res.json({
      message: 'Camera updated successfully',
      camera
    });
    
  } catch (error) {
    console.error('Update camera error:', error);
    res.status(500).json({
      error: error.message || 'Error updating camera'
    });
  }
});

// Delete camera (hard delete - permanently removes from database)
router.delete('/:id', authenticate, authorize(['admin']), async (req, res) => {
  try {
    let camera;
    
    // Try to find by MongoDB _id first
    if (req.params.id.match(/^[0-9a-fA-F]{24}$/)) {
      camera = await Camera.findByIdAndDelete(req.params.id);
    }
    
    // If not found, try by cameraId
    if (!camera) {
      camera = await Camera.findOneAndDelete({ cameraId: req.params.id });
    }
    
    if (!camera) {
      return res.status(404).json({
        error: 'Camera not found'
      });
    }
    
    console.log(`Camera deleted: ${camera.name} (${camera._id})`);
    
    res.json({
      message: 'Camera deleted successfully',
      deletedCamera: {
        id: camera._id,
        name: camera.name
      }
    });
    
  } catch (error) {
    console.error('Delete camera error:', error);
    res.status(500).json({
      error: error.message || 'Error deleting camera'
    });
  }
});

// Update camera status (for heartbeat/monitoring)
router.patch('/:id/status', async (req, res) => {
  try {
    const { status, lastOnline } = req.body;
    
    let camera;
    
    // Try to find by MongoDB _id first
    if (req.params.id.match(/^[0-9a-fA-F]{24}$/)) {
      camera = await Camera.findById(req.params.id);
    }
    
    // If not found, try by cameraId
    if (!camera) {
      camera = await Camera.findOne({ cameraId: req.params.id });
    }
    
    if (!camera) {
      return res.status(404).json({
        error: 'Camera not found'
      });
    }
    
    if (status) {
      camera.status = status;
    }
    
    if (lastOnline) {
      camera.lastOnline = new Date(lastOnline);
    } else {
      camera.lastOnline = new Date();
    }
    
    await camera.save();
    
    res.json({
      message: 'Camera status updated',
      camera
    });
    
  } catch (error) {
    console.error('Update camera status error:', error);
    res.status(500).json({
      error: error.message || 'Error updating camera status'
    });
  }
});

// Get active cameras for surveillance
router.get('/active/list', async (req, res) => {
  try {
    const cameras = await Camera.find({
      isActive: true,
      status: 'active'
    }).select('cameraId name location streamUrl resolution fps');
    
    res.json({
      cameras,
      total: cameras.length
    });
    
  } catch (error) {
    console.error('Get active cameras error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching active cameras'
    });
  }
});

module.exports = router;
