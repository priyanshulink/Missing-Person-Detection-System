/**
 * Person Model
 * Stores information about missing/found persons
 */

const mongoose = require('mongoose');

const personSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true
  },
  age: {
    type: Number,
    min: 0,
    max: 150
  },
  gender: {
    type: String,
    enum: ['male', 'female', 'other'],
    default: 'other'
  },
  status: {
    type: String,
    enum: ['missing', 'found', 'active'],
    default: 'missing'
  },
  description: {
    type: String,
    trim: true
  },
  lastSeenLocation: {
    type: String,
    trim: true
  },
  lastSeenDate: {
    type: Date
  },
  contactInfo: {
    phone: String,
    email: String,
    address: String
  },
  faceEncodings: [{
    encoding: {
      type: [Number],
      required: true
    },
    uploadedAt: {
      type: Date,
      default: Date.now
    },
    imageUrl: String
  }],
  photos: [{
    url: String,
    uploadedAt: {
      type: Date,
      default: Date.now
    }
  }],
  reportedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  priority: {
    type: String,
    enum: ['low', 'medium', 'high', 'critical'],
    default: 'medium'
  },
  tags: [{
    type: String,
    trim: true
  }],
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
  isActive: {
    type: Boolean,
    default: true
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
personSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

// Index for faster searches
personSchema.index({ name: 'text', description: 'text' });
personSchema.index({ status: 1, isActive: 1 });
personSchema.index({ createdAt: -1 });

module.exports = mongoose.model('Person', personSchema);
