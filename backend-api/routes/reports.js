/**
 * Report Routes
 * Handles match report retrieval and management
 */

const express = require('express');
const router = express.Router();
const Report = require('../models/Report');
const { authenticate, authorize } = require('../middleware/auth');

// Get all reports
router.get('/', authenticate, async (req, res) => {
  try {
    const {
      personId,
      cameraId,
      verificationStatus,
      startDate,
      endDate,
      page = 1,
      limit = 20
    } = req.query;
    
    // Build query
    const query = {};
    
    if (personId) {
      query.person = personId;
    }
    
    if (cameraId) {
      query['detectionInfo.cameraId'] = cameraId;
    }
    
    if (verificationStatus) {
      query.verificationStatus = verificationStatus;
    }
    
    if (startDate || endDate) {
      query['detectionInfo.timestamp'] = {};
      if (startDate) {
        query['detectionInfo.timestamp'].$gte = new Date(startDate);
      }
      if (endDate) {
        query['detectionInfo.timestamp'].$lte = new Date(endDate);
      }
    }
    
    // Execute query with pagination
    const reports = await Report.find(query)
      .populate('person', 'name status priority')
      .populate('camera', 'cameraId name location')
      .populate('verifiedBy', 'username fullName')
      .sort({ 'detectionInfo.timestamp': -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .exec();
    
    // Get total count
    const count = await Report.countDocuments(query);
    
    res.json({
      reports,
      totalPages: Math.ceil(count / limit),
      currentPage: page,
      total: count
    });
    
  } catch (error) {
    console.error('Get reports error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching reports'
    });
  }
});

// Get single report by ID
router.get('/:id', authenticate, async (req, res) => {
  try {
    const report = await Report.findById(req.params.id)
      .populate('person')
      .populate('camera', 'cameraId name location streamUrl')
      .populate('verifiedBy', 'username fullName')
      .populate('notes.addedBy', 'username fullName');
    
    if (!report) {
      return res.status(404).json({
        error: 'Report not found'
      });
    }
    
    res.json({ report });
    
  } catch (error) {
    console.error('Get report error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching report'
    });
  }
});

// Update report verification status
router.patch('/:id/verify', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    const { verificationStatus } = req.body;
    
    if (!['confirmed', 'false_positive'].includes(verificationStatus)) {
      return res.status(400).json({
        error: 'Invalid verification status'
      });
    }
    
    const report = await Report.findById(req.params.id);
    
    if (!report) {
      return res.status(404).json({
        error: 'Report not found'
      });
    }
    
    report.verificationStatus = verificationStatus;
    report.verifiedBy = req.user.userId;
    report.verifiedAt = new Date();
    
    await report.save();
    
    res.json({
      message: 'Report verification updated',
      report
    });
    
  } catch (error) {
    console.error('Verify report error:', error);
    res.status(500).json({
      error: error.message || 'Error verifying report'
    });
  }
});

// Add note to report
router.post('/:id/notes', authenticate, async (req, res) => {
  try {
    const { content } = req.body;
    
    if (!content) {
      return res.status(400).json({
        error: 'Note content is required'
      });
    }
    
    const report = await Report.findById(req.params.id);
    
    if (!report) {
      return res.status(404).json({
        error: 'Report not found'
      });
    }
    
    report.notes.push({
      content,
      addedBy: req.user.userId,
      addedAt: new Date()
    });
    
    await report.save();
    
    res.json({
      message: 'Note added successfully',
      report
    });
    
  } catch (error) {
    console.error('Add note error:', error);
    res.status(500).json({
      error: error.message || 'Error adding note'
    });
  }
});

// Get statistics
router.get('/stats/summary', authenticate, async (req, res) => {
  try {
    const { startDate, endDate } = req.query;
    
    const dateFilter = {};
    if (startDate || endDate) {
      dateFilter['detectionInfo.timestamp'] = {};
      if (startDate) {
        dateFilter['detectionInfo.timestamp'].$gte = new Date(startDate);
      }
      if (endDate) {
        dateFilter['detectionInfo.timestamp'].$lte = new Date(endDate);
      }
    }
    
    const [
      totalReports,
      confirmedReports,
      falsePositives,
      pendingReports,
      reportsPerCamera
    ] = await Promise.all([
      Report.countDocuments(dateFilter),
      Report.countDocuments({ ...dateFilter, verificationStatus: 'confirmed' }),
      Report.countDocuments({ ...dateFilter, verificationStatus: 'false_positive' }),
      Report.countDocuments({ ...dateFilter, verificationStatus: 'pending' }),
      Report.aggregate([
        { $match: dateFilter },
        { $group: { _id: '$detectionInfo.cameraId', count: { $sum: 1 } } },
        { $sort: { count: -1 } }
      ])
    ]);
    
    res.json({
      totalReports,
      confirmedReports,
      falsePositives,
      pendingReports,
      reportsPerCamera
    });
    
  } catch (error) {
    console.error('Get stats error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching statistics'
    });
  }
});

module.exports = router;
