/**
 * Person Routes
 * Handles CRUD operations for missing/found persons
 */

const express = require('express');
const router = express.Router();
const Person = require('../models/Person');
const { authenticate, authorize } = require('../middleware/auth');
const recognitionRouter = require('./recognition');

// Get all persons (no auth required for surveillance system)
router.get('/', async (req, res) => {
  try {
    const {
      status,
      priority,
      search,
      page = 1,
      limit = 20
    } = req.query;
    
    // Build query
    const query = { isActive: true };
    
    if (status) {
      query.status = status;
    }
    
    if (priority) {
      query.priority = priority;
    }
    
    if (search) {
      query.$text = { $search: search };
    }
    
    // Execute query with pagination
    const persons = await Person.find(query)
      .populate('reportedBy', 'username fullName')
      .sort({ createdAt: -1 })
      .limit(limit * 1)
      .skip((page - 1) * limit)
      .exec();
    
    // Get total count
    const count = await Person.countDocuments(query);
    
    res.json({
      persons,
      totalPages: Math.ceil(count / limit),
      currentPage: page,
      total: count
    });
    
  } catch (error) {
    console.error('Get persons error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching persons'
    });
  }
});

// Get single person by ID
router.get('/:id', authenticate, async (req, res) => {
  try {
    const person = await Person.findById(req.params.id)
      .populate('reportedBy', 'username fullName')
      .populate('notes.addedBy', 'username fullName');
    
    if (!person) {
      return res.status(404).json({
        error: 'Person not found'
      });
    }
    
    res.json({ person });
    
  } catch (error) {
    console.error('Get person error:', error);
    res.status(500).json({
      error: error.message || 'Error fetching person'
    });
  }
});

// Create new person
router.post('/', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    const personData = {
      ...req.body,
      reportedBy: req.user.userId
    };
    
    const person = new Person(personData);
    await person.save();
    
    // Invalidate recognition cache
    if (recognitionRouter.invalidateCache) {
      recognitionRouter.invalidateCache();
    }
    
    res.status(201).json({
      message: 'Person created successfully',
      person
    });
    
  } catch (error) {
    console.error('Create person error:', error);
    res.status(500).json({
      error: error.message || 'Error creating person'
    });
  }
});

// Update person
router.put('/:id', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    const person = await Person.findById(req.params.id);
    
    if (!person) {
      return res.status(404).json({
        error: 'Person not found'
      });
    }
    
    // Update fields
    Object.keys(req.body).forEach(key => {
      if (key !== '_id' && key !== 'reportedBy') {
        person[key] = req.body[key];
      }
    });
    
    await person.save();
    
    // Invalidate recognition cache
    if (recognitionRouter.invalidateCache) {
      recognitionRouter.invalidateCache();
    }
    
    res.json({
      message: 'Person updated successfully',
      person
    });
    
  } catch (error) {
    console.error('Update person error:', error);
    res.status(500).json({
      error: error.message || 'Error updating person'
    });
  }
});

// Delete person (soft delete)
router.delete('/:id', authenticate, authorize(['admin']), async (req, res) => {
  try {
    const person = await Person.findById(req.params.id);
    
    if (!person) {
      return res.status(404).json({
        error: 'Person not found'
      });
    }
    
    person.isActive = false;
    await person.save();
    
    res.json({
      message: 'Person deleted successfully'
    });
    
  } catch (error) {
    console.error('Delete person error:', error);
    res.status(500).json({
      error: error.message || 'Error deleting person'
    });
  }
});

// Add face encoding to person
router.post('/:id/encodings', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    const { encoding, imageUrl } = req.body;
    
    if (!encoding || !Array.isArray(encoding)) {
      return res.status(400).json({
        error: 'Valid face encoding is required'
      });
    }
    
    const person = await Person.findById(req.params.id);
    
    if (!person) {
      return res.status(404).json({
        error: 'Person not found'
      });
    }
    
    person.faceEncodings.push({
      encoding,
      imageUrl,
      uploadedAt: new Date()
    });
    
    await person.save();
    
    // Invalidate recognition cache
    if (recognitionRouter.invalidateCache) {
      recognitionRouter.invalidateCache();
    }
    
    res.json({
      message: 'Face encoding added successfully',
      person
    });
    
  } catch (error) {
    console.error('Add encoding error:', error);
    res.status(500).json({
      error: error.message || 'Error adding face encoding'
    });
  }
});

// Add note to person
router.post('/:id/notes', authenticate, async (req, res) => {
  try {
    const { content } = req.body;
    
    if (!content) {
      return res.status(400).json({
        error: 'Note content is required'
      });
    }
    
    const person = await Person.findById(req.params.id);
    
    if (!person) {
      return res.status(404).json({
        error: 'Person not found'
      });
    }
    
    person.notes.push({
      content,
      addedBy: req.user.userId,
      addedAt: new Date()
    });
    
    await person.save();
    
    res.json({
      message: 'Note added successfully',
      person
    });
    
  } catch (error) {
    console.error('Add note error:', error);
    res.status(500).json({
      error: error.message || 'Error adding note'
    });
  }
});

// Update person status (missing/found)
router.put('/updateStatus/:id', authenticate, authorize(['admin', 'operator']), async (req, res) => {
  try {
    const { status } = req.body;
    
    if (!status || !['missing', 'found', 'active'].includes(status)) {
      return res.status(400).json({
        error: 'Valid status is required (missing, found, or active)'
      });
    }
    
    const person = await Person.findByIdAndUpdate(
      req.params.id,
      { status, updatedAt: new Date() },
      { new: true, runValidators: true }
    );
    
    if (!person) {
      return res.status(404).json({
        error: 'Person not found'
      });
    }
    
    // Invalidate recognition cache when status changes
    if (recognitionRouter.invalidateCache) {
      recognitionRouter.invalidateCache();
    }
    
    res.json({
      message: `Person status updated to ${status}`,
      person
    });
    
  } catch (error) {
    console.error('Update status error:', error);
    res.status(500).json({
      error: error.message || 'Error updating person status'
    });
  }
});

module.exports = router;
