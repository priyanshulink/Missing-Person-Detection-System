/**
 * Report Model
 * Stores match reports when a person is identified
 */

const mongoose = require('mongoose');

const reportSchema = new mongoose.Schema({
  person: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Person',
    required: true
  },
  camera: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Camera'
  },
  matchDetails: {
    similarity: {
      type: Number,
      required: true,
      min: 0,
      max: 1
    },
    confidence: {
      type: Number,
      min: 0,
      max: 1
    },
    faceEncoding: [Number]
  },
  detectionInfo: {
    cameraId: {
      type: String,
      required: true
    },
    cameraName: {
      type: String,
      default: 'Unknown Camera'
    },
    cameraLocation: {
      type: String,
      default: 'Unknown Location'
    },
    timestamp: {
      type: Date,
      required: true
    },
    location: String,
    bbox: {
      x1: Number,
      y1: Number,
      x2: Number,
      y2: Number
    }
  },
  screenshot: {
    url: String,
    uploadedAt: Date
  },
  alertSent: {
    type: Boolean,
    default: false
  },
  alertDetails: {
    sentAt: Date,
    recipients: [String],
    method: {
      type: String,
      enum: ['fcm', 'email', 'sms', 'socket'],
      default: 'socket'
    }
  },
  verificationStatus: {
    type: String,
    enum: ['pending', 'confirmed', 'false_positive'],
    default: 'pending'
  },
  verifiedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  verifiedAt: {
    type: Date
  },
  notes: [{
    content: String,
    addedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    addedAt: {
      type: Date,
      default: Date.now
    }
  }],
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Index for faster queries
reportSchema.index({ person: 1, createdAt: -1 });
reportSchema.index({ 'detectionInfo.cameraId': 1, 'detectionInfo.timestamp': -1 });
reportSchema.index({ verificationStatus: 1 });
reportSchema.index({ createdAt: -1 });

module.exports = mongoose.model('Report', reportSchema);
