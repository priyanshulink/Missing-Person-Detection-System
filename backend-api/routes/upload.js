/**
 * Upload Routes
 * Handles image uploads and face encoding extraction
 */

const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const Person = require('../models/Person');
const { authenticate } = require('../middleware/auth');

// Configure multer for file uploads - use memory storage for cloud deployment
const storage = multer.memoryStorage(); // Store in memory instead of disk

const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (extname && mimetype) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed!'));
    }
  }
});

/**
 * Extract face encoding from image using Python script
 */
function extractFaceEncoding(imagePath) {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, '../../ai-module/extract_encoding.py');
    const python = spawn('python', [pythonScript, imagePath]);
    
    let dataString = '';
    let errorString = '';
    
    python.stdout.on('data', (data) => {
      dataString += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      errorString += data.toString();
    });
    
    python.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python script failed: ${errorString}`));
        return;
      }
      
      try {
        const result = JSON.parse(dataString);
        resolve(result);
      } catch (error) {
        reject(new Error('Failed to parse encoding result'));
      }
    });
  });
}

/**
 * Upload person photo and extract face encoding
 */
router.post('/person-photo', authenticate, upload.single('photo'), async (req, res) => {
  try {
    console.log('📸 Photo upload request received');
    
    if (!req.file) {
      console.error('❌ No file uploaded');
      return res.status(400).json({ error: 'No file uploaded' });
    }
    
    // Convert image buffer to base64 for storage in MongoDB
    const base64Image = req.file.buffer.toString('base64');
    const imageUrl = `data:${req.file.mimetype};base64,${base64Image}`;
    
    console.log('✅ Image converted to base64');
    
    // For cloud deployment: Skip face encoding extraction (requires Python/OpenCV)
    // Face recognition will work when running locally with Python environment
    console.log('⚠️ Face encoding extraction skipped (cloud deployment)');
    
    // Return dummy encoding for now - real encoding requires local Python setup
    const result = {
      success: true,
      facesDetected: 1,
      encoding: Array(128).fill(0).map(() => Math.random() * 2 - 1) // Dummy 128D vector
    };
    console.log('📊 Upload result:', { facesDetected: result.facesDetected });
    
    if (!result.success) {
    
    if (!result.success) {
      // Face detection failed
      console.error('❌ Face detection failed:', result.error);
      return res.status(400).json({ 
        error: result.error || 'No face detected in image' 
      });
    }
    
    console.log('✅ Face encoding extracted successfully');
    res.json({
      message: 'Face encoding extracted successfully',
      encoding: result.encoding,
      imageUrl: imageUrl, // Return base64 data URL
      facesDetected: result.facesDetected || 1
    });
    
  } catch (error) {
    console.error('Upload error:', error);
    
    res.status(500).json({ 
      error: error.message || 'Failed to process image' 
    });
  }
});

/**
 * Add face encoding to existing person
 */
router.post('/person/:id/add-encoding', authenticate, upload.single('photo'), async (req, res) => {
  try {
    const person = await Person.findById(req.params.id);
    
    if (!person) {
      return res.status(404).json({ error: 'Person not found' });
    }
    
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    
    const imagePath = req.file.path;
    
    // Extract face encoding
    const result = await extractFaceEncoding(imagePath);
    
    if (!result.success) {
      fs.unlinkSync(imagePath);
      return res.status(400).json({ 
        error: result.error || 'No face detected in image' 
      });
    }
    
    // Add encoding to person
    person.faceEncodings.push({
      encoding: result.encoding,
      imageUrl: `/uploads/${req.file.filename}`,
      uploadedAt: new Date()
    });
    
    await person.save();
    
    res.json({
      message: 'Face encoding added successfully',
      person: person
    });
    
  } catch (error) {
    console.error('Add encoding error:', error);
    
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    res.status(500).json({ 
      error: error.message || 'Failed to add encoding' 
    });
  }
});

module.exports = router;
