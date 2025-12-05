/**
 * Camera Model
 * Stores camera configurations for multi-camera surveillance
 */

const mongoose = require('mongoose');

const cameraSchema = new mongoose.Schema({
  cameraId: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  name: {
    type: String,
    required: true,
    trim: true
  },
  location: {
    type: String,
    required: true,
    trim: true
  },
  streamUrl: {
    type: String,
    required: true,
    trim: true
  },
  status: {
    type: String,
    enum: ['active', 'inactive', 'maintenance'],
    default: 'active'
  },
  resolution: {
    width: {
      type: Number,
      default: 1280
    },
    height: {
      type: Number,
      default: 720
    }
  },
  fps: {
    type: Number,
    default: 30
  },
  description: {
    type: String,
    trim: true
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastOnline: {
    type: Date,
    default: Date.now
  },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

// Update timestamp on save
cameraSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

// Index for faster queries
cameraSchema.index({ cameraId: 1 });
cameraSchema.index({ status: 1, isActive: 1 });
cameraSchema.index({ location: 1 });

module.exports = mongoose.model('Camera', cameraSchema);
